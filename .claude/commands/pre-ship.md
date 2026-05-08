Run the pre-ship verification checklist before committing any changes to docs/app.html or docs/sw.js.

1. Check version sync:
```bash
SW_VER=$(grep -oE "qc-v[0-9]+" docs/sw.js | head -1)
APP_VER=$(grep -oE "quantum-cube@qc-v[0-9]+" docs/app.html | head -1 | sed 's/quantum-cube@//')
echo "SW: $SW_VER  APP: $APP_VER"
[ "$SW_VER" = "$APP_VER" ] && echo "VERSIONS IN SYNC ✓" || echo "MISMATCH — bump version before shipping"
```

2. Verify runCalculation anchor is present:
```bash
grep -c "function runCalculation" docs/app.html
```
Must return 1. If 0, the edit broke the function — revert and investigate.

3. Check for uncommitted changes:
```bash
git diff --stat
git status --short
```

Report findings. If everything passes: "Safe to commit." If anything fails: "BLOCKED — fix [issue] before committing."
