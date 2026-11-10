#!/usr/bin/env python3
"""Web and mail addresses not written with the style's commands (house rule, Andrea, 2026-11-10): a web address is
\\uurl (or \\uuurl), a mail address \\umail (or \\uumail), the title page's included; never a plain \\url, a
\\texttt address or an \\href to mailto:.  Read off the source, comments and verbatim out.

  urls.py [--fix] tex/<deck>.tex [sty/<layer>.sty ...]      --fix: rewrite them in place, as reported
"""
import re, sys

RAW = re.compile(r'\\begin\{(verbatim|semiverbatim|lstlisting|minted|Verbatim)\}')
BAD = [
    (re.compile(r'\\url\{mailto:([^}]*)\}'), r'\\umail{\1}'),
    (re.compile(r'\\url\{([^}]*)\}'), r'\\uurl{\1}'),
    (re.compile(r'\\href\{mailto:([^}]*)\}\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'), r'\\umail{\1}'),   # the text may nest: {\texttt{#1}}
    (re.compile(r'\\texttt\{\s*([^{}\\\s]+@[^{}\\\s]+)\s*\}'), r'\\umail{\1}'),
]
FIX = '--fix' in sys.argv
ARGS = [a for a in sys.argv[1:] if a != '--fix']
bad = 0
for path in ARGS:
    raw = None
    out = []
    for n, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
        out.append(line)
        if raw:
            if f'\\end{{{raw}}}' in line: raw = None
            continue
        m = RAW.search(line)
        if m and not line.lstrip().startswith('%'):
            raw = m.group(1)
            if f'\\end{{{raw}}}' in line: raw = None
            continue
        code = re.split(r'(?<!\\)%', line, maxsplit=1)[0]
        com = line[len(code):]
        code = re.sub(r'\\verb(.).*?\1', '', code)
        for pat, fix in BAD:
            for hit in pat.finditer(code):
                print(f'{path}:{n}: {hit.group(0)}  ->  {hit.expand(fix)}')
                bad += 1
            code = pat.sub('', code)
        if FIX and '\\verb' not in line:
            c = line[:len(line) - len(com)]
            for pat, fix in BAD: c = pat.sub(fix, c)
            depth = lambda t: len(re.findall(r'(?<!\\)\{', t)) - len(re.findall(r'(?<!\\)\}', t))
            if depth(c) != depth(line[:len(line) - len(com)]):   # a rewrite never changes the braces (2026-11-10, AS 20·21 S3)
                sys.exit(f'{path}:{n}: --fix would unbalance the braces; nothing written')
            out[-1] = c + com
    if FIX: open(path, 'w', encoding='utf-8').write(''.join(out))
print(f'--- {" ".join(ARGS)}: {bad} address(es) not in the house form' + (', rewritten' if FIX and bad else ''))
sys.exit(0 if FIX or not bad else 1)
