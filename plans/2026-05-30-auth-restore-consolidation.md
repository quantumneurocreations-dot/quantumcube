# Auth Session-Restore Consolidation — Implementation Plan

> **For the implementing session:** This is a structural refactor of the live auth/payment path. Execute on a **feature branch** (`auth-restore-consolidation`), one task at a time, and **device-test on a real Android TWA before merge** (Task 9). Steps use checkbox (`- [ ]`) syntax.

**Goal:** Replace the three duplicated session-restore code paths and the overloaded `_qcSessionRestored` flag with a single idempotent restore function driven by an explicit auth state machine, so the cold-start blank-page class of bugs (Sentry JAVASCRIPT-8, plus the v348/v355 symptoms) is closed at the root.

**Architecture:** One state variable `_qcAuthPhase` (`idle → restoring → restored | awaiting-input`) plus a dedicated loader-dismiss signal `_qcAuthSettled`. All three triggers (DOMContentLoaded init, `onAuthStateChange`, `visibilitychange`) become thin callers of one function `_qcResolveAuth(session, source)`. The auth loader dismisses **only** on `_qcAuthSettled || currentFace !== 0 || 12s timeout` — never on a "restore committed but not yet navigated" state, which is what caused the blank flash.

**Tech Stack:** Vanilla JS in `docs/app.html`, Supabase JS v2 auth, service worker `docs/sw.js` (cache-version gated). No build step, no test framework — verification is manual device testing + Sentry breadcrumbs.

**Version:** Ships as `qc-v356`. Bump `docs/app.html` Sentry release + `docs/sw.js` `CACHE` to `qc-v356` **once** in Task 1; the pre-commit hook only requires `current !== origin/main`, so every later commit on the branch keeps `qc-v356` and still passes.

---

## Why this exists (root cause, one paragraph)

`_qcSessionRestored` is overloaded to mean three different things: (1) "a restore path has committed — don't let another double-fire," (2) "the user successfully navigated off face 0," and (3) "the auth loader may dismiss." On cold start, path A (`initSupabaseSession`) sets it `true` *before* its `setTimeout`-deferred `runCalculation()` confirms navigation. When that `runCalculation` silently returns early (Android autofill DOM corruption — see v314/v343), the user is stranded on blank face 0 with the flag latched `true`, and both the loader poll (`docs/app.html:2287`) and the unconditional `_qcHideAuthLoader()` at the end of `onAuthStateChange` (`docs/app.html:4810`) dismiss the loader before nav, producing the blank flash. v348/v355 patched symptoms of this same conflation. Splitting the three concerns into a phase machine + a settled signal is the permanent fix.

---

## File Structure

Single file changes (this app is one HTML file; do **not** restructure into modules — follow the established pattern):

- **Modify `docs/app.html`** — all logic changes below.
- **Modify `docs/sw.js`** — cache version bump only (Task 1).
- No new files. No test files (no harness exists).

### Touch-point inventory (current line numbers, pre-change)

| # | Location | Current role | Change |
|---|----------|--------------|--------|
| 1 | `1230` `let _qcSessionRestored = false;` | overloaded flag | Replace with `_qcAuthPhase` + `_qcAuthSettled` (Task 2) |
| 2 | `2106–2135` `visibilitychange` handler | duplicate restore path C | Thin caller of `_qcResolveAuth` (Task 6) |
| 3 | `2121` `if(_qcSessionRestored) return;` | visibility guard | Becomes phase guard (Task 6) |
| 4 | `2285–2295` `_qcLoaderPoll` + dismiss `2287` | loader dismiss | Key off `_qcAuthSettled` (Task 5) |
| 5 | `4059–4201` `initSupabaseSession()` | restore path A | Thin caller of `_qcResolveAuth` (Task 4) |
| 6 | `4167`, `4191` `_qcSessionRestored = true` | optimistic flag sets | Removed (logic moves into `_qcResolveAuth`) (Task 4) |
| 7 | `4581–4811` `onAuthStateChange` | restore path B + SIGNED_OUT + loader dismiss | Route to `_qcResolveAuth`; rewrite SIGNED_OUT; remove `4810` unconditional dismiss (Task 7) |
| 8 | `4629` `_isLateRestore`, `4683` `isSessionRestore`, `4690–4756` restore block, `4753` v355 rescue | duplicate restore + band-aid | Deleted, replaced by `_qcResolveAuth` call (Task 7) |
| 9 | `4592` SIGNED_OUT cold-start branch | uses `!_qcSessionRestored` | Phase-aware (Task 7) |

`_qcOtpVerifying` (`1226`) stays a **separate** concern — the OTP verify path (`_qcOtpVerify`, ~`4380`) is intricate and already well-guarded; `_qcResolveAuth` will check it and bail, exactly as the current code does. Folding OTP into the phase machine is explicitly **out of scope** (YAGNI / blast-radius control).

---

## The state machine (reference — implemented in Task 2/3)

```
_qcAuthPhase values:
  'idle'           — nothing decided yet (initial); a restore may start
  'restoring'      — a restore is in flight (profile fetch / runCalc pending); blocks re-entry
  'restored'       — navigated to a content face (currentFace !== 0); terminal
  'awaiting-input' — settled deliberately on face 0 (no session / signed out /
                     incomplete profile / brand-new user); terminal-for-loader

_qcAuthSettled (bool): true once phase is 'restored' OR 'awaiting-input'.
                       The auth loader dismisses ONLY on (_qcAuthSettled || currentFace !== 0 || 12s).

Critical rule: on a FAILED nav (runCalc ran but currentFace still 0), phase returns
to 'idle' and _qcAuthSettled stays false — the loader stays up and a later trigger
retries. This is what fixes both the stranding AND the flash.
```

---

## Task 1: Branch + version bump

**Files:**
- Modify: `docs/app.html:659` (Sentry release)
- Modify: `docs/sw.js:1` (cache key)

- [ ] **Step 1: Create the feature branch**

```bash
cd /Users/qnc/Projects/quantumcube
git checkout -b auth-restore-consolidation
```

- [ ] **Step 2: Bump Sentry release in `docs/app.html`**

Change line 659 from `release: "quantum-cube@qc-v355",` to:
```js
      release: "quantum-cube@qc-v356",
```

- [ ] **Step 3: Bump SW cache in `docs/sw.js`**

Change line 1 from `const CACHE='qc-v355';` to:
```js
const CACHE='qc-v356';
```

- [ ] **Step 4: Commit**

```bash
git add docs/app.html docs/sw.js
git commit -m "qc-v356: branch open — auth restore consolidation (version bump)"
```
Expected: pre-commit prints `✓ pre-commit: SW + Sentry release in sync at qc-v356, bump verified`.

---

## Task 2: Replace the overloaded flag with the phase machine state

**Files:**
- Modify: `docs/app.html:1224–1230` (state declarations)

- [ ] **Step 1: Replace the `_qcSessionRestored` declaration**

At `docs/app.html:1230`, replace:
```js
let _qcSessionRestored = false;
```
with:
```js
// v356: auth restore state machine. Replaces the overloaded _qcSessionRestored flag,
// which conflated "double-fire guard" + "nav succeeded" + "loader may dismiss".
//   'idle' | 'restoring' | 'restored' | 'awaiting-input'
let _qcAuthPhase = 'idle';
// Loader-dismiss signal — true once we've reached a stable end state (navigated to a
// content face, or settled deliberately on face 0). NEVER true mid-restore.
let _qcAuthSettled = false;
// Back-compat shim: some legacy reads remain until Task 8 sweeps them. Kept as a
// getter-like convention — true only once a restore genuinely succeeded.
// (Do NOT write to this directly; it is derived. Task 8 removes remaining readers.)
```

- [ ] **Step 2: Verify no syntax break**

Run:
```bash
node --check <(sed -n '/<script>/,/<\/script>/p' docs/app.html 2>/dev/null) 2>/dev/null || echo "manual-check: open docs/app.html in browser, confirm no console ReferenceError on load"
```
Expected: no parse error. (The `sed` extraction is best-effort; the authoritative check is loading the page — Step 3.)

- [ ] **Step 3: Commit**

```bash
git add docs/app.html
git commit -m "qc-v356: add _qcAuthPhase state machine, retire _qcSessionRestored decl"
```

> NOTE: This commit intentionally leaves dangling references to `_qcSessionRestored` (they're fixed in Tasks 4–8). The app is **not** expected to run cleanly until Task 8. Do not deploy mid-branch.

---

## Task 3: Add the single restore function + profile-fetch helper

**Files:**
- Modify: `docs/app.html` — insert immediately **before** `function initSupabaseSession()` (currently `:4059`)

- [ ] **Step 1: Insert the profile-fetch helper and `_qcResolveAuth`**

Insert this block before `async function initSupabaseSession(){`:

```js
// v356: single source of truth for "fetch this user's profile". Replaces three
// copy-pasted `sb.from("profiles").select(...)` calls (initSupabaseSession,
// onAuthStateChange, visibilitychange).
async function _qcFetchProfile(userId){
  try {
    // v356 (Task 7): 8s timeout. Supabase query builder is a thenable, so Promise.race
    // works. On timeout we throw → caught below → return null, so _qcResolveAuth settles
    // cleanly via the no-profile branch instead of latching _qcAuthPhase at 'restoring'
    // forever and blocking every future restore. A later auth/visibility event retries.
    const { data } = await Promise.race([
      sb.from("profiles")
        .select("id,email,has_paid,marketing_consent,dob,name,edit_count")
        .eq("id", userId).maybeSingle(),
      new Promise((_, reject) => setTimeout(() => reject(new Error('fetch-profile-timeout')), 8000))
    ]);
    return data || null;
  } catch(e){
    console.error("[QC] _qcFetchProfile error:", e);
    try { if(window.Sentry) Sentry.captureException(e, { tags: { area: 'fetch-profile' } }); } catch(_){}
    return null;
  }
}

// v356: apply a fetched profile to the shared lock/unlock state. Pure side-effects on
// globals — no navigation. Centralises what was duplicated across all three paths.
function _qcApplyProfile(profile){
  qcCurrentProfile = profile || null;
  _qcSavedName = (profile && profile.name) || null;
  _qcSavedDob  = (profile && profile.dob)  || null;
  _qcSavedEditCount = (profile && typeof profile.edit_count === 'number') ? profile.edit_count : 0;
  try { syncUnlockFromProfile(profile); } catch(_){}
}

// v356: mark a terminal "settled" state and let the loader dismiss. Idempotent.
function _qcSettle(phase, reason, ctx){
  _qcAuthPhase = phase;            // 'restored' | 'awaiting-input'
  _qcAuthSettled = true;
  try { _qcSessionNav('settled:'+phase+' ('+reason+')', ctx || {}); } catch(_){}
}

// v356: THE single restore-and-navigate entry point. Every trigger calls this.
//   session: a Supabase session object (or null/undefined for "no session")
//   source : 'init' | 'authchange' | 'visibility'  (breadcrumb only)
// Idempotent + re-entrancy-safe via _qcAuthPhase. On a FAILED nav it returns the
// phase to 'idle' (NOT settled) so a later trigger retries and the loader stays up.
async function _qcResolveAuth(session, source){
  const ctx = { source, phase: _qcAuthPhase, currentFace,
                hasSession: !!(session && session.user) };

  // The OTP verify path owns its own SIGNED_IN — never interfere with it.
  if(_qcOtpVerifying){ try { _qcSessionNav('resolveAuth skip — otp verifying', ctx); } catch(_){} return; }

  // Idempotency / re-entrancy: a restore in flight or already-succeeded short-circuits.
  if(_qcAuthPhase === 'restoring' || _qcAuthPhase === 'restored'){
    try { _qcSessionNav('resolveAuth skip — phase '+_qcAuthPhase, ctx); } catch(_){}
    return;
  }

  // No session → settle on face 0 (show the form), unless we already restored.
  if(!session || !session.user){
    if(_qcAuthPhase !== 'restored') _qcSettle('awaiting-input', 'no session', ctx);
    return;
  }

  _qcAuthPhase = 'restoring';
  qcCurrentUser = session.user;
  try { if(session.user.email) localStorage.setItem('qc_last_email', session.user.email); } catch(_){}
  updateSettingsLinkVisibility();
  try { restorePendingProfile(); } catch(_){}

  const profile = await _qcFetchProfile(session.user.id);
  _qcApplyProfile(profile);
  try { restorePlayPurchases().catch(()=>{}); } catch(_){}

  // If the user already navigated to a content face during the await, don't interrupt.
  if(currentFace !== 0){ _qcSettle('restored', 'already on content face', ctx); return; }

  const complete = profile && profile.name && profile.dob;
  if(!complete){
    // Incomplete profile (or brand-new user with metadata only) → stay on face 0 to
    // complete it. Recover any stashed signup metadata, then settle (loader dismisses).
    try {
      if(!profile){
        const meta = session.user.user_metadata || {};
        let hasPending = false; try { hasPending = !!localStorage.getItem(QC_PENDING_KEY); } catch(_){}
        if(!hasPending && (meta.pending_first_name || meta.pending_dob_year)){
          const set = (id,v)=>{const el=document.getElementById(id);if(el&&v!=null&&v!=='')el.value=v;};
          set("firstName",meta.pending_first_name); set("middleName",meta.pending_middle_name);
          set("lastName",meta.pending_last_name); set("dobDay",meta.pending_dob_day);
          set("dobMonth",meta.pending_dob_month); set("dobYear",meta.pending_dob_year);
          if(typeof updateCalcBtnReady === "function") updateCalcBtnReady();
        }
      } else {
        populateFormFromProfile(profile, session.user);
        const errEl = document.getElementById('errMsg');
        if(errEl){ errEl.textContent = "Welcome back! Please enter your name and date of birth to reveal your Cube."; errEl.style.display = "block"; errEl.style.color = "#0cc0df"; }
      }
      const emEl = document.getElementById('email');
      if(emEl){ emEl.readOnly = false; emEl.style.opacity = ""; }
    } catch(_){}
    _qcSettle('awaiting-input', !profile ? 'no profile' : 'incomplete profile', ctx);
    return;
  }

  // Complete profile → force-populate (clears autofill corruption) + navigate.
  try {
    _qcForcePopulateFromProfile(profile, session.user);
    runCalculation();
  } catch(e){
    console.error("[QC] _qcResolveAuth runCalculation:", e);
    try { if(window.Sentry) Sentry.captureException(e, { tags: { area: 'resolve-auth-runcalc' } }); } catch(_){}
  }

  if(currentFace !== 0){ _qcSettle('restored', 'runCalculation navigated', ctx); return; }

  // Nav did NOT happen (silent early-return — autofill DOM corruption). Retry once
  // after the DOM settles. If it still fails, drop back to 'idle' (NOT settled) so a
  // later trigger / the 12s loader timeout handles it — loader stays up meanwhile.
  _qcAuthPhase = 'idle';
  setTimeout(function(){
    if(currentFace === 0 && _qcAuthPhase === 'idle' && !_qcOtpVerifying){
      try {
        _qcForcePopulateFromProfile(profile, session.user);
        runCalculation();
      } catch(e){ try { showFace(1); } catch(_){} }
      if(currentFace !== 0){ _qcSettle('restored', 'runCalculation navigated (retry)', ctx); }
      else {
        try { if(window.Sentry) Sentry.captureMessage('v356: restore retry still on face 0', { level:'warning', extra: ctx }); } catch(_){}
        // v356 (Task 7 quality pass): force-settle so the loader dismisses now (form is
        // force-populated; user can tap Reveal) instead of hanging 12s. 'awaiting-input'
        // still lets a later auth/visibility event retry.
        _qcSettle('awaiting-input', 'restore retry failed — force settle', ctx);
      }
    }
  }, 300);
}
```

- [ ] **Step 2: Sanity-check references**

Confirm every symbol used by `_qcResolveAuth` exists in the file:
```bash
cd /Users/qnc/Projects/quantumcube
for sym in _qcForcePopulateFromProfile populateFormFromProfile runCalculation syncUnlockFromProfile restorePendingProfile restorePlayPurchases updateSettingsLinkVisibility _qcSessionNav updateCalcBtnReady QC_PENDING_KEY qcCurrentProfile _qcSavedName _qcSavedEditCount; do
  printf '%-30s ' "$sym"; grep -c "$sym" docs/app.html;
done
```
Expected: every symbol returns ≥ 1 (≥ 2 for ones the new function references plus their definition). If any returns the new-function count only (i.e., undefined elsewhere), STOP and resolve before continuing.

- [ ] **Step 3: Commit**

```bash
git add docs/app.html
git commit -m "qc-v356: add _qcResolveAuth single restore fn + profile helpers"
```

---

## Task 4: Rewire `initSupabaseSession` to call `_qcResolveAuth`

**Files:**
- Modify: `docs/app.html:4059–4201` (`initSupabaseSession`)

- [ ] **Step 1: Replace the body of `initSupabaseSession`**

Replace the entire function (`async function initSupabaseSession(){ … }`, lines `4059–4201`) with:

```js
async function initSupabaseSession(){
  // v356: thin trigger. getSession (12s timeout — v347) then hand off to the single
  // restore function. All populate/runCalc/flag logic now lives in _qcResolveAuth.
  let session = null, resolved = false;
  try {
    const r = await Promise.race([
      sb.auth.getSession(),
      new Promise((_, reject) => setTimeout(() => reject(new Error('getSession-timeout-init')), 12000))
    ]);
    session = r && r.data ? r.data.session : null;
    resolved = true;
  } catch(e){
    // v347: log but NEVER clear the token on a getSession error. SIGNED_OUT fires for a
    // genuinely-invalid token; INITIAL_SESSION/TOKEN_REFRESHED fires when a valid-but-slow
    // token finishes refreshing — both routed through _qcResolveAuth via onAuthStateChange.
    try { if(window.Sentry) Sentry.addBreadcrumb({ category:'auth', level:'warning', message:'initSupabaseSession getSession error', data:{ msg: e && e.message } }); } catch(_){}
  }
  try { localStorage.removeItem('qc_last_magic'); } catch(_){}  // v283 cleanup
  // Defensive: keep the email field editable (cross-device / autofill edge cases — v275/v267).
  try { const emEl = document.getElementById('email'); if(emEl){ emEl.readOnly = false; emEl.style.opacity = ''; } } catch(_){}
  // v356 review-fix: only resolve when getSession actually returned. On timeout/error,
  // leave phase 'idle' and let onAuthStateChange resolve it under the loader — passing
  // null here would flash the signup form for slow-network users with a valid token.
  if(resolved) await _qcResolveAuth(session, 'init');
}
```

- [ ] **Step 2: Confirm the optimistic flag sets are gone**

Run:
```bash
cd /Users/qnc/Projects/quantumcube
grep -n "_qcSessionRestored = true" docs/app.html
```
Expected: only the `onAuthStateChange` copy at (old) `4691` remains — it's removed in Task 7. The two `initSupabaseSession` sets (`4167`, `4191`) must be **gone**.

- [ ] **Step 3: Commit**

```bash
git add docs/app.html
git commit -m "qc-v356: initSupabaseSession becomes thin _qcResolveAuth caller"
```

---

## Task 5: Loader dismisses on `_qcAuthSettled`, not the old flag

**Files:**
- Modify: `docs/app.html:2287` (loader poll dismiss condition)

- [ ] **Step 1: Update the poll condition**

At `docs/app.html:2287`, replace:
```js
  if(_qcSessionRestored || currentFace !== 0){
```
with:
```js
  if(_qcAuthSettled || currentFace !== 0){   // v356: dismiss only on a settled state or real nav
```

- [ ] **Step 2: Confirm the 12s hard timeout still exists below it**

Run:
```bash
grep -n "elapsed >= 12000" docs/app.html
```
Expected: 1 match (the hard timeout fallback at ~`2293` is unchanged — it still dismisses after 12s so the loader can never hang forever).

- [ ] **Step 3: Commit**

```bash
git add docs/app.html
git commit -m "qc-v356: auth loader dismisses on _qcAuthSettled (not the overloaded flag)"
```

---

## Task 6: `visibilitychange` becomes a thin caller

**Files:**
- Modify: `docs/app.html:2106–2135` (`visibilitychange` handler)

- [ ] **Step 1: Replace the handler body**

Replace the whole `document.addEventListener('visibilitychange', async function(){ … });` block (`2106–2135`) with:

```js
// v356: returning-to-tab handler — now a thin trigger. Reads the session from
// localStorage (avoids the getSession hang) and hands off to the single restore fn,
// which is itself idempotent (won't double-run if already restored/restoring).
document.addEventListener('visibilitychange', async function(){
  if(document.visibilityState !== 'visible') return;
  if(_qcDodoInFlight) return;                 // never interfere with a checkout in flight
  if(_qcOtpVerifying) return;                 // OTP path owns SIGNED_IN
  if(_qcAuthPhase === 'restored') return;     // already inside — nothing to do
  if(currentFace !== 0) return;               // only act while stranded on face 0
  let session = null;
  try { session = _readSessionFromStorage(); } catch(_){}
  if(session && session.user){ await _qcResolveAuth(session, 'visibility'); }
});
```

> NOTE: `_readSessionFromStorage()` returns a `{ access_token, user, … }` shape (defined ~`3064`); `_qcResolveAuth` only reads `session.user`, so this is compatible. The v348 fix (no `saveProfileFromForm` on a passive event) is preserved — the new handler never writes.

- [ ] **Step 2: Commit**

```bash
git add docs/app.html
git commit -m "qc-v356: visibilitychange becomes thin _qcResolveAuth caller"
```

---

## Task 7: Rewrite the `onAuthStateChange` handler

**Files:**
- Modify: `docs/app.html:4581–4811` (`onAuthStateChange` callback)

This is the largest change. The handler currently contains: the `_isLateRestore` computation, the duplicate `isSessionRestore` restore block, the `CheckEmail` branch, the v355 rescue branch, the SIGNED_OUT handlers, and the unconditional loader dismiss. All of it collapses to event routing + `_qcResolveAuth`.

- [ ] **Step 1: Replace the entire `onAuthStateChange` callback**

Replace `sb.auth.onAuthStateChange(async (event, session) => { … });` (`4581`-ish through `4811`) with:

```js
sb.auth.onAuthStateChange(async (event, session) => {
  try { if(window.Sentry) Sentry.addBreadcrumb({ category:'auth', level:'info', message:'authchange: '+event, data:{ hasSession: !!(session&&session.user), currentFace, phase:_qcAuthPhase } }); } catch(_){}

  // Post-payment unlock path (unchanged contract — see attemptPaymentUnlock).
  if (_qcPendingPaymentUnlock && (event === "SIGNED_IN" || event === "INITIAL_SESSION") && session?.user) {
    attemptPaymentUnlock(session);
  }

  if(event === "SIGNED_OUT"){
    // Clear all user state and settle on face 0 with a gentle message if this was a
    // cold-start expiry (we never reached a content face).
    qcCurrentUser = null; qcCurrentProfile = null;
    _qcSavedName = null; _qcSavedDob = null; _qcSavedEditCount = 0; _qcUnlockForEditUsed = false;
    updateSettingsLinkVisibility();
    try { localStorage.removeItem(STORE_KEY); } catch(_){}
    try { localStorage.removeItem(QC_PENDING_KEY); } catch(_){}
    if(currentFace === 0 && _qcAuthPhase !== 'restored'){
      try {
        const storedEmail = localStorage.getItem('qc_last_email');
        const emEl = document.getElementById('email');
        if(emEl){ emEl.readOnly = false; emEl.style.opacity = ""; if(storedEmail && !emEl.value) emEl.value = storedEmail; else if(!storedEmail) emEl.value = ""; }
        const errEl = document.getElementById('errMsg');
        if(errEl){ errEl.textContent = 'Your session expired. Enter your email to sign in again.'; errEl.style.display = 'block'; errEl.style.color = '#0cc0df'; }
      } catch(_){}
      _qcSettle('awaiting-input', 'signed out on face 0', { event });
    }
    try { _qcHideAuthLoader(); } catch(_){}   // a SIGNED_OUT is itself a resolved state
    return;
  }

  // OTP/magic-link completion: the OTP verify path owns SIGNED_IN while verifying.
  if(_qcOtpVerifying) return;

  // Any event carrying a session → route through the single restore fn. INITIAL_SESSION
  // and TOKEN_REFRESHED are the "late restore" recoveries (valid-but-slow token); SIGNED_IN
  // is a fresh login. _qcResolveAuth is idempotent, so duplicate events are safe no-ops.
  if((event === "SIGNED_IN" || event === "INITIAL_SESSION" || event === "TOKEN_REFRESHED") && session && session.user){
    try { localStorage.removeItem('qc_last_magic'); } catch(_){}
    await _qcResolveAuth(session, 'authchange');
  }

  // NOTE: the v318 unconditional _qcHideAuthLoader() at the end of this handler is
  // REMOVED. Loader dismissal is now owned solely by the poll (Task 5), keyed off
  // _qcAuthSettled / currentFace / 12s. SIGNED_OUT above dismisses explicitly.
});
```

- [ ] **Step 2: Confirm the old duplicated blocks are gone**

Run:
```bash
cd /Users/qnc/Projects/quantumcube
grep -n "no nav action (left user in place)\|isSessionRestore\|_isLateRestore\|v355 rescue\|_qcSessionRestored = true" docs/app.html
```
Expected: **zero matches.** All of it now lives in `_qcResolveAuth`.

- [ ] **Step 3: Commit**

```bash
git add docs/app.html
git commit -m "qc-v356: collapse onAuthStateChange restore paths into _qcResolveAuth; drop unconditional loader dismiss"
```

---

## Task 8: Sweep remaining `_qcSessionRestored` readers

**Files:**
- Modify: `docs/app.html` — every remaining reference

- [ ] **Step 1: Find all remaining references**

```bash
cd /Users/qnc/Projects/quantumcube
grep -n "_qcSessionRestored" docs/app.html
```
Expected remaining readers after Tasks 4 & 7: the `visibilitychange` guard was already replaced (Task 6); the SIGNED_OUT cold-start branch was replaced (Task 7). Any leftover is a stale reader.

- [ ] **Step 2: Replace each remaining reader**

For each line the grep returns, apply this mapping:
- `!_qcSessionRestored` (meaning "not yet restored") → `_qcAuthPhase !== 'restored'`
- `_qcSessionRestored` (meaning "already restored") → `_qcAuthPhase === 'restored'`

(There should be 0–1 left; if the codebase is clean after Tasks 4/6/7, this task is a no-op verification.)

- [ ] **Step 3: Confirm zero references remain**

```bash
grep -c "_qcSessionRestored" docs/app.html
```
Expected: `0`.

- [ ] **Step 4: Commit (skip if Step 1 found nothing)**

```bash
git add docs/app.html
git commit -m "qc-v356: remove last _qcSessionRestored readers — phase machine is sole source of truth"
```

---

## Task 9: Device test (REQUIRED before merge — no skipping)

**No code.** This is the verification that replaces the missing unit tests. Run every scenario on a **real Android TWA build** (the autofill DOM-corruption timing that caused this entire bug class does not reproduce in desktop Chrome). Use the `?review=qncreview2026` bypass only for non-auth scenarios.

Build/serve the branch to a test channel first (do **not** deploy to prod main).

- [ ] **Scenario A — cold start, returning paid user (the JAVASCRIPT-8 case).** Force-quit the app, reopen. **Expected:** auth loader stays visible until the cube appears; lands on a content face with the reading; **no blank face-0 flash**; no pull-to-refresh needed. Sentry breadcrumbs show `authchange: INITIAL_SESSION` → `settled:restored (runCalculation navigated)`.
- [ ] **Scenario B — cold start, returning user with autofill active.** Ensure Android has saved form data for the field. Cold start 5×. **Expected:** every launch lands in the cube, no flash. If the first `runCalculation` returns early, breadcrumbs show the retry then `settled:restored (...retry)` — loader never dismissed to blank.
- [ ] **Scenario C — brand-new user, no session.** Fresh install / cleared storage. **Expected:** loader dismisses promptly to the **sign-up form** (not a 12s hang). Breadcrumb `settled:awaiting-input (no session)`.
- [ ] **Scenario D — incomplete profile (name/dob missing).** Account with a profile row lacking dob. **Expected:** loader dismisses to face 0 with the "enter your name and date of birth" message; email field editable. Breadcrumb `settled:awaiting-input (incomplete profile)`.
- [ ] **Scenario E — session expired.** Invalidate the refresh token server-side, cold start. **Expected:** "Your session expired" message, email pre-filled, form usable. Breadcrumb `settled:awaiting-input (signed out on face 0)`.
- [ ] **Scenario F — OTP sign-up end to end.** New email → OTP → verify. **Expected:** unchanged from today; `_qcResolveAuth` logs `skip — otp verifying` during verification (proving no interference). Lands in cube after verify.
- [ ] **Scenario G — no double-fire.** On any successful cold start, confirm exactly **one** `settled:restored` breadcrumb and exactly **one** profile fetch (check network tab / `profiles` request count). Two = double-fire regression.
- [ ] **Scenario H — payment still works.** Tap Pay → Dodo overlay → complete $17 → unlock. Confirm `_qcDodoInFlight` guards still suppress visibility re-entry (no auth side-effects mid-checkout).
- [ ] **Scenario I — foreground while idle on face 0 lock card.** Paid user navigates back to face 0 (sees lock card), backgrounds, foregrounds. **Expected:** NOT yanked to a content face (phase is `restored`, visibility handler returns early). Lock card stays.

- [ ] **Final step: Merge only after all 9 pass**

```bash
cd /Users/qnc/Projects/quantumcube
git checkout main
git merge --no-ff auth-restore-consolidation -m "qc-v356: auth session-restore consolidation — single state machine + restore fn"
# then deploy per the standard runbook (frontend push; no edge-function change in this branch)
```

---

## Rollback

This branch touches **only the frontend** (`app.html` + `sw.js`) — no edge-function deploy. Rollback is a frontend revert:
```bash
git revert --no-commit <merge-sha>
# bump SW + Sentry release to qc-v357 (the hook requires a bump on any app.html change)
git commit -m "qc-v357: revert auth consolidation (qc-v356) — <reason>"
git push origin main
```
Because there's no DB/edge change, revert is clean and immediate. Keep the branch around until v356 has soaked in production for a few days.

---

## Task 7 — Post-Codex hardening (applied)

After the onAuthStateChange rewrite, the Codex layer (third review) found real auth/payment
issues. Fixed #1/#2/#4/#6 (deferred #3 cosmetic, #5 pre-existing-minor). Canonical code is in
`docs/app.html`; summary of changes:

- **New state:** `_qcAuthGen` (bumped on SIGNED_OUT), `_qcProfileRetryScheduled` (bounds the
  fetch-failure retry to once/load), `const _QC_FETCH_FAILED = Symbol(...)` (fetch-failed sentinel).
- **#1 resurrection race:** `_qcResolveAuth` snapshots `const _gen = _qcAuthGen` before the
  profile-fetch await; after the await (and in the runCalc retry) it aborts if `_qcAuthGen !== _gen`
  (a SIGNED_OUT bumped it), resetting `'restoring' → 'idle'` so it can't apply stale state / navigate.
- **#2 fetch-failure vs no-row:** `_qcFetchProfile` returns `_QC_FETCH_FAILED` on timeout/error
  (null stays = genuine no-row). On failure with a valid session, `_qcResolveAuth` settles
  `awaiting-input` (loader dismisses) AND schedules one `1500ms` retry so a complete-profile user
  isn't stranded (events during `'restoring'` were skipped).
- **#4 payment downgrade:** `_qcResolveAuth` early-returns when `_qcPendingPaymentUnlock` is true —
  `attemptPaymentUnlock` owns the unlock + nav; prevents a stale unpaid profile re-locking a paid user.
- **#6 OAuth prefill:** the `!profile` branch calls `populateFormFromProfile(null, session.user)` to
  restore email/name prefill lost in the rewrite.

**Re-review round (superpowers quality + Codex, on the hardened result):**
- **Quality pass:** `_qcApplyProfile` now only runs when `!_fetchFailed` (don't stomp cached
  unlock/profile state on a transient failure before the retry recovers it).
- **Codex pass (HIGH):** `_qcFetchProfile` now destructures `{ data, error }` and returns
  `_QC_FETCH_FAILED` when `error` is set — Supabase reports API/RLS/network errors as `{ error }`
  WITHOUT throwing, so the throw-only catch missed them and misclassified errors as no-row.
- **Codex pass (MEDIUM):** the fetch-failure retry timer now also skips when `_qcAuthPhase ===
  'restoring'` (a later event-driven restore took over during the 1500ms window) to prevent a
  double-fire that would clobber the in-flight restore's phase.

## Self-review notes (done by author)

- **Spec coverage:** state machine (Task 2) ✓, single restore fn (Task 3) ✓, loader rewrite (Task 5) ✓, all touch points from the inventory (Tasks 4/6/7/8) ✓, device testing (Task 9) ✓.
- **OTP scope:** deliberately left as a separate `_qcOtpVerifying` concern — documented, not an omission.
- **Type/name consistency:** `_qcResolveAuth(session, source)`, `_qcFetchProfile(userId)`, `_qcApplyProfile(profile)`, `_qcSettle(phase, reason, ctx)`, states `idle|restoring|restored|awaiting-input`, signal `_qcAuthSettled` — used identically across all tasks.
- **Known residual risk:** if `runCalculation` silently fails on BOTH the initial call and the 300ms retry across ALL triggers, the loader still falls through to its 12s timeout and shows face 0 — but now with a `v356: restore retry still on face 0` Sentry warning, so it's observable rather than silent. This is strictly better than today and is the floor we accept until/unless the autofill-corruption root cause in `runCalculation`/`populateFormFromProfile` is itself addressed (separate effort).
