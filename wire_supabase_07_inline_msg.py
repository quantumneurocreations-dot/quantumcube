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

# 1. Add CSS: bigger .err-msg styling + new .err-msg.success variant for bright cyan
MSG_CSS = '''
.err-msg{display:none;text-align:center;width:100%;padding:6px 12px;font-family:'Cinzel',serif;font-size:15px;letter-spacing:2px;font-style:normal;color:#ff8fa3;text-shadow:0 0 6px rgba(255,143,163,0.4);text-transform:uppercase}
.err-msg.success{color:var(--glow);text-shadow:0 0 10px rgba(125,212,252,0.7),0 0 18px rgba(125,212,252,0.35)}
'''
STYLE_CLOSE = "</style>"
count = html.count(STYLE_CLOSE)
assert count == 1, f"Expected exactly one </style>, found {count}"
html = html.replace(STYLE_CLOSE, MSG_CSS + STYLE_CLOSE, 1)

# 2. Remove the separate cyan banner card element (#magicLinkBanner)
OLD_BANNER = '<p id="magicLinkBanner" style="display:none;margin:14px 32px 0 32px;padding:12px 16px;background:rgba(125,212,252,0.08);border:1px solid rgba(125,212,252,0.35);border-radius:8px;font-family:\'Cormorant Garamond\',serif;font-size:15px;color:#fff;text-align:center;line-height:1.4"></p>'
assert html.count(OLD_BANNER) == 1, "magicLinkBanner anchor not found exactly once"
html = html.replace(OLD_BANNER, "", 1)

# 3. Rewrite handleRevealClick body — use errMsg slot, 3s/3s/rotate sequence
OLD_HANDLER = '''  savePendingProfile(fn, mn, ln, d, m, y, em);
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

NEW_HANDLER = '''  savePendingProfile(fn, mn, ln, d, m, y, em);
  const btn = document.getElementById("revealBtn");
  const err = document.getElementById("errMsg");
  if(btn){ btn.disabled = true; btn.textContent = "SENDING"; }
  if(err){
    err.textContent = "Verify your email";
    err.classList.add("success");
    err.style.display = "block";
  }
  let sendOk = false;
  let errorText = "";
  try{
    const redirectTo = window.location.origin + window.location.pathname;
    const { error } = await sb.auth.signInWithOtp({
      email: em,
      options: { emailRedirectTo: redirectTo, data: { marketing_consent: consent } }
    });
    if(error){
      errorText = error.message;
    }else{
      sendOk = true;
    }
  }catch(e){
    errorText = (e && e.message) ? e.message : "Network error";
  }
  if(sendOk){
    // 3 seconds SENDING, then 3 seconds EMAIL SENT, then rotate.
    setTimeout(() => {
      if(btn){ btn.textContent = "EMAIL SENT"; }
    }, 3000);
    setTimeout(() => {
      if(btn){ btn.disabled = false; btn.textContent = "Reveal My Cube"; }
      if(err){
        err.classList.remove("success");
        err.textContent = "Please complete all fields";
        err.style.display = "none";
      }
      runCalculation();
    }, 6000);
  }else{
    // Revert button + error styling, surface the problem, stay on Face 0
    if(btn){ btn.disabled = false; btn.textContent = "Reveal My Cube"; }
    if(err){
      err.classList.remove("success");
      err.textContent = errorText ? ("Could not send: " + errorText) : "Could not send sign-in link";
      err.style.display = "block";
    }
    runCalculation();
  }
}'''

assert html.count(OLD_HANDLER) == 1, "handleRevealClick body anchor not found exactly once"
html = html.replace(OLD_HANDLER, NEW_HANDLER, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 7 applied: banner removed, errMsg reused with bright-cyan success variant, 3s+3s sequence.")
