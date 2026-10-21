#!/usr/bin/env bash
# Genuine adapter to the user's separately installed HEXBAZAAR v0.1.2-rc1.
# No saved report unless the underlying user explicitly invokes --out themselves.
set -euo pipefail
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
USER_LAUNCHERS="$HOME/PhantomLabsLaunchers"
ENGINE=""
for root in   "$USER_LAUNCHERS/hexbazaar-savage-intel-shop-v0_1_2_rc1_rosie_savage"   "$USER_LAUNCHERS/hexbazaar-savage-intel-shop-v0_1_2_rc1_rosie_facebook_recipes"; do
  if [ -f "$root/hexbazaar_savage_intel_shop_v0_1_2_rc1.py" ]; then
    ENGINE="$root/hexbazaar_savage_intel_shop_v0_1_2_rc1.py"
    break
  fi
done
mode="${1:-help}"
if [[ "$mode" == "guide" ]]; then
  bash "$SELF_DIR/OPEN_GUIDE.sh"
  exit $?
fi
if [[ "$mode" == "help" || "$mode" == "--help" ]]; then
  cat <<'HELP'
HEXBAZAAR LIVE COMMAND DECK v0.1.0
  start     real public DNS of example.com
  easy      real public DNS of facebook.com
  medium    real DNS + RIPEstat of example.com
  savage    real 4-provider public research of facebook.com
  shop      list actual installed HEXBAZAAR engine modules (offline)
  check     verify path and display actual engine --help (offline)
  guide     open local HTML recipes, no internet until you run a live command
  help      display these commands
No mock observations. No automatic report saving.
HELP
  exit 0
fi
if [[ -z "$ENGINE" ]]; then
  echo '[ERROR] HEXBAZAAR v0.1.2-rc1 engine not found in known versioned installation folders.' >&2
  echo '[HELP] Keep existing files intact; install the original HEXBAZAAR engine before running the Deck.' >&2
  exit 3
fi
case "$mode" in
  check)
    printf '[FOUND] Real HEXBAZAAR engine: %s\n' "$ENGINE"
    exec python3 -B "$ENGINE" --help
    ;;
  shop)
    exec python3 -B "$ENGINE" --color always shop
    ;;
  start)
    echo '[LIVE] HEXBAZAAR public DNS • example.com • real provider responses only'
    exec python3 -B "$ENGINE" --color always domain example.com --live --providers dns --timeout 4 --limit 15
    ;;
  easy)
    echo '[LIVE] HEXBAZAAR public DNS • facebook.com • real provider responses only'
    exec python3 -B "$ENGINE" --color always domain facebook.com --live --providers dns --timeout 4 --limit 10
    ;;
  medium)
    echo '[LIVE] HEXBAZAAR public DNS + RIPEstat • example.com'
    exec python3 -B "$ENGINE" --color always domain example.com --live --providers dns,ripe --view full --limit 50 --timeout 4 --delay 0
    ;;
  savage)
    echo '[LIVE] HEXBAZAAR 4 passive public providers • facebook.com'
    exec python3 -B "$ENGINE" --color always domain facebook.com --live --providers dns,ripe,certspotter,urlscan --view full --limit 200 --timeout 4 --delay 1
    ;;
  *)
    echo "[ERROR] Unknown command: $mode; run help" >&2
    exit 2
    ;;
esac
