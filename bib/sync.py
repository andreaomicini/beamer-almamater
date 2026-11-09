#!/usr/bin/env python3
"""sync.py -- a helper to align bib/apice.bib with APICe BY NEED, entry by entry. Writes apice.bib and pool.bib, never APICe.

    python3 bib/sync.py check <key>...            those entries against their records
    python3 bib/sync.py pull <key>...             those entries rewritten from their records (our key kept)
    python3 bib/sync.py add <Record> [<key>]      a record's BibTeX added under <key> (default: APICe's own)
    python3 bib/sync.py promote <key>             a pool.bib entry moved into apice.bib (from its record, if any)
    python3 bib/sync.py integrity                 the local checks only, no APICe

The rule (Andrea, 2026-11-09): alignment goes piecemeal, by need -- when an entry changes, when a deck starts citing a
work, when a deck is created or recovered -- and only the entries involved are touched. NEVER call this from CI, a
hook, a schedule or any other automation: it is a helper for a person working on a deck. The named records are read
live (Safari's APICe session, ~/bin/apc/lib/apice-cookie.py): a handful of requests.

`check --all` / `pull --all` take the whole file: only when Andrea decides it is the case. They read the APICe backups
(~/APICe/{publications,talks,theses}/*.xar) and, live, the records modified after each backup. NOT TESTED (2026-11-09).

The content rules (bib/README.md): APICe gives the content, minus the abstract; the key is ours, one per record; only
`published` publications; web resources are @webpage entries with no record. Every command that writes ends with the
integrity check: keys unique ignoring case, every crossref parent present, BibTeX reading both files with no error.
"""
import json, os, re, subprocess, sys, tempfile, zipfile, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APICE, POOL = os.path.join(ROOT, 'bib', 'apice.bib'), os.path.join(ROOT, 'bib', 'pool.bib')
SPACES = {'Publication': ('~/APICe/publications/Publication.WebHome.xar', 'Publications.Class'),
          'Talk': ('~/APICe/talks/Talk.WebHome.xar', 'Talks.Class'),
          'Thesis': ('~/APICe/theses/Thesis.WebHome.xar', 'Theses.Class')}
LIVE = '--all' not in sys.argv     # named keys: live; --all: the backups first


# ---------- the .bib files, kept as text: an entry is replaced or added, the rest untouched
def entries(text):
    """[(start, end, type, key)] of every entry in the text"""
    out = []
    for m in re.finditer(r'^@(\w+)\s*\{\s*([^,\s]+)\s*,', text, re.M):
        if m.group(1).lower() in ('string', 'preamble', 'comment'): continue
        i, d = m.end(), 1
        while i < len(text) and d: d += {'{': 1, '}': -1}.get(text[i], 0); i += 1
        out.append((m.start(), i, m.group(1).lower(), m.group(2)))
    return out


def field(body, name):
    m = re.search(r'^\s*%s\s*=\s*' % re.escape(name), body, re.M | re.I)
    if not m: return ''
    i, d = m.end(), 0
    while i < len(body):
        c = body[i]
        if c == '{': d += 1
        elif c == '}':
            if d == 0: break
            d -= 1
        elif c == ',' and d == 0: break
        i += 1
    return body[m.end():i].strip().strip('{}"')


def drop_field(body, name):
    m = re.search(r'^\s*%s\s*=\s*' % re.escape(name), body, re.M | re.I)
    if not m: return body
    i, d = m.end(), 0
    while i < len(body):
        c = body[i]
        if c == '{': d += 1
        elif c == '}':
            if d == 0: break
            d -= 1
        elif c == ',' and d == 0: i += 1; break
        i += 1
    return body[:m.start()] + body[i:].lstrip(' ').lstrip('\n')


def insert_field(body, name, val):
    lines = body.split('\n')
    idx = [n for n, l in enumerate(lines) if re.match(r'^\s+[a-z][\w-]*\s*=', l)]
    after = next((n for n in idx if re.match(r'^\s+([a-z][\w-]*)', lines[n]).group(1) > name), None)
    if after is not None:
        lines.insert(after, f'    {name} = {val},')
    else:
        k = max(idx)
        lines[k] = lines[k].rstrip().rstrip(',') + ','
        lines.insert(k + 1, f'    {name} = {val}')
    return '\n'.join(lines)


# ---------- APICe
_xar = {}


def cookie():
    return subprocess.run(['python3', os.path.expanduser('~/bin/apc/lib/apice-cookie.py'), 'apice.unibo.it'],
                          capture_output=True, text=True).stdout.strip()


_stale = None


def stale():
    """{space: names} of the pages modified on APICe after that space's backup was taken: read live, not from the XAR"""
    global _stale
    if _stale is not None: return _stale
    import datetime
    since = {sp: datetime.datetime.fromtimestamp(os.path.getmtime(os.path.expanduser(p)), datetime.timezone.utc)
             for sp, (p, _) in SPACES.items()}
    oldest, c, _stale, start = min(since.values()), cookie(), {sp: set() for sp in SPACES}, 0
    while True:
        u = f'https://apice.unibo.it/rest/wikis/xwiki/modifications?start={start}&number=500'
        x = subprocess.run(['curl', '-s', '-m', '60', '-H', 'Cookie: ' + c, '-H', 'Accept: application/xml', u],
                           capture_output=True, text=True).stdout
        rows = re.findall(r'<space>([^<]*)</space><name>([^<]*)</name>.*?<modified>([^<]*)</modified>', x)
        if not rows: break
        for sp, name, when in rows:
            t = datetime.datetime.fromisoformat(when.replace('Z', '+00:00'))
            if sp in since and t > since[sp]: _stale[sp].add(name)
        if datetime.datetime.fromisoformat(rows[-1][2].replace('Z', '+00:00')) < oldest: break
        start += len(rows)                 # the server may send fewer than asked
    n = sum(len(v) for v in _stale.values())
    print(f'(APICe: {n} records modified after their backup, read live)', file=sys.stderr)
    return _stale


def record(rec):
    """(space, bibtex, status) of an APICe record, or (None, '', '')"""
    if not LIVE and not any(rec in v for v in stale().values()):
        for sp, (path, cls) in SPACES.items():
            z = _xar.setdefault(sp, zipfile.ZipFile(os.path.expanduser(path)))
            try: s = z.read(f'{sp}/{rec}.xml').decode('utf-8', 'replace')
            except KeyError: continue
            o = s.split('<object>')[1] if '<object>' in s else s
            b = re.search(r'<bibtex>([^<]*)</bibtex>', o); st = re.search(r'<status>([^<]*)</status>', o)
            return sp, html.unescape(b.group(1)) if b else '', st.group(1) if st else ''
    c = cookie()
    for sp, (_, cls) in SPACES.items():
        u = f'https://apice.unibo.it/rest/wikis/xwiki/spaces/{sp}/pages/{rec}/objects/{cls}/0'
        r = subprocess.run(['curl', '-s', '-m', '30', '-H', 'Cookie: ' + c, '-H', 'Accept: application/json', u],
                           capture_output=True, text=True).stdout
        try: p = {x['name']: x.get('value') or '' for x in json.loads(r)['properties']}
        except (ValueError, KeyError): continue
        return sp, p.get('bibtex', ''), p.get('status', '')
    return None, '', ''


def from_record(rec, key):
    """the record's BibTeX as an apice.bib entry: our key, no abstract, an apice field"""
    sp, b, st = record(rec)
    if sp is None and not LIVE:
        sp, b, st = record_live(rec)      # newer than the backups
    if sp is None: sys.exit(f'sync: no record {rec} on APICe')
    if sp == 'Publication' and st != 'published': sys.exit(f'sync: {rec} has status {st!r}: only published records')
    m = re.match(r'\s*@(\w+)\s*\{\s*[^,\s]*\s*,(.*)\}\s*$', b, re.S)
    if not m: sys.exit(f'sync: {sp}.{rec} carries no BibTeX')
    body = '\n' + drop_field(m.group(2), 'abstract').lstrip('\n')   # the first field on its own line
    if not field(body, 'apice'): body = insert_field(body, 'apice', '{%s}' % rec)   # in its alphabetical slot
    return f'@{m.group(1).lower()}{{{key},' + body.rstrip() + '\n}'


def record_live(rec):
    global LIVE
    LIVE, saved = True, LIVE
    try: return record(rec)
    finally: LIVE = saved


# ---------- integrity
def integrity():
    a, p = open(APICE).read(), open(POOL).read()
    problems, keys = [], {}
    for name, text in (('apice.bib', a), ('pool.bib', p)):
        for s, e, t, k in entries(text):
            if k.lower() in keys: problems.append(f'key {k} in {name} and {keys[k.lower()]} (BibTeX ignores case)')
            keys[k.lower()] = name
    for s, e, t, k in entries(a):
        x = field(a[s:e], 'crossref')
        if x and x.lower() not in keys: problems.append(f'{k}: crossref {x} missing')
    with tempfile.TemporaryDirectory() as d:
        for f in (APICE, POOL, os.path.join(ROOT, 'apalike-AMS.bst')):
            os.symlink(f, os.path.join(d, os.path.basename(f)))
        open(os.path.join(d, 't.aux'), 'w').write('\\citation{*}\n\\bibstyle{apalike-AMS}\n\\bibdata{apice,pool}\n')
        subprocess.run(['bibtex', 't'], cwd=d, capture_output=True, timeout=120)
        blg = open(os.path.join(d, 't.blg'), errors='replace').read()
        n = open(os.path.join(d, 't.bbl'), errors='replace').read().count('\\bibitem')
    errs = re.findall(r'(I was expecting.*|Repeated entry.*|.*doesn\'t exist|I couldn\'t open.*)', blg)
    problems += [f'BibTeX: {x}' for x in errs]
    total = len(entries(a)) + len(entries(p))
    if n != total: problems.append(f'BibTeX read {n} entries of {total}')
    print(f'integrity: {len(entries(a))} entries in apice.bib, {len(entries(p))} in pool.bib, BibTeX read {n}; '
          + ('no problem' if not problems else f'{len(problems)} problems'))
    for x in problems: print('  ' + x)
    return not problems


# ---------- commands
def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def check(keys):
    global LIVE
    a = open(APICE).read(); diff = 0
    for s, e, t, k in entries(a):
        rec = field(a[s:e], 'apice')
        if not rec or not ('--all' in keys or k in keys): continue
        want = from_record(rec, k)
        if norm(want) != norm(a[s:e]) and not LIVE:
            LIVE = True; want = from_record(rec, k); LIVE = False   # --all: the backup may be older, confirm live
        if norm(want) != norm(a[s:e]): diff += 1; print(f'differs from APICe: {k} ({rec})')
    print(f'{diff} entries differ from their record' + (' (sync.py pull <key> to align)' if diff else ''))
    return integrity() and not diff


def pull(keys):
    a = open(APICE).read(); out, last, n = [], 0, 0
    for s, e, t, k in entries(a):
        rec = field(a[s:e], 'apice')
        if rec and ('--all' in keys or k in keys):
            new = from_record(rec, k)
            if norm(new) != norm(a[s:e]): out.append(a[last:s] + new); last = e; n += 1; print(f'pulled {k} ({rec})')
    out.append(a[last:]); open(APICE, 'w').write(''.join(out))
    print(f'{n} entries rewritten from APICe'); integrity()


def add(rec, key=None):
    a = open(APICE).read()
    if any(field(a[s:e], 'apice') == rec for s, e, t, k in entries(a)): sys.exit(f'sync: {rec} is already in apice.bib')
    new = from_record(rec, key or 'KEY')
    if not key: key = re.match(r'@\w+\{([^,]*),', record(rec)[1] or record_live(rec)[1]).group(1); new = new.replace('{KEY,', '{%s,' % key, 1)
    open(APICE, 'w').write(a.rstrip('\n') + '\n\n' + new + '\n')
    print(f'added {key} ({rec})'); integrity()


def promote(key):
    a, p = open(APICE).read(), open(POOL).read()
    hit = [(s, e) for s, e, t, k in entries(p) if k == key]
    if not hit: sys.exit(f'sync: no {key} in pool.bib')
    s, e = hit[0]; rec = field(p[s:e], 'apice')
    new = from_record(rec, key) if rec else p[s:e]
    open(POOL, 'w').write(p[:s].rstrip('\n') + '\n\n' + p[e:].lstrip('\n'))
    open(APICE, 'w').write(a.rstrip('\n') + '\n\n' + new + '\n')
    print(f'promoted {key}' + (f' ({rec}, from APICe)' if rec else ' (no record: as it was)')); integrity()


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args: sys.exit(__doc__)
    cmd, rest = args[0], args[1:]
    if cmd == 'integrity': sys.exit(0 if integrity() else 1)
    elif cmd == 'check' and rest: sys.exit(0 if check(rest) else 1)
    elif cmd == 'pull' and rest: pull(rest)
    elif cmd == 'add' and rest: add(*rest[:2])
    elif cmd == 'promote' and len(rest) == 1: promote(rest[0])
    else: sys.exit(__doc__)
