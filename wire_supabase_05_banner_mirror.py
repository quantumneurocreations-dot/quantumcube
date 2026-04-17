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

OLD_HANDLER = '''  savePendingProfile(fn, mn, ln, d, m, y, em);
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
}'''

NEW_HANDLER = '''  savePendingProfile(fn, mn, ln, d, m, y, em);
  const btn = document.getElementById("revealBtn");
  if(btn){ btn.disabled = true; btn.textContent = "Sending sign-in link..."; }
  let sendOk = false;
  let bannerMsg = "";
  try{
    const redirectTo = window.location.origin + window.location.pathname;
    const { error } = await sb.auth.signInWithOtp({
      email: em,
      options: { emailRedirectTo: redirectTo, data: { marketing_consent: consent } }
    });
    if(error){
      bannerMsg = "Could not send sign-in link: " + error.message + ". You can still continue and view the free content.";
    }else{
      sendOk = true;
      bannerMsg = "Check your inbox. Verify your email — you can start exploring while you wait.";
    }
  }catch(e){
    bannerMsg = "Could not send sign-in link. You can still continue and view the free content.";
  }finally{
    if(btn){ btn.disabled = false; btn.textContent = "Reveal My Cube"; }
  }
  showMagicLinkBanner(bannerMsg);
  if(sendOk){
    runCountdownThenReveal(3);
  }else{
    runCalculation();
  }
}

function runCountdownThenReveal(seconds){
  const el = document.getElementById("magicLinkBanner");
  const baseMsg = el ? el.textContent : "";
  let remaining = seconds;
  const tick = () => {
    if(el) el.textContent = baseMsg + " Continuing in " + remaining + "...";
    if(remaining <= 0){
      runCalculation();
      return;
    }
    remaining -= 1;
    setTimeout(tick, 1000);
  };
  tick();
}

function syncMarketingConsent(source){
  const all = document.querySelectorAll("input.qc-consent-checkbox");
  const val = !!source.checked;
  all.forEach(cb => { if(cb !== source) cb.checked = val; });
}'''

assert html.count(OLD_HANDLER) == 1, "handleRevealClick body anchor not found exactly once"
html = html.replace(OLD_HANDLER, NEW_HANDLER, 1)

OLD_FACE0_CHECKBOX = '<input type="checkbox" id="marketingConsent">'
NEW_FACE0_CHECKBOX = '<input type="checkbox" id="marketingConsent" class="qc-consent-checkbox" onchange="syncMarketingConsent(this)">'
assert html.count(OLD_FACE0_CHECKBOX) == 1, "Face 0 checkbox anchor not found exactly once"
html = html.replace(OLD_FACE0_CHECKBOX, NEW_FACE0_CHECKBOX, 1)

LOCK_CONSENT_LABEL = '''<button class="unlock-btn" onclick="unlock()">Unlock</button>
<label class="marketing-consent" style="margin-top:14px">
  <input type="checkbox" class="qc-consent-checkbox" onchange="syncMarketingConsent(this)">
  <span class="consent-box"></span>
  <span>Email me updates about Quantum Cube</span>
</label>
<button class="demo-btn" onclick="unlockDemo()">Try Demo (test mode)</button>'''

OLD_LOCK_BLOCK = '''<button class="unlock-btn" onclick="unlock()">Unlock</button>
<button class="demo-btn" onclick="unlockDemo()">Try Demo (test mode)</button>'''

count = html.count(OLD_LOCK_BLOCK)
assert count == 4, f"Expected 4 lock-card unlock blocks, found {count}"
html = html.replace(OLD_LOCK_BLOCK, LOCK_CONSENT_LABEL)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 5 applied: new banner copy + 3s countdown + mirrored consent on 4 lock cards.")
