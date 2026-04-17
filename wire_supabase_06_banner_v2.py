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

OLD_BLOCK = '''  savePendingProfile(fn, mn, ln, d, m, y, em);
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
}'''

NEW_BLOCK = '''  savePendingProfile(fn, mn, ln, d, m, y, em);
  const btn = document.getElementById("revealBtn");
  if(btn){ btn.disabled = true; btn.textContent = "Sending..."; }
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
      bannerMsg = "Verify your email";
    }
  }catch(e){
    bannerMsg = "Could not send sign-in link. You can still continue and view the free content.";
  }
  showMagicLinkBanner(bannerMsg);
  if(sendOk){
    // Stage 1: banner shows "Verify your email", button still says "Sending..." (2 seconds)
    // Stage 2: banner still shows "Verify your email", button switches to "Check your inbox" (2 seconds)
    // Then rotate to Face 1.
    setTimeout(() => {
      if(btn){ btn.textContent = "Check your inbox"; }
    }, 2000);
    setTimeout(() => {
      if(btn){ btn.disabled = false; btn.textContent = "Reveal My Cube"; }
      runCalculation();
    }, 4000);
  }else{
    if(btn){ btn.disabled = false; btn.textContent = "Reveal My Cube"; }
    runCalculation();
  }
}'''

assert html.count(OLD_BLOCK) == 1, "Old Chunk 5 banner/countdown block not found exactly once"
html = html.replace(OLD_BLOCK, NEW_BLOCK, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 6 applied: two-stage banner flow — banner + button coordinate, no countdown.")
