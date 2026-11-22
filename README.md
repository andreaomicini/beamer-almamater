# beamer-AMSSilverBlue — branch `cesena`

The old **AMSCesenaBleu** Beamer style, version 1.0 (RCS 2016/08/15), exactly
as it was copied into the WOA 2018 tutorial deck in June 2018: the ancestor
whose colours `main` recovered. It is not `main` and never merges into it.

It exists so that decks of 2016–2019 can be rebuilt as they were, pinned
through their `.style` submodule at the tag `cesena-1.0` — the first being
`blockchain-woa2018minischool-slides` (Doctorate Mini-School @ WOA 2018,
Palermo, 27 June 2018). Source: the deck's own copy in
`~/Documents/presentazioni/2018/WOA 2018 Tutorial/slides/1/`, recovered on
2026-10-25; iCloud's `Archivio/Documenti/prodotti/beamer/AMSCesenaBleu/`
(2019) holds the same file without its RCS line.

The theme loads its seal as `img/almacesena-background`, so a consumer links
`img/almacesena-background.pdf` to `.style/almacesena-background.pdf`. The
bibliography style of the time was LaTeX's own `apalike`, not `apalike-AMS`.

Three tags, one per variant:

- `cesena-1.0` — the style as Andrea had it, loading the seal from `img/`.
- `cesena-1.0-ciatto` — Giovanni Ciatto's copy, used for his deck of 30 May
  2018 (*A gentle introduction to the Blockchain and Smart contracts*,
  Autonomous Systems course), the seed of the tutorial: the seal from
  `./res/img/` (a consumer links `res/img/almacesena-background.pdf` instead),
  numeric labels in the bibliography (`\insertbiblabel`), and `\hhref` without
  its light twin `\hhhref`.
- `cesena-1.0-2017` — the copy in Andrea's course folders of 2017/18 and 2018/19
  (`corsi/…/SD 2017:2018/slides/`, 15 Aug 2017; the SD 2018:2019 copy is a
  re-save of Jan 2019 differing by one space in the RCS line): abstract
  colours added, `\hhref` and `\hhhref` gone (the decks' `.sty` has its own),
  the seal from `img/`. Pinned by `sd1819-slides`' history. The branch head
  carries this variant.
