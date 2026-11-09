#!/bin/bash
# The CI's check of urls.py (job `urls` in ../../.gitlab-ci.yml), the same run locally: the case file's four BAD lines
# are flagged, nothing else (comments, verbatim, \verb and the right forms stay quiet).
set -uo pipefail
cd "$(dirname "$0")"
out=$(python3 ../urls.py urls/case.tex); rc=$?
got=$(grep -c ': ' <<<"$(grep -v '^---' <<<"$out")")
want=$(grep -c '% BAD' urls/case.tex)
echo "$out"
[[ $rc -eq 1 && $got -eq $want ]] || { echo "urls-test: flagged $got, expected $want (exit $rc)"; exit 1; }
echo "urls-test: $got of $want flagged, as expected"
