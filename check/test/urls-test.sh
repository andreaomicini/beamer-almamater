#!/bin/bash
# The CI's check of urls.py (job `urls` in ../../.gitlab-ci.yml), the same run locally: the case file's BAD lines
# are flagged, nothing else (comments, verbatim, \verb and the right forms stay quiet).
set -uo pipefail
cd "$(dirname "$0")"
out=$(python3 ../urls.py urls/case.tex); rc=$?
got=$(grep -c ': ' <<<"$(grep -v '^---' <<<"$out")")
want=$(grep -c '% BAD' urls/case.tex)
echo "$out"
[[ $rc -eq 1 && $got -eq $want ]] || { echo "urls-test: flagged $got, expected $want (exit $rc)"; exit 1; }
# --fix leaves every line's braces as they were, and nothing to flag after it
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT; cp urls/case.tex "$w/case.tex"
python3 ../urls.py --fix "$w/case.tex" > /dev/null || { echo "urls-test: --fix failed"; exit 1; }
python3 ../urls.py "$w/case.tex" > /dev/null || { echo "urls-test: --fix left addresses to flag"; exit 1; }
grep -q 'newcommand{\\mailbad}\[1\]{\\umail{#1}} %' "$w/case.tex" || { echo "urls-test: --fix broke the nested mailto"; exit 1; }
echo "urls-test: $got of $want flagged, as expected; --fix rewrites them, braces intact"
