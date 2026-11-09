# beamer-AMSRedGrey — branch `cesena`

The old **AMSCesena** Beamer style, version 1.0 (RCS 2013/08/12), exactly as
it was copied into the CILC 2016 deck in June 2016: the ancestor whose reds
and greys `main` recovered. It is not `main` and never merges into it.

It exists so that decks of 2013–2017 can be rebuilt as they were, pinned
through their `.style` submodule at the tag `cesena-1.0` — the first being
`labelledvariables-cilc2016-slides` (*Labelled Variables in Logic
Programming: Foundations*, CILC 2016, Milan, 20 June 2016). Source: the deck's
own copy in
`~/Documents/pubblicazioni/9 - published/2016-2020/2016/CDDO-CILC 2016/slides/`,
the same in all six build folders, recovered on 2026-10-26. iCloud's
`Archivio/Documenti/prodotti/beamer/AMSCesena/` holds a later state (January
2017, same RCS line): `\setbeamertemplate{navigation symbols}{}` and two block
environments, `alertb` and `exampleb`. It is not here: no recovered deck uses
it yet.

The theme builds on beamer's `infolines`, `rounded` and `beaver`, and loads
its seal as `img/almacesena-background`, so a consumer links
`img/almacesena-background.pdf` to `.style/almacesena-background.pdf`. The
bibliography style of the time was LaTeX's own `apalike`, not `apalike-AMS`.

## Two tags, two states of 1.0

- `redgrey-cesena-1.0-2013` — the file as copied into the ICCCI 2013 deck
  (*Complexity & Interaction*, Craiova, 11 September 2013), dated 12 August
  2013: navigation symbols shown, `\emph` in dark red italics. Pinned by
  `interactioncomplexity-iccci2013-slides`' stage `v1-presented`; recovered on
  2026-11-09 from `~/Documents/presentazioni/2013/iccci/Omicini-ICCCI2013/`.
- `redgrey-cesena-1.0` — the later state of the same RCS line, as in the CILC
  2016 deck: `\beamertemplatenavigationsymbolsempty` added, the `\emph`
  redefinition commented out.

The 2013 commit sits on top of the branch, after the CILC one, because a
pushed history is never rewritten; the tags say which state is which, and the
branch's head carries the 2013 file.
