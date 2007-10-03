# beamer-AMSCesena — branch `cesena`

The **CesenaSMA2006** Beamer style, exactly as it sits beside the decks of the
course *Sistemi Multi-Agente LS*, A.Y. 2006/2007, in Cesena: the first Beamer
style of the series, the ancestor whose blues `main` recovered. It is not
`main` and never merges into it.

It exists so that the 2006/2007 course decks can be rebuilt as they were,
pinned through their `.style` submodule at the tag `cesena-2006`, the
2007/2008 ones at `cesena-2007`, the 2008/2009 ones at `cesena-2008`, the
2009/2010 ones at `cesena-2009`, the SMA-LM 2010/2011 ones at
`cesena-2010` and the SMA-LM 2011/2012 ones at `cesena-2011`. Source:
`~/Documents/corsi/2005-2010/2006:2007/SMA-LS/slides/`, recovered on
2026-10-27; the commit carries the theme's own date, 2006-10-08.

Two files, both byte for byte:

* `beamerthemeCesenaSMA2006.sty` (2006/10/08): Beamer's `rounded` inner theme
  with shadows and the `orchid` and `whale` colour themes, over Beamer's default
  blue, with `\setbeamercovered{transparent}`; ten archive folders hold it,
  all identical. Its RCS header is Tantau's
  template line, kept by every later copy of the series.
* `beamerouterthemesmoothbarsinfolines.sty` (2006/10/07): Beamer's `smoothbars`
  outer theme of 2004 (RCS 1.5), with its head line, frame title and an
  `infolines`-like foot line declared under the name `smoothbarsinfolines
  theme`. The same file is in sixteen archive folders, all identical: it also
  served `Leuven2006` and `ICTTN2007`.

`beamerthemeCesenaSMA2007.sty` (2007-10-03), byte for byte the copy beside the
2007/2008 decks (`…/2007:2008/SMA-LS/slides/`): CesenaSMA2006 with Beamer's
own `infolines` outer theme in place of `smoothbarsinfolines`, nothing else
changed, the RCS header included. Every 2007 copy in the archive is identical.

`beamerthemeCesenaSMA2008.sty` (2008-09-30), byte for byte the copy beside the
2008/2009 decks (`…/2008:2009/SMA-LS/slides/`): CesenaSMA2007 with its name in
the RCS header, nothing else changed. The three copies in the archive are
identical.

`beamerthemeCesenaSMA2009.sty` (its file date 2008-09-30), byte for byte the
copy beside the 2009/2010 decks (`…/2009:2010/SMA LS/slides/`): the same bytes
as CesenaSMA2008, its RCS header still naming CesenaSMA2008; only the file name
changed, which the 2009 decks load.

`beamerthemeCesenaSMA2010.sty` (its file date 2008-09-30): the same bytes as
CesenaSMA2009, under the name the SMA-LM 2010/2011 lab decks load (Elena
Nardini's). The one copy in the archive sits beside the EASSS 2010 slides
(`~/Documents/scuole/easss 2010/slides/`).

`beamerthemeCesena2010.sty` (2010-10-05, RCS 2010/10/01) and
`beamercolorthemecesena.sty`, byte for byte the copies beside the SMA-LM
2010/2011 course decks (`…/2010:2011/SMA-LM 2010:2011/slides/`): Beamer's
`infolines` outer theme and `rounded` inner theme with shadows, as before, over
a new colour theme `cesena`, Beamer's `beaver` (its RCS header kept) turned
blue-grey, with `orchid`'s block colours. Every archive copy of the two is
identical (25 and 84 copies).

`beamerthemeCesena2011.sty` (its file date 2010-10-05): the same bytes as
Cesena2010, its RCS header still naming Cesena2010; only the file name changed,
which the SMA-LM 2011/2012 course decks load (`…/2011:2012/SMA-LM/slides/`,
beside the same `beamercolorthemecesena.sty`). Every archive copy is identical
(51).

None loads an image: the UniBo logo in the corner of the 2006 slides is the
decks' own `\logo`, from their `img/`. The bibliography style of the time was
LaTeX's own `apalike`, not `apalike-AMS`.

The name `AMSCesena` of this repository is not the 2010 `AMSCesena`, the red
theme over `beaver`, which survives as the branch `cesena` of
[beamer-AMSRedGrey](https://github.com/andreaomicini/beamer-AMSRedGrey), tag
`cesena-1.0`.

`beamerthemeCesenaSD2008.sty` and `beamerthemeCesenaSD2009.sty` (their file
date 2007-10-03): the same bytes as CesenaSMA2007, its RCS header still
naming CesenaSMA2006; only the file names changed, which the *Sistemi
Distribuiti L-A* decks of 2007/2008 (`…/2007:2008/SD-LA/slides/`) and of
2008/2009 (`…/2008:2009/SD-L/slides/`) load. Tags `cesena-sd-2008` and
`cesena-sd-2009`; one archive copy of each, identical.
