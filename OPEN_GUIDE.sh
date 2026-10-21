#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$HERE/index.html"
else
  echo "[HELP] Open this local browser page: $HERE/index.html"
fi
