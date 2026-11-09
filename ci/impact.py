#!/usr/bin/env python3
"""Which decks a push touches: the CI child pipeline that builds them, and only them.

    impact.py <before-sha>            YAML for the child pipeline, on stdout
    impact.py <before-sha> --list     the decks, one per line, each with why

Run from a deck repository's root (beamer-almamater/ci/impact.gitlab-ci.yml). The rule (Andrea, 2026-11-09): a deck is
built when something it reads changed, and only then.

- deps/<deck>.files lists every file of the repository the deck reads, links and their targets in .style alike
  (decks/records.pl writes it at each build). A deck is touched when a changed file is on its list.
- A move of .style counts as the files changed between the two pins, as .style/<path>. A shared .sty that only adds
  definitions (comments aside, every other line and every existing definition unchanged) counts only for the decks
  using a new name, in their .tex or in a repository file they read (Andrea, 2026-11-10: \\umail must not rebuild
  everything). Its bib/apice.bib is decided entry by entry: the entries whose text changes, appears or goes, their crossref children, and the decks citing
  them in bib/cites/<deck>.keys. Its pool.bib never counts: no deck reads it.
- A repository's own .bib (a course before the shared file) is decided the same way, entry by entry.
- .latexmkrc, .gitlab-ci.yml, .gitmodules: every deck. A deck with no deps/<deck>.files: built, whatever changed.
- deps/ and bib/cites/ are what a build writes: changing them touches nothing.
- Each deck built is checked by ../check/urls.py (its .tex and the repository's own layers it reads): a deck whose web or
  mail addresses are not in the house form gets a failing job urls:<deck> listing them (Andrea, 2026-11-10). The rule
  binds a deck when it is built anyway, never all decks at once.
- With no <before-sha> (zeros: the repository's first push, or a pipeline run by hand; impact runs on main only):
  every deck, since nothing of it has been built yet (ICCCI 2013, 2026-11-09: the parent commit as the comparison
  built nothing on a new repository's first push). A <before-sha> not in the history: the parent commit.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EVERY = {'.latexmkrc', '.gitlab-ci.yml', '.gitmodules'}


def git(*a, cwd=None):
    r = subprocess.run(['git', *a], capture_output=True, text=True, cwd=cwd)
    return r.stdout if r.returncode == 0 else None


def decks():
    return sorted(p.stem for p in Path('tex').glob('*.tex'))


def parse(text):
    """entries: key -> (normalised text, crossref parent); strings: name -> value; preamble"""
    entries, strings, preamble, i = {}, {}, [], 0
    for m in re.finditer(r'@(\w+)\s*[{(]', text or ''):
        if m.start() < i: continue
        j, depth = m.end(), 1
        while j < len(text) and depth:
            depth += {'{': 1, '(': 1, '}': -1, ')': -1}.get(text[j], 0); j += 1
        body, kind = text[m.end():j - 1], m.group(1).lower()
        i = j
        if kind == 'string':
            name, _, value = body.partition('=')
            strings[name.strip().lower()] = re.sub(r'\s+', ' ', value).strip()
        elif kind == 'preamble':
            preamble.append(re.sub(r'\s+', ' ', body).strip())
        elif kind != 'comment':
            key = body.split(',', 1)[0].strip().lower()
            cr = re.search(r'^\s*crossref\s*=\s*[{"]([^}"]*)[}"]', body, re.M | re.I)
            entries[key] = (re.sub(r'\s+', ' ', body).strip(), cr.group(1).strip().lower() if cr else None)
    return entries, strings, preamble


def changed_entries(old, new):
    """the keys whose entry changed, with their crossref children; None: every deck (an @preamble changed)"""
    (o, os_, op), (n, ns, np) = parse(old), parse(new)
    if op != np: return None
    ch = {k for k in o.keys() | n.keys() if o.get(k, (None,))[0] != n.get(k, (None,))[0]}
    for s in {s for s in os_.keys() | ns.keys() if os_.get(s) != ns.get(s)}:
        ch |= {k for k, (body, _) in n.items() if re.search(r'(?:=|#)\s*' + re.escape(s) + r'\s*(?=[,#}]|$)', body, re.I)}
    grew = True
    while grew:
        more = {k for k, (_, p) in n.items() if p in ch} - ch
        ch |= more; grew = bool(more)
    return ch


def citing(keys):
    out = set()
    for d in decks():
        f = Path(f'bib/cites/{d}.keys')
        if not f.exists() or keys & {k.strip().lower() for k in f.read_text().split()}: out.add(d)
    return out


DEF = re.compile(r'\\(?:(?:new|renew|provide)command\*?|DeclareRobustCommand\*?|(?:New|Renew|Provide|Declare)Document'
                 r'(?:Command|Environment)|(?:new|renew)environment\*?|g?def)\s*\{?\s*\\?([A-Za-z@]+)\s*\}?')


def definitions(text):
    """(name -> its whole definition, normalised), and the rest of the text, normalised; comments out"""
    text = '\n'.join(re.sub(r'(?<!\\)%.*', '', l) for l in text.split('\n'))
    defs, rest, i = {}, [], 0
    for m in DEF.finditer(text):
        if m.start() < i: continue
        j = m.end()
        while True:                          # parameters, optional and mandatory arguments
            k = j
            while k < len(text) and text[k] in ' \t\n': k += 1
            if k < len(text) and text[k] in '[{':
                close, depth = {'[': ']', '{': '}'}[text[k]], 0
                for e in range(k, len(text)):
                    depth += {'{': 1, '[': 1, '}': -1, ']': -1}.get(text[e], 0)
                    if depth == 0 and text[e] == close: break
                j = e + 1
            elif k < len(text) and text[k] == '#': j = k + 2
            else: break
        rest.append(text[i:m.start()]); defs.setdefault(m.group(1), '')
        defs[m.group(1)] += ' '.join(text[m.start():j].split())
        i = j
    rest.append(text[i:])
    return defs, ' '.join(''.join(rest).split())


def additions(old, new):
    """the names a .sty change only adds; None: the change does more (a redefinition, any other line)"""
    (od, orest), (nd, nrest) = definitions(old), definitions(new)
    if orest != nrest or any(nd.get(k) != v for k, v in od.items()): return None
    return set(nd) - set(od)


def using(names):
    """the decks whose .tex, or a repository file they read, uses one of the names (a command, or an environment)"""
    if not names: return set()
    pat = re.compile(r'\\(?:' + '|'.join(map(re.escape, names)) + r')(?![A-Za-z@])|\\begin\{(?:'
                     + '|'.join(map(re.escape, names)) + r')\}')
    seen, out = {}, set()
    def uses(f):
        if f not in seen:
            p = Path(f)
            own = p.is_file() and not p.is_symlink() and not f.startswith('.style/')   # links lead into .style
            seen[f] = bool(own and pat.search(p.read_text(errors='replace')))
        return seen[f]
    for d in decks():
        deps = Path(f'deps/{d}.files')
        read = [f'tex/{d}.tex'] + (deps.read_text().split() if deps.exists() else [])
        if not deps.exists() or any(uses(f) for f in read): out.add(d)
    return out


def style_files(old_pin, new_pin):
    """the files changed between two pins of .style, as .style/<path>, and the two texts of bib/apice.bib"""
    url = git('config', '-f', '.gitmodules', 'submodule..style.url').strip()
    if url.startswith('../'):
        import os
        host, ns = os.environ.get('CI_SERVER_HOST'), os.environ.get('CI_PROJECT_NAMESPACE')
        tok = os.environ.get('CI_JOB_TOKEN')
        if host and tok: url = f'https://gitlab-ci-token:{tok}@{host}/{ns}/{url[3:]}'
        else:                                  # on a desk: the sibling clone, with or without .git
            p = (Path.cwd() / url).resolve()
            url = str(p if p.exists() else p.with_suffix(''))
    with tempfile.TemporaryDirectory() as d:
        if git('clone', '-q', '--filter=blob:none', '--no-checkout', url, d) is None:
            return None, None, None, None
        names = git('diff', '--name-only', old_pin, new_pin, cwd=d)
        if names is None: return None, None, None, None
        files = {'.style/' + n for n in names.split()}
        bib = '.style/bib/apice.bib'
        old = git('show', f'{old_pin}:bib/apice.bib', cwd=d) if bib in files else None
        new = git('show', f'{new_pin}:bib/apice.bib', cwd=d) if bib in files else None
        sty = {f: (git('show', f'{old_pin}:{f[7:]}', cwd=d) or '', git('show', f'{new_pin}:{f[7:]}', cwd=d) or '')
               for f in files if f.endswith('.sty')}
        return files, old, new, sty


def touched(before):
    if not before: return {d: 'first push or a pipeline run by hand: nothing built yet' for d in decks()}
    base = before if before and git('cat-file', '-e', before + '^{commit}') is not None else 'HEAD~1'
    names = git('diff', '--name-only', base, 'HEAD')
    if names is None: return {d: 'no history to compare with' for d in decks()}
    changed = set(names.split())
    out = {}
    def mark(ds, why):
        for d in ds: out.setdefault(d, why)
    if changed & EVERY:
        mark(decks(), 'changed: ' + ', '.join(sorted(changed & EVERY))); return out
    # .style moved: its changed files, apice.bib entry by entry
    if '.style' in changed:
        old_pin = (git('ls-tree', base, '.style') or '').split()
        new_pin = (git('ls-tree', 'HEAD', '.style') or '').split()
        files, old, new, sty = style_files(old_pin[2], new_pin[2]) if len(old_pin) > 2 and len(new_pin) > 2 else (None,) * 4
        if files is None:
            mark(decks(), '.style moved, its changes unreadable'); return out
        for f, (a, b) in sty.items():
            added = additions(a, b)
            if added is None: continue
            files.discard(f)
            mark(using(added), f'{f} adds ' + ', '.join(sorted(added)))
        changed |= files
        if old is not None or new is not None:
            ch = changed_entries(old, new)
            if ch is None: mark(decks(), 'apice.bib: @preamble changed')
            else: mark(citing(ch), 'cites an entry changed in apice.bib: ' + ', '.join(sorted(ch))[:200])
    # the repository's own .bib files (not links into .style): entry by entry
    for b in sorted(c for c in changed if re.fullmatch(r'bib/[^/]+\.bib', c) and not Path(c).name == 'pool.bib'):
        if Path(b).is_symlink(): continue
        ch = changed_entries(git('show', f'{base}:{b}'), Path(b).read_text(encoding='utf-8') if Path(b).exists() else '')
        if ch is None: mark(decks(), f'{b}: @preamble changed')
        else: mark(citing(ch), f'cites an entry changed in {b}')
    # every other file: the decks that read it
    files = {c for c in changed if not c.endswith('.bib') and not c.startswith(('deps/', 'bib/cites/')) and c != '.style'}
    for d in decks():
        f = Path(f'deps/{d}.files')
        if not f.exists():
            if files or changed - {c for c in changed if c.startswith(('deps/', 'bib/cites/'))}:
                mark([d], 'no deps/%s.files' % d)
            continue
        hit = files & set(f.read_text().split())
        if hit: mark([d], 'reads ' + ', '.join(sorted(hit))[:200])
    return out


def urlcheck(d):
    """the hits of ../check/urls.py on a deck's .tex and the repository's own layers it reads; '' if none"""
    import os
    urls = Path(__file__).resolve().parent.parent / 'check' / 'urls.py'
    if not urls.exists(): return ''
    deps = Path(f'deps/{d}.files')
    files = [f'tex/{d}.tex'] + [f for f in (deps.read_text().split() if deps.exists() else [])
                                 if f.endswith(('.sty', '.tex')) and not f.startswith('.style/')
                                 and Path(f).is_file() and not Path(f).is_symlink() and f != f'tex/{d}.tex']
    r = subprocess.run([sys.executable, str(urls), *files], capture_output=True, text=True)
    return '' if r.returncode == 0 else r.stdout


def deck_template():
    lines = Path('.gitlab-ci.yml').read_text().splitlines()
    i = lines.index('.deck:')
    j = next((k for k in range(i + 1, len(lines)) if lines[k] and not lines[k].startswith(' ')), len(lines))
    return '\n'.join(lines[i:j]).rstrip()


def main(argv):
    if not argv: sys.exit(__doc__)
    before = '' if re.fullmatch(r'0*', argv[0]) else argv[0]
    t = touched(before)
    if '--list' in argv:
        for d in sorted(t): print(f'{d}\t{t[d]}')
        return
    print('# generated by beamer-almamater/ci/impact.py: the decks this push touches')
    for d in sorted(t): print(f'#   {d}: {t[d]}')
    print(deck_template()); print()
    if not t:
        print('no-deck-touched:\n  image: alpine:latest\n  script:\n    - echo "no deck reads a changed file"')
    for d in sorted(t):
        print(f'{d}:\n  extends: .deck\n  variables:\n    DECK: {d}\n')
        hits = urlcheck(d)
        if hits:
            lines = [l for l in hits.splitlines() if l.strip()]
            print(f'urls:{d}:\n  image: alpine:latest\n  script:')
            for l in lines: print('    - ' + __import__('json').dumps('echo ' + __import__('shlex').quote(l)))
            print('    - exit 1\n')


if __name__ == '__main__':
    main(sys.argv[1:])
