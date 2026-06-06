-- Consumed Google Play purchase tokens for Edge Function `verify-play-purchase`.
-- Each successfully-verified purchaseToken is recorded here so it can never be
-- replayed to re-grant entitlement (replay / token-reuse block).
--
-- Written only via service_role from the Edge Function (RLS denies all others).
-- The UNIQUE primary key on purchase_token is the replay guard: a second
-- INSERT of the same token fails on conflict and the function refuses the grant.

CREATE TABLE IF NOT EXISTS public.play_consumed_tokens (
  purchase_token text PRIMARY KEY,
  user_id uuid NOT NULL,
  product_id text NOT NULL,
  consumed_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE public.play_consumed_tokens ENABLE ROW LEVEL SECURITY;

-- No policies: anon/authenticated cannot access; service_role bypasses RLS.

-- Lookup grants/audits by user.
CREATE INDEX IF NOT EXISTS play_consumed_tokens_user_id_idx
  ON public.play_consumed_tokens (user_id);
