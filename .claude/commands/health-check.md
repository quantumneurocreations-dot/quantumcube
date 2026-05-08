Run the Quantum Cube health check and report the results inline.

Execute this bash sequence:
```bash
cd /Users/qnc/Projects/quantumcube
git branch --show-current
git status --short
git log --oneline -3
echo "--- version sync ---"
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
echo "SW: $SW_VER  APP: $APP_VER  $([ "$SW_VER" = "$APP_VER" ] && echo "OK" || echo "MISMATCH — fix before shipping")"
echo "--- runCalculation anchor ---"
grep -c "function runCalculation" docs/app.html
echo "--- live vs repo ---"
curl -s https://quantumcube.app/sw.js | grep -oE "qc-v[0-9]+" | head -1
echo "--- origin sync ---"
git log origin/main..HEAD --oneline 2>/dev/null || true
```

Report: branch, tree state, last 3 commits, version sync status, runCalculation presence (must be 1), live SW version vs repo, any unpushed commits.
