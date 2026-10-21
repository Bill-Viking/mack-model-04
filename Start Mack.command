#!/bin/zsh
# Double-click in Finder. No dependency installation or Apple software needed.
cd -- "${0:A:h}" || exit 1
exec python3 tools/serve_desktop.py
