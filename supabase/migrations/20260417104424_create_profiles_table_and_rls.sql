-- profiles table: one row per auth user
-- Matches schema from PROJECT_BRIEF.md: email, has_paid, marketing_consent, created_at
-- No reading history stored (per brief: readings are deterministic from inputs)

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text not null,
  has_paid boolean not null default false,
  marketing_consent boolean not null default false,
  created_at timestamptz not null default now()
);

comment on table public.profiles is 'One row per signed-up user. Stores minimum account data per Quantum Cube privacy policy: email, unlock status, marketing opt-in, creation date.';
comment on column public.profiles.id is 'Foreign key to auth.users.id. Cascades on delete so removing an auth user wipes their profile.';
comment on column public.profiles.email is 'Mirror of auth.users.email at sign-up time.';
comment on column public.profiles.has_paid is 'True once PayFast (or future processor) confirms a successful unlock payment.';
comment on column public.profiles.marketing_consent is 'True only if the user explicitly ticked the opt-in checkbox on sign-up. Unchecked by default per GDPR/POPIA.';

-- Enable Row Level Security
alter table public.profiles enable row level security;

-- Policy: users can read only their own profile row
create policy "users_select_own_profile"
on public.profiles
for select
using (auth.uid() = id);

-- Policy: users can update only their own profile row
-- Note: we intentionally do NOT allow users to update has_paid themselves.
-- has_paid must be updated server-side after payment webhook verification.
create policy "users_update_own_profile"
on public.profiles
for update
using (auth.uid() = id)
with check (
  auth.uid() = id
  -- Allow user to change marketing_consent and email, but not has_paid
  -- (Column-level check: has_paid is immutable to the user)
  and has_paid = (select has_paid from public.profiles where id = auth.uid())
);

-- Policy: users can insert their own profile row
-- (Used if sign-up trigger is bypassed or for manual profile creation)
create policy "users_insert_own_profile"
on public.profiles
for insert
with check (auth.uid() = id);

-- No DELETE policy: users cannot directly delete their profile.
-- Account deletion is handled via auth.users delete which cascades.

-- Trigger: automatically create a profile row when a new auth user is created
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email, marketing_consent)
  values (
    new.id,
    new.email,
    coalesce((new.raw_user_meta_data->>'marketing_consent')::boolean, false)
  );
  return new;
end;
$$;

create trigger on_auth_user_created
after insert on auth.users
for each row execute function public.handle_new_user();
