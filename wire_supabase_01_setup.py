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

OLD_STRAY = '><link rel="preload" href="https://quantumneurocreations-dot.github.io/quantumcube/cube-background.jpg" as="image">'
NEW_STRAY = '<link rel="preload" href="https://quantumneurocreations-dot.github.io/quantumcube/cube-background.jpg" as="image">'
assert OLD_STRAY in html, "Stray '>' anchor not found (already fixed?)"
html = html.replace(OLD_STRAY, NEW_STRAY, 1)

SUPABASE_BLOCK = '''
<!-- Supabase JS SDK + client init -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"></script>
<script>
const SUPABASE_URL = "https://fqqdldvnxupzxvvbyvjm.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_wp2cRcjgyJcarRVuq_Q1zw_Vd68AEcZ";
const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    flowType: "implicit"
  }
});
</script>
'''

HEAD_CLOSE = "</head>"
assert html.count(HEAD_CLOSE) == 1, "Expected exactly one </head>"
html = html.replace(HEAD_CLOSE, SUPABASE_BLOCK + "\n" + HEAD_CLOSE, 1)

with open(FILE, "w") as f:
    f.write(html)

check_run_calc("after")
print("Chunk 1 applied: stray '>' fixed, Supabase SDK loaded, client 'sb' initialised.")
