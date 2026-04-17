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

OLD_CHECK = '''function checkStoredUnlock(){
  try{
    const stored = localStorage.getItem(STORE_KEY);
    if(stored === "1"){
      isUnlocked = true;
      // Silently unlock cube faces (no success screen on return visit)
      applyUnlockedState(false);
    }
  }catch(e){}
}'''

NEW_CHECK = '''function checkStoredUnlock(){
  try{
    const stored = localStorage.getItem(STORE_KEY);
    if(stored === "1"){
      isUnlocked = true;
      applyUnlockedState(false);
    }
  }catch(e){}
}

function syncUnlockFromProfile(profile){
  const paid = !!(profile && profile.has_paid === true);
  if(paid){
    if(!isUnlocked){
      applyUnlockedState(false);
    }else{
      try{localStorage.setItem(STORE_KEY,"1");}catch(e){}
    }
  }else{
    try{localStorage.removeItem(STORE_KEY);}catch(e){}
    if(isUnlocked){
      isUnlocked = false;
      document.querySelectorAll(".lock-screen").forEach(el=>el.style.display="block");
      ["face3-content","face4-content","face5-content","face6-content"].forEach(id=>{
        const el=document.getElementById(id);if(el)el.style.display="none";
      });
      document.querySelectorAll(".lock-footer").forEach(el=>el.style.display="");
      ["lock3","lock4","lock5","lock6"].forEach(id=>{
        const el=document.getElementById(id);if(el)el.style.display="block";
      });
      [2,3,4,5].forEach(n=>{
        const faceEl=document.querySelectorAll(".cube-face")[n];
        if(faceEl)faceEl.classList.add("locked");
      });
    }
  }
}'''

assert html.count(OLD_CHECK) == 1, "checkStoredUnlock anchor not found exactly once"
html = html.replace(OLD_CHECK, NEW_CHECK, 1)

OLD_INIT = '''async function initSupabaseSession(){
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
}'''

NEW_INIT = '''async function initSupabaseSession(){
  try{
    const { data: { session } } = await sb.auth.getSession();
    if(session && session.user){
      qcCurrentUser = session.user;
      const { data: profile } = await sb.from("profiles").select("*").maybeSingle();
      qcCurrentProfile = profile || null;
      syncUnlockFromProfile(profile);
      showMagicLinkBanner("Signed in as " + session.user.email + ".");
    }
  }catch(e){}
  restorePendingProfile();
}'''

assert html.count(OLD_INIT) == 1, "initSupabaseSession anchor not found exactly once"
html = html.replace(OLD_INIT, NEW_INIT, 1)

OLD_LISTENER = '''sb.auth.onAuthStateChange((event, session) => {
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
});'''

NEW_LISTENER = '''sb.auth.onAuthStateChange((event, session) => {
  if(event === "SIGNED_IN" && session && session.user){
    qcCurrentUser = session.user;
    sb.from("profiles").select("*").maybeSingle().then(r => {
      qcCurrentProfile = r.data || null;
      syncUnlockFromProfile(qcCurrentProfile);
      showMagicLinkBanner("Signed in as " + session.user.email + ".");
    });
  }
  if(event === "SIGNED_OUT"){
    qcCurrentUser = null;
    qcCurrentProfile = null;
  }
});'''

assert html.count(OLD_LISTENER) == 1, "onAuthStateChange anchor not found exactly once"
html = html.replace(OLD_LISTENER, NEW_LISTENER, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 4 applied.")
