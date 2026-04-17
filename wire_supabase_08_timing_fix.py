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

NEW_HANDLER = '''  savePendingProfile(fn, mn, ln, d, m, y, em);
  const btn = document.getElementById("revealBtn");
  const err = document.getElementById("errMsg");

  // Stage 0: start choreography IMMEDIATELY so user sees 3s SENDING + 3s EMAIL SENT
  // The API call runs in parallel in the background.
  if(btn){ btn.disabled = true; btn.textContent = "SENDING"; }
  if(err){
    err.textContent = "Verify your email";
    err.classList.add("success");
    err.style.display = "block";
  }

  // Kick off the API call without awaiting — we race it with the animation.
  const redirectTo = window.location.origin + window.location.pathname;
  const sendPromise = sb.auth.signInWithOtp({
    email: em,
    options: { emailRedirectTo: redirectTo, data: { marketing_consent: consent } }
  }).catch(e => ({ error: { message: (e && e.message) ? e.message : "Network error" } }));

  // 3 seconds SENDING → flip to EMAIL SENT
  setTimeout(() => {
    if(btn){ btn.textContent = "EMAIL SENT"; }
  }, 3000);

  // 6 seconds total → check whether the API actually succeeded, then act.
  setTimeout(async () => {
    const result = await sendPromise;
    const hadError = !!(result && result.error);
    if(btn){ btn.disabled = false; btn.textContent = "Reveal My Cube"; }
    if(err){
      err.classList.remove("success");
      err.textContent = "Please complete all fields";
      err.style.display = "none";
    }
    if(hadError){
      // Abort face rotate; surface the error on Face 0
      if(err){
        err.textContent = "Could not send: " + (result.error.message || "unknown error");
        err.style.display = "block";
      }
      return;
    }
    runCalculation();
  }, 6000);
}'''

assert html.count(OLD_HANDLER) == 1, "handleRevealClick body anchor not found exactly once"
html = html.replace(OLD_HANDLER, NEW_HANDLER, 1)

# Strip dead showMagicLinkBanner calls from init + onAuthStateChange
OLD_INIT_BANNER = '      showMagicLinkBanner("Signed in as " + session.user.email + ".");\n    }\n  }catch(e){}'
NEW_INIT_BANNER = '    }\n  }catch(e){}'
assert html.count(OLD_INIT_BANNER) == 1, "init showMagicLinkBanner anchor not found exactly once"
html = html.replace(OLD_INIT_BANNER, NEW_INIT_BANNER, 1)

OLD_LISTENER_BANNER = '      syncUnlockFromProfile(qcCurrentProfile);\n      showMagicLinkBanner("Signed in as " + session.user.email + ".");\n    });'
NEW_LISTENER_BANNER = '      syncUnlockFromProfile(qcCurrentProfile);\n    });'
assert html.count(OLD_LISTENER_BANNER) == 1, "listener showMagicLinkBanner anchor not found exactly once"
html = html.replace(OLD_LISTENER_BANNER, NEW_LISTENER_BANNER, 1)

# Strengthen errMsg centering: add margin auto + block display for layout certainty
OLD_CSS = ".err-msg{display:none;text-align:center;width:100%;padding:6px 12px;font-family:'Cinzel',serif;font-size:15px;letter-spacing:2px;font-style:normal;color:#ff8fa3;text-shadow:0 0 6px rgba(255,143,163,0.4);text-transform:uppercase}"
NEW_CSS = ".err-msg{display:none;text-align:center;width:100%;margin:12px auto 6px auto;padding:6px 12px;font-family:'Cinzel',serif;font-size:15px;letter-spacing:2px;font-style:normal;color:#ff8fa3;text-shadow:0 0 6px rgba(255,143,163,0.4);text-transform:uppercase}"
assert html.count(OLD_CSS) == 1, "err-msg CSS anchor not found exactly once"
html = html.replace(OLD_CSS, NEW_CSS, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 8 applied: timing starts immediately, dead banner calls removed, centering strengthened.")
