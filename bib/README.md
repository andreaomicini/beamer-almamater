# One bibliography for every deck

Since 2026-11-09 every deck, course or talk, reads one shared bibliography, `apice.bib`, kept here and reached through
the pinned `.style` submodule like the theme (Andrea's design, 2026-11-09; the decisions and their reasons are in
`~/Documents/Claude/2026.11.09 – shared bib/DECISIONS.md`).

| file | what |
| --- | --- |
| `apice.bib` | every entry a deck cites: an APICe record's BibTeX, minus the abstract, under our key; or a web resource as `@webpage` |
| `pool.bib` | the reserve: entries of the old `.bib` files that no deck cites; no deck reads it |
| `sync.py` | a helper to align entries with APICe, by need (below) |

## In a deck repository

`bib/apice.bib` and `bib/pool.bib` are committed links to `../.style/bib/`, as the theme is in `sty/`; every deck says
`\bibliography{apice}` and nothing else. `bib/cites/<deck>.keys` (the keys it cites) and `deps/<deck>.files` (every
file it reads) are written at each build by `decks/records.pl` and committed.

- **A change rebuilds only the decks it touches.** When `.style` moves, the CI (`ci/impact.py`) takes the entries of
  `apice.bib` whose text changed, appeared or went, with their crossref children, and builds only the decks citing
  one. A change to `pool.bib` builds nothing.
- **The zip carries the deck's own `<deck>.bib`**: the entries it cites, their crossref parents and the `@string`s
  they use (`zip/zip.sh`), never the shared file whole.

## The rules

- **APICe gives the content**: an entry is its record's BibTeX (Publication, Talk or Thesis), minus the abstract,
  with an `apice` field naming the record. Where a deck's text was better, APICe was corrected first (2026-11-09:
  capitals protected, compound surnames written `{Van Hentenryck}, Pascal`, missing cities and pages).
- **The key is ours**: one entry per record, so one key per record. A record cited under several keys took the key
  most decks used; keys are unique ignoring case, as BibTeX reads them.
- **Only `published` publications.** A rejected paper is never cited (FOCLASA 2008 gave way to SAC 2009).
- **Web resources are `@webpage`**: title and URL at least; an organisation as author when there is none. They have
  no record, and are the noted exceptions to the rule above.
- **No `@string` and no `@` outside entries** in `apice.bib`.
- **A field the `.bst` cannot print beside another keeps a leading underscore** (Andrea, 2026-11-10): `_editor` for an
  editor beside an author in a `@book`/`@inbook`, `_number` for a number beside a volume in a book or proceedings
  paper. BibTeX ignores it, so the page is what it was and the warning goes; the record keeps the field. `sync.py`
  applies it whenever it writes an entry (`unprintable()`), and compares with it.

## Alignment: by need, entry by entry

`apice.bib` is aligned with APICe **piecemeal**: when an entry changes, when a deck starts citing a work, when a deck is
created or recovered; only the entries involved are touched. Never a sweep of the whole file (Andrea, 2026-11-09:
"we go PIECEMEAL ... BY NEED. Otherwise we are just dead").

```sh
python3 bib/sync.py check <key>...        # those entries against their records, read live
python3 bib/sync.py pull <key>...         # rewritten from their records, our key kept
python3 bib/sync.py add <Record> [<key>]  # a record's BibTeX added (key: APICe's own unless given)
python3 bib/sync.py promote <key>         # a pool.bib entry moved into apice.bib, from its record if any
python3 bib/sync.py integrity             # local only: unique keys, crossref parents, BibTeX reads both files
```

Run from this repository's root. `sync.py` writes `apice.bib` and `pool.bib`, never APICe: an improvement found in a
deck is made on the record first, then pulled. **It is never called from CI, a hook, a schedule or any other
automation.** `check --all` and `pull --all` exist for the day Andrea decides a whole pass is the case; untested.

A change here is one commit; it reaches a deck repository when its `.style` moves, and rebuilds there only the decks
citing a changed entry.
