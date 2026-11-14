"""The CI's check of impact.py's two .sty rules of 2026-11-14 (job impact-test): the style's version lines alone are no
change, and a .sty change that only adds a class option (its flag, its \\DeclareOption, its own \\if...\\fi block) counts
for the decks naming the option, any other change for every deck. Run from the repository root:
python3 ci/test/impact-option-test.py"""
import sys, pathlib
src = pathlib.Path('ci/impact.py').read_text()
ns = {}; exec(compile(src.split('\nif __name__')[0], 'impact', 'exec'), ns)
add, opt, unv = ns['additions'], ns['option_additions'], ns['unversioned']
OLD = r'''\newcommand{\stylemajor}{2}
\newcommand{\styleminor}{0}
\newif\if@doSeal
\@doSealfalse
\DeclareOption{bologna}{\@doSealtrue}   % a comment
\ProcessOptions
\if@doSeal
  \pgfdeclareimage{bg}{almabologna-background}
  \setbeamertemplate{background}{\pgfuseimage{bg}}
\fi
'''
BUMP = OLD.replace(r'\newcommand{\styleminor}{0}', r'\newcommand{\styleminor}{1}')
NEW = BUMP.replace(r'''\DeclareOption{bologna}{\@doSealtrue}   % a comment
''', r'''\DeclareOption{bologna}{\@doSealtrue}   % a comment
\newif\if@doBbs
\@doBbsfalse
\DeclareOption{bbs}{\@doBbstrue}
''') + r'''\if@doBbs
  \pgfdeclareimage{bg}{almabbs-background}
  \setbeamertemplate{background}{\pgfuseimage{bg}}
\fi
'''
cases = [('a version bump alone is no change', add(unv(OLD), unv(BUMP)) == set()),
         ('a new option is additive', opt(OLD, NEW) == {'bbs'}),
         ('a comment only is no change', add(unv(OLD), unv(OLD.replace('% a comment', '% another'))) == set()),
         ('an existing option changed is not additive', opt(OLD, NEW.replace(r'{bologna}{\@doSealtrue}', r'{bologna}{\@doSealfalse}')) is None),
         ('an existing line removed is not additive', opt(OLD, NEW.replace('\\ProcessOptions\n', '')) is None),
         ('a new option setting an old flag is not additive', opt(OLD, NEW.replace(r'{bbs}{\@doBbstrue}', r'{bbs}{\@doBbstrue}' + '\n' + r'\@doSealtrue')) is None),
         ('a line outside the new block is not additive', opt(OLD, NEW + r'\pgfdeclareimage{bg}{x}' + '\n') is None)]
for name, ok in cases: print('ok  ' if ok else 'FAIL', name)
print('impact-option-test: %d cases' % len(cases))
sys.exit(0 if all(ok for _, ok in cases) else 1)
