-- Add dob + name columns to profiles
-- Supports OAuth signup flow (Google returns email + name but not DOB)
-- and persistent storage of magic-link users' DOB + name across sessions

alter table public.profiles
  add column if not exists dob date,
  add column if not exists name text;

comment on column public.profiles.dob is 'User date of birth. Required for numerology/astrology calculations. Collected via signup form (magic-link) or post-OAuth modal (Google).';
comment on column public.profiles.name is 'User display name. Magic-link users provide this on signup; OAuth users get it from the provider.';

-- Update handle_new_user to capture dob + name from auth metadata
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email, marketing_consent, dob, name)
  values (
    new.id,
    new.email,
    coalesce((new.raw_user_meta_data->>'marketing_consent')::boolean, false),
    nullif(new.raw_user_meta_data->>'dob','')::date,
    coalesce(
      nullif(new.raw_user_meta_data->>'name',''),
      nullif(new.raw_user_meta_data->>'full_name',''),
      null
    )
  );
  return new;
end;
$$;

-- Update RLS update policy to allow user to update dob + name (not has_paid)
drop policy if exists "users_update_own_profile" on public.profiles;
create policy "users_update_own_profile"
on public.profiles
for update
using (auth.uid() = id)
with check (
  auth.uid() = id
  and has_paid = (select has_paid from public.profiles where id = auth.uid())
);
