import subprocess, sys

FILE = "/Users/qnc/Projects/quantumcube/quantum-cube-v10.html"

def check_run_calc(when):
    r = subprocess.run(["grep", "-n", "function runCalculation", FILE],
                       capture_output=True, text=True)
    if "function runCalculation" not in r.stdout:
        sys.exit(f"ABORT ({when}): runCalculation not found.")
    print(f"OK ({when}):", r.stdout.strip())

check_run_calc("before")

with open(FILE) as f:
    html = f.read()

# 1. Swap Reveal button onclick: runCalculation() -> handleRevealClick()
OLD_BTN = '<button class="calc-btn" style="margin-top:16px;margin-left:32px;margin-right:16px;width:calc(100% - 48px)" onclick="runCalculation()">Reveal My Cube</button>'
NEW_BTN = '''<button class="calc-btn" id="revealBtn" style="margin-top:16px;margin-left:32px;margin-right:16px;width:calc(100% - 48px)" onclick="handleRevealClick()">Reveal My Cube</button>
<p id="magicLinkBanner" style="display:none;margin:14px 32px 0 32px;padding:12px 16px;background:rgba(125,212,252,0.08);border:1px solid rgba(125,212,252,0.35);border-radius:8px;font-family:'Cormorant Garamond',serif;font-size:15px;color:#fff;text-align:center;line-height:1.4"></p>'''
assert html.count(OLD_BTN) == 1, "Reveal button anchor not found exactly once"
html = html.replace(OLD_BTN, NEW_BTN, 1)

# 2. Insert auth helpers + handleRevealClick right BEFORE function runCalculation()
OLD_RUN_CALC = 'function runCalculation(){'
NEW_BLOCK = '''// ═══ SUPABASE AUTH HELPERS ═══════════════════
const QC_PENDING_KEY = "qc_pending_profile_v1";
let qcCurrentUser = null;
let qcCurrentProfile = null;

function showMagicLinkBanner(msg){
  const el = document.getElementById("magicLinkBanner");
  if(!el) return;
  el.textContent = msg;
  el.style.display = "block";
}

function savePendingProfile(fn, mn, ln, d, m, y, em){
  try{
    localStorage.setItem(QC_PENDING_KEY, JSON.stringify({
      firstName:fn, middleName:mn, lastName:ln,
      dobDay:d, dobMonth:m, dobYear:y, email:em, t:Date.now()
    }));
  }catch(e){}
}

function restorePendingProfile(){
  try{
    const raw = localStorage.getItem(QC_PENDING_KEY);
    if(!raw) return;
    const p = JSON.parse(raw);
    const set = (id,v)=>{const el=document.getElementById(id);if(el&&v!=null)el.value=v;};
    set("firstName", p.firstName);
    set("middleName", p.middleName);
    set("lastName", p.lastName);
    set("dobDay", p.dobDay);
    set("dobMonth", p.dobMonth);
    set("dobYear", p.dobYear);
    set("email", p.email);
    if(typeof updateCalcBtnReady === "function") updateCalcBtnReady();
  }catch(e){}
}

async function handleRevealClick(){
  const fn = document.getElementById("firstName").value.trim();
  const mn = document.getElementById("middleName").value.trim();
  const ln = document.getElementById("lastName").value.trim();
  const em = document.getElementById("email").value.trim();
  const d  = document.getElementById("dobDay").value.trim();
  const m  = document.getElementById("dobMonth").value;
  const y  = document.getElementById("dobYear").value.trim();
  const consent = !!document.getElementById("marketingConsent")?.checked;
  const emOk = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(em);
  if(!(fn && ln && emOk && d && m && y)){
    const err = document.getElementById("errMsg");
    if(err) err.style.display = "block";
    return;
  }
  savePendingProfile(fn, mn, ln, d, m, y, em);
  const btn = document.getElementById("revealBtn");
  if(btn){ btn.disabled = true; btn.textContent = "Sending sign-in link..."; }
  try{
    const redirectTo = window.location.origin + window.location.pathname;
    const { error } = await sb.auth.signInWithOtp({
      email: em,
      options: { emailRedirectTo: redirectTo, data: { marketing_consent: consent } }
    });
    if(error){
      showMagicLinkBanner("Could not send sign-in link: " + error.message + ". You can still view your reading below.");
    }else{
      showMagicLinkBanner("Sign-in link sent to " + em + ". Click it to unlock your full cube — you can keep exploring while you wait.");
    }
  }catch(e){
    showMagicLinkBanner("Could not send sign-in link. You can still view your reading below.");
  }finally{
    if(btn){ btn.disabled = false; btn.textContent = "Reveal My Cube"; }
  }
  runCalculation();
}

async function initSupabaseSession(){
  try{
    const { data: { session } } = await sb.auth.getSession();
    if(session && session.user){
      qcCurrentUser = session.user;
      const { data: profile } = await sb.from("profiles").select("*").maybeSingle();
      qcCurrentProfile = profile || null;
      if(profile && profile.has_paid === true){
        if(typeof applyUnlockedState === "function") applyUnlockedState(false);
      }
      showMagicLinkBanner("Signed in as " + session.user.email + ".");
    }
  }catch(e){}
  restorePendingProfile();
}

sb.auth.onAuthStateChange((event, session) => {
  if(event === "SIGNED_IN" && session && session.user){
    qcCurrentUser = session.user;
    sb.from("profiles").select("*").maybeSingle().then(r => {
      qcCurrentProfile = r.data || null;
      if(qcCurrentProfile && qcCurrentProfile.has_paid === true){
        if(typeof applyUnlockedState === "function") applyUnlockedState(false);
      }
      showMagicLinkBanner("Signed in as " + session.user.email + ".");
    });
  }
  if(event === "SIGNED_OUT"){
    qcCurrentUser = null;
    qcCurrentProfile = null;
  }
});

document.addEventListener("DOMContentLoaded", () => { initSupabaseSession(); });

'''
assert html.count(OLD_RUN_CALC) == 1, "runCalculation anchor not found exactly once"
html = html.replace(OLD_RUN_CALC, NEW_BLOCK + OLD_RUN_CALC, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 3 applied: magic-link flow wired, session restore on load.")
