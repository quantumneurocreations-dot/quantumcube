import subprocess, sys

FILE = "/Users/qnc/Projects/quantumcube/quantum-cube-v10.html"

def check_run_calc(when):
    r = subprocess.run(["grep", "-n", "function runCalculation", FILE],
                       capture_output=True, text=True)
    if "function runCalculation" not in r.stdout:
        sys.exit(f"ABORT ({when}): runCalculation not found. git restore before proceeding.")
    print(f"OK ({when}):", r.stdout.strip())

check_run_calc("before")

with open(FILE) as f:
    html = f.read()

OLD_LAST_NAME = '<div class="form-group form-full" style="text-align:center"><label style="text-align:center;display:block">Last Name</label><input type="text" id="lastName" placeholder="" autocomplete="family-name" style="text-align:center"></div>'
NEW_LAST_NAME_BLOCK = OLD_LAST_NAME + '\n<div class="form-group form-full" style="text-align:center"><label style="text-align:center;display:block">Email</label><input type="email" id="email" placeholder="" autocomplete="email" inputmode="email" style="text-align:center"></div>'
assert html.count(OLD_LAST_NAME) == 1, "Last Name anchor not found exactly once"
html = html.replace(OLD_LAST_NAME, NEW_LAST_NAME_BLOCK, 1)

OLD_ERR = '<p class="err-msg" id="errMsg">Please complete all fields</p>\n</div>\n<button class="calc-btn" style="margin-top:16px;margin-left:32px;margin-right:16px;width:calc(100% - 48px)" onclick="runCalculation()">Reveal My Cube</button>'
NEW_ERR = '''<p class="err-msg" id="errMsg">Please complete all fields</p>
</div>
<label class="marketing-consent" style="display:flex;align-items:center;justify-content:center;gap:8px;margin:16px 32px 0 32px;font-family:'Cormorant Garamond',serif;font-size:16px;color:#fff;cursor:pointer;">
  <input type="checkbox" id="marketingConsent" style="width:18px;height:18px;cursor:pointer;accent-color:#7dd4fc;">
  <span>Email me updates about Quantum Cube</span>
</label>
<button class="calc-btn" style="margin-top:16px;margin-left:32px;margin-right:16px;width:calc(100% - 48px)" onclick="runCalculation()">Reveal My Cube</button>'''
assert html.count(OLD_ERR) == 1, "Reveal button anchor not found exactly once"
html = html.replace(OLD_ERR, NEW_ERR, 1)

OLD_READY = 'function updateCalcBtnReady(){var fn=document.getElementById("firstName").value.trim();var ln=document.getElementById("lastName").value.trim();var d=document.getElementById("dobDay").value.trim();var m=document.getElementById("dobMonth").value;var y=document.getElementById("dobYear").value.trim();var ok=!!(fn&&ln&&d&&m&&y);document.querySelectorAll(".calc-btn").forEach(function(b){b.classList.toggle("ready",ok);});}'
NEW_READY = 'function updateCalcBtnReady(){var fn=document.getElementById("firstName").value.trim();var ln=document.getElementById("lastName").value.trim();var em=document.getElementById("email")?document.getElementById("email").value.trim():"";var d=document.getElementById("dobDay").value.trim();var m=document.getElementById("dobMonth").value;var y=document.getElementById("dobYear").value.trim();var emOk=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(em);var ok=!!(fn&&ln&&emOk&&d&&m&&y);document.querySelectorAll(".calc-btn").forEach(function(b){b.classList.toggle("ready",ok);});}'
assert html.count(OLD_READY) == 1, "updateCalcBtnReady anchor not found exactly once"
html = html.replace(OLD_READY, NEW_READY, 1)

OLD_LISTENERS = '["firstName","lastName","dobDay","dobYear"].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener("input",updateCalcBtnReady);});'
NEW_LISTENERS = '["firstName","lastName","email","dobDay","dobYear"].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener("input",updateCalcBtnReady);});'
assert html.count(OLD_LISTENERS) == 1, "DOMContentLoaded listener anchor not found exactly once"
html = html.replace(OLD_LISTENERS, NEW_LISTENERS, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 2 applied: email field + marketing consent added to Face 0 form.")
