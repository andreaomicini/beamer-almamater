#!/bin/bash
# zip.sh [<deck>] -- the deck as one flat folder, zipped to zip/<deck>.zip
# run from the deck's root; <deck> may be omitted when tex/ holds a single .tex
set -euo pipefail

die() { echo "zip.sh: $*" >&2; exit 1; }

[ -f .latexmkrc ] && [ -d tex ] || die "run from the root of a deck repository"
if [ $# -ge 1 ]; then
	deck=$(basename "$1" .tex)
else
	set -- tex/*.tex
	[ $# -eq 1 ] && [ -e "$1" ] || die "tex/ holds $# .tex files: name the deck"
	deck=$(basename "$1" .tex)
fi
[ -f "tex/$deck.tex" ] || die "no tex/$deck.tex"
git check-ignore -q zip/ 2>/dev/null || echo "zip.sh: warning: zip/ is not gitignored here" >&2

## build, so that aux/ lists what the deck reads now
latexmk -pdf "tex/$deck.tex" >/dev/null 2>&1 || die "the deck does not build: see aux/$deck.log"

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
dir="$work/$deck"
mkdir -p "$dir" "$work/texmf"

## the .tex without its TeXShop magic comments
grep -v '^% *!TEX' "tex/$deck.tex" > "$dir/$deck.tex"

## every project file the build read, symlinks resolved
put() {
	local n
	n=$(basename "$1")
	if [ -e "$dir/$n" ]; then
		cmp -s "$1" "$dir/$n" || die "two different files named $n"
	else
		cp -L "$1" "$dir/"
	fi
}
## one name per line, read whole: a name may hold spaces
grep '^INPUT ' "aux/$deck.fls" | cut -c7- | sed 's|^\./||' | sort -u |
	grep -v -e '^/' -e '^aux/' -e "^tex/$deck.tex\$" | while IFS= read -r f; do
	put "$f"
done

## bibtex's inputs, which the .fls does not see: found by name anywhere in the repository
find_one() {
	local hits
	hits=$(find . \( -path ./aux -o -path ./pdf -o -path ./src -o -path ./zip -o -path ./.git \) -prune \
		-o -name "$1" -print)
	[ -n "$hits" ] || die "$1 not found in the repository"
	for h in $hits; do put "$h"; done
}
## the deck's own <deck>.bib, never the shared one whole (Andrea, 2026-11-09): from the .bib files the deck reads, the
## entries it cites, their crossref parents (to any depth) and the @strings they use; the flat copy reads {<deck>}
bibs=$(sed -n 's/^\\bibdata{\(.*\)}$/\1/p' "aux/$deck.aux" | tr , ' ')
if [ -n "$bibs" ]; then
	srcs=()
	for b in $bibs; do
		h=$(find . \( -path ./aux -o -path ./pdf -o -path ./src -o -path ./zip -o -path ./.git \) -prune -o -name "$b.bib" -print | head -1)
		[ -n "$h" ] || die "$b.bib not found in the repository"
		srcs+=("$h")
	done
	python3 -I - "aux/$deck.aux" "$dir/$deck.bib" "${srcs[@]}" <<'PYEOF' || die "cannot write $deck.bib"
import re, sys
aux, out, srcs = sys.argv[1], sys.argv[2], sys.argv[3:]
cites = {k.strip().lower() for c in re.findall(r'\\citation\{([^}]*)\}', open(aux).read()) for k in c.split(',')}
entries, strings, order = {}, {}, []
for f in srcs:
    t = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'^@(\w+)\s*\{', t, re.M):
        i, d = m.end(), 1
        while i < len(t) and d: d += {'{': 1, '}': -1}.get(t[i], 0); i += 1
        kind, body = m.group(1).lower(), t[m.end():i - 1]
        if kind == 'string':
            strings.setdefault(body.split('=', 1)[0].strip().lower(), t[m.start():i])
        elif kind not in ('preamble', 'comment'):
            k = body.split(',', 1)[0].strip().lower()
            if k not in entries: entries[k] = t[m.start():i]; order.append(k)
want = set(order) if '*' in cites else cites & set(entries)
grew = True
while grew:
    more = set()
    for k in want:
        x = re.search(r'^\s*crossref\s*=\s*[{"]([^}"]*)[}"]', entries[k], re.M | re.I)
        if x and x.group(1).strip().lower() in entries: more.add(x.group(1).strip().lower())
    grew = bool(more - want); want |= more
missing = cites - set(entries) - {'*'}
if missing: sys.exit('not in the .bib files: ' + ', '.join(sorted(missing)))
text = '\n'.join(entries[k] for k in order if k in want)
used, grew = set(), True
while grew:
    names = {n for n in strings if re.search(r'(?:=|#)\s*' + re.escape(n) + r'\s*(?=[,#}\n]|$)', text + '\n'.join(strings[u] for u in used), re.I)}
    grew = bool(names - used); used |= names
with open(out, 'w') as o:
    for n in sorted(used): o.write(strings[n] + '\n')
    if used: o.write('\n')
    o.write('\n\n'.join(entries[k] for k in order if k in want) + '\n')
PYEOF
	perl -pi -e 'BEGIN { $d = shift } s#\\bibliography\{[^}]*\}#\\bibliography{$d}#g' "$deck" "$dir/$deck.tex"
fi
for s in $(sed -n 's/^\\bibstyle{\(.*\)}$/\1/p' "aux/$deck.aux"); do find_one "$s.bst"; done

## a file called through a folder is called by name, now that all sit side by side:
## {img/x} becomes {x} wherever x, with or without its extension, is one of the files here (x may hold spaces);
## never inside a web address ({https://…/l2-jason} kept, though l2-jason.tex is here: AS 20·21 L2, L3, T4),
## nor one written without its scheme ({hub.docker.com/r/bitnami/etcd} kept, though etcd.png is here: DS 23·24 L7),
## nor a command line, whose folder part holds a space ({> docker pull bitnami/etcd}, the same slide);
## inside a macro, {img/#1} becomes {#1} wherever img/ is a folder of the repository (the check below proves it)
for f in "$dir"/*.tex "$dir"/*.sty; do
	[ -e "$f" ] || continue
	perl -pi -e 'BEGIN { $d = shift } s{\{(?![^{}]*://)(?![\w-]+(?:\.[\w-]+)+/)(?![^{}/]*\s[^{}]*/)[^{}%#\\]*/([^{}/%#\\]+)\}}{ (-e "$d/$1" || (() = glob("\Q$d/$1\E.*"))) ? "{$1}" : $& }ge' "$dir" "$f"
	perl -pi -e 's{\{([^{}%#\\]+)/(#[1-9][^{}/%\\]*)\}}{ -d $1 ? "{$2}" : $& }ge' "$f"
done

## check: a plain build in a copy, no local tree, same warnings and same pages as aux/
cp -R "$dir" "$work/test"
(
	cd "$work/test"
	unset TEXINPUTS BIBINPUTS BSTINPUTS
	export TEXMFHOME="$work/texmf"
	pdflatex -interaction=nonstopmode "$deck" >/dev/null || true
	if grep -q '^\\bibdata' "$deck.aux"; then bibtex "$deck" >/dev/null || die "bibtex fails in the flat folder"; fi
	## rerun until .aux and .nav settle: beamer's frame total changes them without asking for a rerun
	for i in 1 2 3 4 5; do
		before=$(cat "$deck.aux" "$deck.nav" 2>/dev/null | cksum)
		pdflatex -interaction=nonstopmode -recorder "$deck" >/dev/null || true
		if [ "$before" = "$(cat "$deck.aux" "$deck.nav" 2>/dev/null | cksum)" ] &&
			! grep -q 'Rerun to get' "$deck.log"; then break; fi
	done
	grep -q '^!' "$deck.log" && die "the flat build stops with an error"
	grep -q 'Library/texmf' "$deck.fls" && die "the flat build reads ~/Library/texmf"
	exit 0
)
warns() { grep -E '^(Package|LaTeX|Class).*Warning|Overfull|Underfull' "$1" | sed 's/[0-9.]//g' | sort; }
[ "$(warns "aux/$deck.log")" = "$(warns "$work/test/$deck.log")" ] ||
	die "the flat build warns differently from aux/$deck.log"
mkdir -p "$work/a" "$work/b"
pdftoppm -r 100 -png "aux/$deck.pdf" "$work/a/p"
pdftoppm -r 100 -png "$work/test/$deck.pdf" "$work/b/p"
[ "$(ls "$work/a" | wc -l)" -eq "$(ls "$work/b" | wc -l)" ] || die "page count differs"
for p in "$work"/a/*.png; do
	cmp -s "$p" "$work/b/$(basename "$p")" || die "page $(basename "$p" .png) differs"
done

## the archive
mkdir -p zip
rm -f "zip/$deck.zip"
(cd "$work" && zip -X -q -r - "$deck") > "zip/$deck.zip"
echo "zip/$deck.zip: $(ls "$dir" | wc -l | tr -d ' ') files, $(ls "$work/a" | wc -l | tr -d ' ') pages identical"
