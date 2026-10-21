#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
[ -f "$HERE/index.html" ] && [ -f "$HERE/RUN_HEXBAZAAR_LIVE.sh" ] || { echo '[ERROR] Missing Deck files' >&2; exit 2; }
mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
BIN="$HOME/.local/bin/hexbazaar-live-deck"
if [ ! -e "$BIN" ] && [ ! -L "$BIN" ]; then
  cat > "$BIN" <<EOF
#!/usr/bin/env bash
exec /bin/bash "$HERE/RUN_HEXBAZAAR_LIVE.sh" "\$@"
EOF
  chmod 755 "$BIN"
  echo '[PASS] Short command created: hexbazaar-live-deck'
else
  echo '[NOTICE] Existing short command preserved; no overwrite.'
fi
MENU="$HOME/.local/share/applications/hexbazaar-live-command-deck-v1.desktop"
if [ ! -e "$MENU" ] && [ ! -L "$MENU" ]; then
cat > "$MENU" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=HEXBAZAAR Live Command Deck v1
Comment=Real live public-domain research recipes and launcher
Exec=/bin/bash "$HERE/OPEN_GUIDE.sh"
Icon=$HERE/assets/favicon.png
Terminal=false
Categories=Utility;Education;
EOF
chmod 644 "$MENU"
fi
DESKTOP="$HOME/Desktop"
if command -v xdg-user-dir >/dev/null 2>&1; then DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")"; fi
if [ "$DESKTOP" = "$HOME" ] || [ -z "$DESKTOP" ]; then DESKTOP="$HOME/Desktop"; fi
mkdir -p "$DESKTOP"
SHORT="$DESKTOP/HEXBAZAAR-Live-Command-Deck-v1.desktop"
if [ ! -e "$SHORT" ] && [ ! -L "$SHORT" ]; then
  cp "$MENU" "$SHORT"
  chmod 755 "$SHORT"
  if command -v gio >/dev/null 2>&1; then gio set "$SHORT" metadata::trusted true >/dev/null 2>&1 || true; fi
  echo '[PASS] Independent desktop icon created'
else
  echo '[NOTICE] Existing desktop icon preserved'
fi
printf '[DONE] HEXBAZAAR Live Deck installed separately; original engines, tools and hub unchanged.\n'
