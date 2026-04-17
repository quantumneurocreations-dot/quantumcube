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

CONSENT_CSS = '''
.marketing-consent{display:flex;align-items:center;justify-content:center;gap:10px;margin:18px 32px 0 32px;font-family:'Cormorant Garamond',serif;font-size:15px;color:var(--text);cursor:pointer;user-select:none;transition:color 0.2s ease}
.marketing-consent input[type="checkbox"]{position:absolute;opacity:0;pointer-events:none;width:0;height:0}
.consent-box{display:inline-block;width:20px;height:20px;border:1.5px solid rgba(255,255,255,0.4);border-radius:4px;background:rgba(255,255,255,0.04);position:relative;transition:all 0.2s ease;flex-shrink:0}
.marketing-consent input[type="checkbox"]:checked ~ .consent-box{border-color:var(--glow);background:rgba(125,212,252,0.15);box-shadow:0 0 12px rgba(125,212,252,0.55),inset 0 0 6px rgba(125,212,252,0.2)}
.marketing-consent input[type="checkbox"]:checked ~ .consent-box::after{content:"";position:absolute;top:2px;left:6px;width:5px;height:10px;border:solid var(--glow);border-width:0 2px 2px 0;transform:rotate(45deg)}
.marketing-consent:hover .consent-box{border-color:rgba(255,255,255,0.65)}
.marketing-consent:hover input[type="checkbox"]:checked ~ .consent-box{border-color:var(--glow-b);box-shadow:0 0 16px rgba(125,212,252,0.75),inset 0 0 8px rgba(125,212,252,0.25)}
'''

STYLE_CLOSE = "</style>"
count = html.count(STYLE_CLOSE)
assert count == 1, f"Expected exactly one </style>, found {count}"
html = html.replace(STYLE_CLOSE, CONSENT_CSS + STYLE_CLOSE, 1)

OLD_LABEL = '''<label class="marketing-consent" style="display:flex;align-items:center;justify-content:center;gap:8px;margin:16px 32px 0 32px;font-family:'Cormorant Garamond',serif;font-size:16px;color:#fff;cursor:pointer;">
  <input type="checkbox" id="marketingConsent" style="width:18px;height:18px;cursor:pointer;accent-color:#7dd4fc;">
  <span>Email me updates about Quantum Cube</span>
</label>'''

NEW_LABEL = '''<label class="marketing-consent">
  <input type="checkbox" id="marketingConsent">
  <span class="consent-box"></span>
  <span>Email me updates about Quantum Cube</span>
</label>'''

assert html.count(OLD_LABEL) == 1, "Marketing consent label anchor not found exactly once"
html = html.replace(OLD_LABEL, NEW_LABEL, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 2b applied: custom cyan-glow checkbox styling.")
