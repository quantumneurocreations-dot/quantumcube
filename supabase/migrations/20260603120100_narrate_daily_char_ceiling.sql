-- Global daily character ceiling for Edge Function `narrate`.
-- Every ElevenLabs call bills per character, so beyond per-IP / per-user limits
-- we cap total characters synthesised across ALL users per UTC day. This bounds
-- maximum daily spend even under distributed abuse.
--
-- Written only via SECURITY DEFINER RPC with service_role from the function.

CREATE TABLE IF NOT EXISTS public.narrate_daily_chars (
  day date PRIMARY KEY,
  char_count bigint NOT NULL DEFAULT 0
);

ALTER TABLE public.narrate_daily_chars ENABLE ROW LEVEL SECURITY;

-- No policies: anon/authenticated cannot access; service_role bypasses RLS.

-- Atomically reserve p_chars against the day's budget. Returns:
--   { ok: true, remaining: <bigint> }                 when within the cap
--   { ok: false, reason: 'daily_cap', remaining: 0 }  when the request would exceed it
-- The reservation is rejected (and NOT counted) when it would breach the cap, so
-- a single oversized request cannot blow past the ceiling.
CREATE OR REPLACE FUNCTION public.narrate_daily_chars_try(
  p_day date,
  p_chars int,
  p_cap bigint
) RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  cur bigint;
BEGIN
  SELECT char_count INTO cur
  FROM public.narrate_daily_chars
  WHERE day = p_day
  FOR UPDATE;

  IF NOT FOUND THEN
    cur := 0;
  END IF;

  IF cur + p_chars > p_cap THEN
    RETURN jsonb_build_object(
      'ok', false,
      'reason', 'daily_cap',
      'remaining', greatest(0, p_cap - cur)
    );
  END IF;

  INSERT INTO public.narrate_daily_chars (day, char_count)
  VALUES (p_day, p_chars)
  ON CONFLICT (day) DO UPDATE
  SET char_count = public.narrate_daily_chars.char_count + EXCLUDED.char_count;

  RETURN jsonb_build_object('ok', true, 'remaining', p_cap - (cur + p_chars));
END;
$$;

REVOKE ALL ON FUNCTION public.narrate_daily_chars_try(date, int, bigint) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.narrate_daily_chars_try(date, int, bigint) TO service_role;
