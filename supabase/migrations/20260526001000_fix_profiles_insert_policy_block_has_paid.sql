-- Fix: prevent users from self-granting paid status on profile insert
-- Old policy only checked id = auth.uid(), not has_paid value
-- Vulnerability: user could POST directly to Supabase REST with has_paid=true
DROP POLICY IF EXISTS "users_insert_own_profile" ON profiles;

CREATE POLICY "users_insert_own_profile" ON profiles
FOR INSERT WITH CHECK (
  (SELECT auth.uid()) = id
  AND has_paid = false
);

COMMENT ON TABLE profiles IS 'User profiles. has_paid is server-only — only Dodo webhook (service_role) may set true.';
