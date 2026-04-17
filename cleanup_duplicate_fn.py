import subprocess, sys, shutil, datetime

FILE = "/Users/qnc/Projects/quantumcube/quantum-cube-v10.html"

def check_run_calc(when):
    r = subprocess.run(["grep", "-n", "function runCalculation", FILE],
                       capture_output=True, text=True)
    if "function runCalculation" not in r.stdout:
        sys.exit(f"ABORT ({when}): runCalculation not found. git restore before proceeding.")
    print(f"OK ({when}):", r.stdout.strip())

check_run_calc("before")

stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
backup = FILE + f".bak-cleanup-{stamp}"
shutil.copyfile(FILE, backup)
print(f"Backup: {backup}")

with open(FILE) as f:
    html = f.read()

VIMEO_BROKEN = '''<script src="https://player.vimeo.com/api/player.js">function updateCalcBtnReady(){var fn=document.getElementById("firstName").value.trim();var ln=document.getElementById("lastName").value.trim();var d=document.getElementById("dobDay").value.trim();var m=document.getElementById("dobMonth").value;var y=document.getElementById("dobYear").value.trim();var ok=!!(fn&&ln&&d&&m&&y);document.querySelectorAll(".calc-btn").forEach(function(b){b.classList.toggle("ready",ok);});}
document.addEventListener("DOMContentLoaded",function(){["firstName","lastName","dobDay","dobYear"].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener("input",updateCalcBtnReady);});var dm=document.getElementById("dobMonth");if(dm)dm.addEventListener("change",updateCalcBtnReady);});
</script>'''
VIMEO_FIXED = '<script src="https://player.vimeo.com/api/player.js"></script>'

assert html.count(VIMEO_BROKEN) == 1, "Vimeo broken block not found exactly once"
html = html.replace(VIMEO_BROKEN, VIMEO_FIXED, 1)
print("Removed dead copy at line ~429 (inside Vimeo script tag).")

DUPE_TAIL = '''}
function updateCalcBtnReady(){var fn=document.getElementById("firstName").value.trim();var ln=document.getElementById("lastName").value.trim();var d=document.getElementById("dobDay").value.trim();var m=document.getElementById("dobMonth").value;var y=document.getElementById("dobYear").value.trim();var ok=!!(fn&&ln&&d&&m&&y);document.querySelectorAll(".calc-btn").forEach(function(b){b.classList.toggle("ready",ok);});}
document.addEventListener("DOMContentLoaded",function(){["firstName","lastName","dobDay","dobYear"].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener("input",updateCalcBtnReady);});var dm=document.getElementById("dobMonth");if(dm)dm.addEventListener("change",updateCalcBtnReady);});
</script>'''
DUPE_TAIL_FIXED = '''}
</script>'''

assert html.count(DUPE_TAIL) == 1, "Duplicate tail block not found exactly once"
html = html.replace(DUPE_TAIL, DUPE_TAIL_FIXED, 1)
print("Removed duplicate at line ~2323 (tail of main script).")

remaining = html.count("function updateCalcBtnReady")
assert remaining == 1, f"Expected 1 copy of updateCalcBtnReady, found {remaining}"
print(f"Final count of updateCalcBtnReady: {remaining} (correct).")

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Cleanup complete.")
