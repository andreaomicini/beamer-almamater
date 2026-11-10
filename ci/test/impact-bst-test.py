"""The CI's check of impact.py's .bst rule (job impact-test): a .bst change that only adds FUNCTIONs is additive (no deck
is rebuilt for it), any other change is not. Run from the repository root: python3 ci/test/impact-bst-test.py"""
import sys, pathlib
src = pathlib.Path('ci/impact.py').read_text()
ns = {}; exec(compile(src.split('\nif __name__')[0], 'impact', 'exec'), ns)
add = ns['bst_additions']
OLD = '''ENTRY { author title } {} { label }
FUNCTION {format.a} { "a" }   % a comment
FUNCTION {article} { format.a write$ }
READ
ITERATE {call.type$}
'''
NEW = OLD.replace('READ', 'FUNCTION {format.b} { "b" }\nFUNCTION {courseproject} { format.b write$ }\nREAD')
cases = [('a new entry type is additive', add(OLD, NEW) == {'format.b', 'courseproject'}),
         ('a comment only is no change', add(OLD, OLD.replace('% a comment', '% another')) == set()),
         ('a changed FUNCTION is not additive', add(OLD, OLD.replace('"a"', '"A"')) is None),
         ('a changed ENTRY is not additive', add(OLD, OLD.replace('author title', 'author title note')) is None),
         ('a removed FUNCTION is not additive', add(OLD, OLD.replace('FUNCTION {format.a} { "a" }   % a comment\n', '')) is None)]
for name, ok in cases: print(('ok   ' if ok else 'FAIL ') + name)
if not all(ok for _, ok in cases): sys.exit(1)
print('impact-bst-test: %d cases' % len(cases))
