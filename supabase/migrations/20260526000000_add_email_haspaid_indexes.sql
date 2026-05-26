-- Add indexes for email and has_paid columns
-- Reason: email used in admin/auth lookups; has_paid for reporting queries
-- Primary key (id) already handles all RLS-filtered app queries
CREATE INDEX IF NOT EXISTS profiles_email_idx ON public.profiles (email);
CREATE INDEX IF NOT EXISTS profiles_has_paid_idx ON public.profiles (has_paid);
