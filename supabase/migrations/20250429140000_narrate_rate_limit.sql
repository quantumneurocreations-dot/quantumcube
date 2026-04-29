-- Per-IP rate limit buckets for Edge Function `narrate` (two windows: minute + hour).
-- Called only via SECURITY DEFINER RPC with service_role from the function.

CREATE TABLE IF NOT EXISTS public.narrate_rate_counters (
  bucket_key text PRIMARY KEY,
  hit_count int NOT NULL,
  window_end timestamptz NOT NULL
);

ALTER TABLE public.narrate_rate_counters ENABLE ROW LEVEL SECURITY;

-- No policies: anon/authenticated cannot access; service_role bypasses RLS.

CREATE OR REPLACE FUNCTION public.narrate_rate_limit_try(
  p_min_key text,
  p_hour_key text,
  p_min_cap int,
  p_hour_cap int,
  p_min_window_end timestamptz,
  p_hour_window_end timestamptz
) RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  m_cnt int;
  m_end timestamptz;
  m_active boolean := false;
  h_cnt int;
  h_end timestamptz;
  h_active boolean := false;
BEGIN
  SELECT hit_count, window_end INTO m_cnt, m_end
  FROM public.narrate_rate_counters
  WHERE bucket_key = p_min_key
  FOR UPDATE;

  IF FOUND AND m_end > now() THEN
    m_active := true;
  ELSE
    m_cnt := 0;
  END IF;

  SELECT hit_count, window_end INTO h_cnt, h_end
  FROM public.narrate_rate_counters
  WHERE bucket_key = p_hour_key
  FOR UPDATE;

  IF FOUND AND h_end > now() THEN
    h_active := true;
  ELSE
    h_cnt := 0;
  END IF;

  IF m_cnt >= p_min_cap THEN
    RETURN jsonb_build_object(
      'ok', false,
      'reason', 'minute',
      'retry_after', greatest(1, ceil(extract(epoch from (m_end - now())))::int)
    );
  END IF;

  IF h_cnt >= p_hour_cap THEN
    RETURN jsonb_build_object(
      'ok', false,
      'reason', 'hour',
      'retry_after', greatest(1, ceil(extract(epoch from (h_end - now())))::int)
    );
  END IF;

  IF m_active THEN
    UPDATE public.narrate_rate_counters
    SET hit_count = hit_count + 1
    WHERE bucket_key = p_min_key;
  ELSE
    INSERT INTO public.narrate_rate_counters (bucket_key, hit_count, window_end)
    VALUES (p_min_key, 1, p_min_window_end)
    ON CONFLICT (bucket_key) DO UPDATE
    SET hit_count = 1, window_end = EXCLUDED.window_end;
  END IF;

  IF h_active THEN
    UPDATE public.narrate_rate_counters
    SET hit_count = hit_count + 1
    WHERE bucket_key = p_hour_key;
  ELSE
    INSERT INTO public.narrate_rate_counters (bucket_key, hit_count, window_end)
    VALUES (p_hour_key, 1, p_hour_window_end)
    ON CONFLICT (bucket_key) DO UPDATE
    SET hit_count = 1, window_end = EXCLUDED.window_end;
  END IF;

  RETURN '{"ok": true}'::jsonb;
END;
$$;

REVOKE ALL ON FUNCTION public.narrate_rate_limit_try(text, text, int, int, timestamptz, timestamptz) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.narrate_rate_limit_try(text, text, int, int, timestamptz, timestamptz) TO service_role;
