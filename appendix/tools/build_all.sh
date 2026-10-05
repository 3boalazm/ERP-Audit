#!/bin/sh
# Order matters: gen_brga2/gen_dar import gen_brga (which regenerates 21-29), so render diagrams last.
set -e
cd /home/claude/audit
python3 tools/gen_findings.py >/dev/null
python3 tools/gen_brga2.py >/dev/null
python3 tools/gen_dar.py
python3 tools/render_brga.py
python3 tools/build_viewer.py
