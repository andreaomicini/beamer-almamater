"""The CI's check of impact.py's .bst rule (job impact-test): a .bst change that only adds FUNCTIONs is additive (no deck
is rebuilt for it), any other change is not; a change to FUNCTIONs alone touches the entry types calling them, and every
entry when a FUNCTION run for all of them is touched (2026-11-27). And apice.bib's rule: an entry changes when its text
or its type does (2026-11-27: bmc-advcomp58, @article to @incollection, rebuilt no deck), its crossref children with it,
and a change of spacing alone is none. Run from the repository root: python3 ci/test/impact-bst-test.py"""
import sys, pathlib
src = pathlib.Path('ci/impact.py').read_text()
ns = {}; exec(compile(src.split('\nif __name__')[0], 'impact', 'exec'), ns)
add = ns['bst_additions']
types = lambda a, b: (lambda r: None if r is None else r[0])(ns['bst_changed_types'](a, b))
OLD = '''ENTRY { author title } {} { label }
FUNCTION {format.a} { "a" }   % a comment
FUNCTION {article} { format.a write$ }
FUNCTION {format.t} { "t" }
FUNCTION {phdthesis} { format.t 'skip$ write$ }
FUNCTION {presort} { "p" }
READ
ITERATE {presort}
ITERATE {call.type$}
'''
NEW = OLD.replace('READ', 'FUNCTION {format.b} { "b" }\nFUNCTION {courseproject} { format.b write$ }\nREAD')
ch = ns['changed_entries']
BIB = '''@article{a, title = {A}, year = 2003}
@book{p, title = {P}}
@inbook{c,
  crossref = {p},
  chapter = 1
}
@misc{z, title = {Z}}
'''
cases = [('a new entry type is additive', add(OLD, NEW) == {'format.b', 'courseproject'}),
         ('a comment only is no change', add(OLD, OLD.replace('% a comment', '% another')) == set()),
         ('a changed FUNCTION is not additive', add(OLD, OLD.replace('"a"', '"A"')) is None),
         ('a changed ENTRY is not additive', add(OLD, OLD.replace('author title', 'author title note')) is None),
         ('a changed helper touches its callers only', types(OLD, OLD.replace('"t"', '"T"')) == {'format.t', 'phdthesis'}),
         ('a changed entry type touches itself only', types(OLD, OLD.replace('format.t \'skip$', 'format.t "x" \'skip$')) == {'phdthesis'}),
         ('a string with a function name is no call', types(OLD, OLD.replace('"a"', '"format.t"')) == {'format.a', 'article'}),
         ('a FUNCTION run for every entry touches all', types(OLD, OLD.replace('"p"', '"q"')) is None),
         ('a changed ENTRY touches all', types(OLD, OLD.replace('author title', 'author title note')) is None),
         ('a removed FUNCTION touches all', types(OLD, OLD.replace('FUNCTION {presort} { "p" }\n', '')) is None),
         ('a removed FUNCTION is not additive', add(OLD, OLD.replace('FUNCTION {format.a} { "a" }   % a comment\n', '')) is None)]
cases += [('no change is no change', ch(BIB, BIB) == set()),
         ('spacing alone is no change', ch(BIB, BIB.replace('title = {A}', 'title  =  {A}')) == set()),
         ('a changed type is a change', ch(BIB, BIB.replace('@article{a', '@incollection{a')) == {'a'}),
         ('a changed field is a change', ch(BIB, BIB.replace('2003', '2004')) == {'a'}),
         ('a changed parent changes its children', ch(BIB, BIB.replace('{P}', '{Q}')) == {'p', 'c'}),
         ('an @preamble changed: every deck', ch(BIB, BIB + '@preamble{"x"}') is None)]
for name, ok in cases: print(('ok   ' if ok else 'FAIL ') + name)
if not all(ok for _, ok in cases): sys.exit(1)
print('impact-bst-test: %d cases' % len(cases))
