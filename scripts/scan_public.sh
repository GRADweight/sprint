# Public-Scan / Preismaterial-Wächter — nur Public-Material.
# Der CI-Scanner selbst (mit Begriffsliste) ist ausgeschlossen, er ist die
# Definition, nicht ein Vorkommen.
#!/usr/bin/env bash
set -euo pipefail
HIT=0
grep -rniE "(\bCHF\b|[0-9]{3,}\.[0-9]{2}|kalkulation|marge|preismaterial|preisstrat|/Users/|~/code|eddvv)" \
  --include="*.md" --include="*.py" --include="*.toml" \
  --exclude-dir=.venv --exclude-dir=.git --exclude=ci.yml . 2>/dev/null || true
echo "--- ergebnis oben leer = sauber ---"
