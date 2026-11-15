"""The CI's check that impact.py keeps file names whole (job impact-test), after 2026-11-15: FoIoT 20/21's
'html/C1 – Visions of IoT I. Humans.html' was split at its spaces, so its 'IoT' matched C4's pictures and built C4 for
nothing, and a changed name with an accent arrived octal-quoted, so no deck reading it would have been built.
Run from the repository root: python3 ci/test/impact-paths-test.py"""
import os, sys, pathlib, subprocess, tempfile
src = pathlib.Path('ci/impact.py').read_text()
ns = {}; exec(compile(src.split('\nif __name__')[0], 'impact', 'exec'), ns)
touched = ns['touched']
def git(*a): subprocess.run(['git', *a], check=True, capture_output=True)
def write(p, t=''):
    p = pathlib.Path(p); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(t, encoding='utf-8')
here = os.getcwd()
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    git('init', '-q'); git('config', 'user.email', 't@t'); git('config', 'user.name', 't')
    write('tex/c1.tex'); write('tex/c4.tex'); write('tex/c5.tex')
    write('deps/c1.files', 'tex/c1.tex\n')
    write('deps/c4.files', 'tex/c4.tex\nimg/3-layer IoT architecture.pdf\n')
    write('deps/c5.files', 'tex/c5.tex\nimg/città è bella.pdf\n')
    write('img/3-layer IoT architecture.pdf', 'a'); write('img/città è bella.pdf', 'a')
    git('add', '-A'); git('commit', '-q', '-m', 'one')
    write('html/C1 – Visions of IoT I. Humans.html', 'page'); git('add', '-A'); git('commit', '-q', '-m', 'html')
    a = touched('HEAD~1')
    write('img/città è bella.pdf', 'b'); git('add', '-A'); git('commit', '-q', '-m', 'accent')
    b = touched('HEAD~1')
    write('img/3-layer IoT architecture.pdf', 'b'); git('add', '-A'); git('commit', '-q', '-m', 'spaces')
    c = touched('HEAD~1')
    os.chdir(here)
cases = [('a page whose name has spaces touches no deck', a == {}),
         ('a changed name with accents and spaces touches its reader', set(b) == {'c5'}),
         ('a changed name with spaces touches its reader only', set(c) == {'c4'})]
for name, ok in cases: print('ok  ' if ok else 'FAIL', name)
print('impact-paths-test: %d cases' % len(cases))
sys.exit(0 if all(ok for _, ok in cases) else 1)
