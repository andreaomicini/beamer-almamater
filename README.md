# beamer-almamater

> The Beamer style of Alma Mater Studiorum — Università di Bologna decks, in six
> presets: one theme, six colour themes, two font themes

## author

* Andrea Omicini

## usage

A deck names its preset, exactly as it named its style before 2.0.0:

```latex
\documentclass[presentation]{beamer}\mode<presentation>{\usetheme{AMSUniBo}}
```

| preset | colours | faces | until 2.0.0 |
| --- | --- | --- | --- |
| `AMSUniBo` | `amsunibo`, the AMSUniBo theme for the APICe wiki | `amsmerriweather`, Merriweather and Inconsolata | [beamer-AMSUniBo](https://github.com/andreaomicini/beamer-AMSUniBo) 1.8.5 |
| `AMSBolognaFC` | `bolognafc` | `amscm`, Computer Modern | [beamer-AMSBolognaFC](https://github.com/andreaomicini/beamer-AMSBolognaFC) 1.11.4 |
| `AMSCesena` | `orchidwhale`, CesenaSMA2006's | `amscm` | [beamer-AMSCesena](https://github.com/andreaomicini/beamer-AMSCesena) 1.1.4 |
| `AMSPurpleAndGold` | `purpleandgold` | `amscm` | [beamer-AMSPurpleAndGold](https://github.com/andreaomicini/beamer-AMSPurpleAndGold) 1.3.4 |
| `AMSRedGrey` | `redgrey` | `amscm` | [beamer-AMSRedGrey](https://github.com/andreaomicini/beamer-AMSRedGrey) 1.3.4 |
| `AMSSilverBlue` | `silverblue` | `amscm` | [beamer-AMSSilverBlue](https://github.com/andreaomicini/beamer-AMSSilverBlue) 1.3.4 |

Each preset is three lines, `beamertheme<Preset>.sty`:

```latex
\usetheme{almamater}
\usecolortheme{amsunibo}
\usefonttheme{amsmerriweather}
```

**Presets only, for now** (Andrea, 2026-11-08): a deck uses one of the six names; a new combination
becomes a named preset here first, so that the template's CI builds and checks it.

The class options are those of every preset: `apice` enables the APICe BibTeX field;
**no option, no watermark** — `bologna` watermarks the slides with the Ateneo seal, `cesena` with the
Campus di Cesena seal:

```latex
\documentclass[presentation,apice,cesena]{beamer}\mode<presentation>{\usetheme{AMSBolognaFC}}
```

The seals are institutional marks, so a deck has to claim one out loud: leaving the option out is what
anyone not belonging — or no longer, or not yet belonging — to the Alma Mater should do.

A ready-to-use presentation skeleton, built once per preset by its CI, is
[beamer-almamater-template](https://github.com/andreaomicini/beamer-almamater-template).

## how the six became one (2.0.0)

Until 2.0.0 each preset was a style of its own, a repository with its own copy of everything; five of
the six themes were AMSUniBo's with the colour names replaced. Every line of the six was classified by
machine (shared, colour role, font, identity) and none was left over; the files here are generated
from them, not rewritten:

- **`beamerthemealmamater.sty`**: what the six shared, about 240 lines. Its commands name colours by
  **role** — `almamarker`, `almaemph`, `almalink`, `almaspeaker`, `almaondark`, `almaquiet`,
  `almafaint`, `almasoft` — never by palette;
- **`beamercolortheme<name>.sty`**: each style's palette, plus its element colours, which block
  titles are dark surfaces, and the value of each role (AMSBolognaFC is the one whose roles do not
  map one to one on its colours);
- **`beamerfonttheme<name>.sty`**: `amsmerriweather`, AMSUniBo's 23 lines of faces; `amscm`, empty,
  since Computer Modern needs nothing beyond what the theme declares.

Proof: the six templates and thirteen decks of every preset (930 pages) built with today's six styles
and with the split, the PDFs byte-identical but for the `/Style` entry below.

The six repositories stay, frozen and readable: the historical stages of the recovered courses pin
them (`cesena-2006` … on AMSCesena), and their READMEs keep each palette's history and sources.

## structure

<!-- markdownlint-disable MD013 -->
| file | what it is |
| --- | --- |
| `beamerthemealmamater.sty` | the theme: the `apice` and `bologna`/`cesena` options, the beamer templates, the commands below, the workarounds, name and version |
| `beamertheme<Preset>.sty` | the six presets, three lines each |
| `beamercolortheme<name>.sty` | the six colour themes: palette, element colours, dark surfaces, roles |
| `beamerfonttheme<name>.sty` | the two font themes |
| `almabologna-background.pdf`, `almacesena-background.pdf` | the seals under the `bologna` and `cesena` options |
| `apalike-AMS.bst` | the bibliography style, a renamed derivative of `apalike.bst` (see [the references frame](#the-references-frame) and the licence note below) |
| `decks/` | `courses.sty` and `talks.sty`, the mechanisms every deck shares, and the recipes in its README |
| `check/` | the shared deck checks and the canonical vocabulary `names.sty` |
| `html/`, `zip/` | a deck as one HTML page, and as one flat folder |
| `ci/` | the release, and the jobs deck repositories include: `style-lag`, `bib-impact` |
<!-- markdownlint-enable MD013 -->

Every release attaches a `style.zip` holding the `.sty`, `.bst` and background files and the `LICENSE`.

Beyond the beamer furniture, the theme defines:

<!-- markdownlint-disable MD013 -->
| command | for |
| --- | --- |
| `\speaker` `\sspeaker` | marking the actual speaker among the authors, in the long and short forms, both in bold. Safe in `\author`: the name still reaches the PDF `/Author` field, only the markup is dropped |
| `\ccite` | superscript citations; takes `\cite`'s optional note, as in `\ccite[p.~42]{key}`. `\cccite` is the same, kept for existing decks |
| `\uurl` `\uuurl` | URLs, in two sizes; since 1.6.2 no character in the address needs escaping |
| `\wwwurl` | a web page's URL, as `@webpage` prints it: the colour of a journal's name, at the size around it; since 1.8.5 |
| `\ddoi` `\dddoi` | DOIs, linked, in two sizes; since 1.6.2 no character in the DOI needs escaping |
| `\apicepubpar` | the APICe marker; defined either way, but expands to nothing unless the `apice` option is given |
| `\apice` `\aapice` | an APICe object — publication, talk, course, event — by its kind and its page name, printed as its short address and linked; since 1.7 |
| `\apicesite` `\aapicesite` | an APICe alias host, such as `andreaomicini.apice.unibo.it`; since 1.7 |
| `\apicepage` `\aapicepage` | any other APICe page, by its space and page path; since 1.7 |
| `\aalert` | a quiet alert, italic |

<!-- markdownlint-enable MD013 -->

Since 1.8 the commands take their **colour from the surface** they land on, and
the doubled form means **smaller and quieter**: `\uurl` is `\scriptsize`,
`\uuurl` `\tiny` — and so `\ddoi`/`\dddoi` and the three APICe pairs. A deck
never picks a command for its background.

* **Surfaces**: the titles of `block` and `alertblock` are dark; running text,
  block bodies and the `exampleblock` title are light.
* **On a light surface** URLs, DOIs, APICe addresses and `\alert` are
  `amsred`, their doubled forms quiet `amsgreyline`, as in the references;
  `\aalert` is `amsgreymid`, italic; citations are faint `amsgreyline`, as
  under AMSBolognaFC. On the tinted example title, citations and the doubled
  forms are `amsgreymid` (since 1.8.1), so that they still read.
* **On a dark surface** URLs, DOIs, APICe addresses and citations are
  `amsgreybg`; `\alert` and `\aalert` are `amsgreyline`, `\aalert` italic.
* `\ccite` and `\cccite` are the same command: no legible size is left below a
  `\tiny` superscript. Until 1.8 they were two shades, and the doubled URL,
  DOI and APICe commands were light, for dark surfaces: existing decks build
  as before, and on a light surface look as before.
* `\sspeaker` inherits its surface's colour: see [typography](#typography).
* `\emph` needs no twin. It is italic in `amsgreendark` everywhere except in a
  block title, whose background is that same green: there, since 1.7.4, it is
  italic in the title's own colour. The same holds for alerted and example
  blocks.

### APICe addresses

APICe gives every object a short address on a host of its kind, and some pages
an alias host of their own. The theme writes both for you, so that a deck names
what it points to and never spells out a host:

<!-- markdownlint-disable MD013 -->
| command | prints and links |
| --- | --- |
| `\apice{pub}{AcltFrocos1996}` | `pubs.apice.unibo.it/AcltFrocos1996` |
| `\apice{talk}{AgotAixia2026}` | `talks.apice.unibo.it/AgotAixia2026` |
| `\apice{course}{Iag2627}` | `courses.apice.unibo.it/Iag2627` |
| `\apice{event}{Aamas2005}` | `events.apice.unibo.it/Aamas2005` |
| `\apicesite{andreaomicini}` | `andreaomicini.apice.unibo.it` |
| `\apicepage{Courses/Series/Ise}` | `apice.unibo.it/bin/view/Courses/Series/Ise` |

<!-- markdownlint-enable MD013 -->

* **Objects** are named by kind and page name, never by host: the kinds and
  their hosts are one table in the theme, so a kind whose short address starts
  working — theses, journals, projects, products — is one line there, and no
  deck changes. An unknown kind stops the build with an error that lists the
  kinds there are.
* **`\apicesite`** is for the alias hosts: people, products, groups.
* **`\apicepage`** is for whatever is neither: a series page, a space home.
* An optional argument prints text instead of the address, linked all the same:
  `\apice[the AGoT talk]{talk}{AgotAixia2026}`.
* The address is stringed like the others below, so `A\_b` and `A_b` are one
  page name; in a bookmark, the command becomes its text, or else its address.

`\apicepubpar`, the marker `apalike-AMS.bst` writes after an entry carrying an
`apice` field, takes its host from the same table.

### addresses need no escaping

Since 1.6.2 the four address commands **string their argument before using it**
— and since 1.7 the six APICe ones too — so
`\ddoi{10.1007/978-3-032-22940-3_12}` and
`\ddoi{10.1007/978-3-032-22940-3\_12}` give the same link and the same text.
Stringing turns every token into an ordinary character, so an `_` no longer
asks for maths mode; every backslash is then dropped, which is what makes the
two spellings equivalent, and what a DOI never needs to keep.

It matters most in the bibliography, where nobody gets to escape anything:
`apalike-AMS.bst` copies the `doi` and `url` fields into the `.bbl` verbatim,
and a Springer LNCS chapter DOI ends in `_<chapter>`.

The work is done when the command runs, not by reading the argument verbatim as
`\url` does, and that is forced by beamer: a frame body is tokenised when the
frame is read, before anything in it runs, so a catcode trick would make every
frame citing a DOI `fragile`.

A PDF string stays the exception. hyperref expands a `\title` or a `\section`
before any of this can run, so there a bare `_` is still dropped with *Token not
allowed in a PDF string* — as it is in plain text — and `\_` is the spelling
that survives.

### the workarounds the theme carries

Both are handled in the theme so that no document has to deal with them.

**Commands that cannot survive hyperref's PDF-string expansion.** Without this,
every deck would have to wrap them in `\texorpdfstring` by hand.

* `\speaker`, `\sspeaker` mark the speaker's name on the title page.
  `\@firstofone` keeps the name and drops only the markup, so the author still
  reaches the PDF `/Author` field.
* `\ccite`, `\cccite` say nothing in a bookmark, so they go entirely. Their
  replacement is expandable: an unexpandable one would have hyperref drop the
  name alone and leave `[p.~42]{key}` behind as literal text.
* `\uurl`, `\uuurl`, `\wwwurl` carry `\url`, whose catcode machinery does not survive
  expansion at all — unhandled, a URL in `\title` turns the PDF `/Title` into
  mojibake. `\@firstofone` keeps the address and drops the styling.
* `\ddoi`, `\dddoi` become `DOI:<doi>`: the number is worth having in the
  metadata, the resolver link is not. The replacement is expandable, so it
  cannot string its argument — see above.
* `\apicepubpar` is a decorative marker, so it is dropped, argument and all.
* `\translate` is beamer's translator hook. `\refname` is `\translate{References}`,
  so `\section*{\refname}` warns *Token not allowed in a PDF string*.
* `\\` — a line break inside `\title` or `\author` is meaningless in a PDF string.
  hyperref would drop it and run the two sides together, turning
  `Nobody Else\\someone@unibo.it` into `Nobody Elsesomeone@unibo.it`; mapping it
  to a space keeps the metadata readable.

## typography

*The faces of the `amsmerriweather` font theme, the `AMSUniBo` preset's; the other five presets keep
Computer Modern (`amscm`).*

Since 1.2 the style sets the faces as well as the colours, and still on
**pdfLaTeX**: every face below is a Type 1 font with T1 metrics. No Unicode
engine is involved, and a deck needs to do nothing — the theme loads all of it.

This is the style's only hard dependency beyond a TeX installation. It needs
`merriweather`, `inconsolata` and `newtxsf`, from `collection-fontsextra`, and
`anyfontsize`, from `collection-latexextra`. Both collections are in
`scheme-full`, but neither is in a minimal install such as BasicTeX. On TeX Live,
`tlmgr install merriweather inconsolata newtxsf anyfontsize` is enough.

<!-- markdownlint-disable MD013 -->
| role | face | how |
| --- | --- | --- |
| body, and anything not listed below | Merriweather Sans | `merriweather`, `sfdefault` |
| title, subtitle, frame titles | Merriweather serif | `merriweather`, `rm`, plus three `\setbeamerfont` |
| `\texttt` and `verbatim` | Inconsolata | `inconsolata`, `varqu,varl` |
| mathematics | sans math | `newtxsf` |

<!-- markdownlint-enable MD013 -->

**The pairing is the web theme's own** — Merriweather Sans for body text,
Merriweather serif for `h1`/`h2`. Earlier versions of this file claimed that
needed LuaLaTeX or XeLaTeX. That was simply wrong: the `merriweather` package
supports pdfLaTeX, and both families are complete — regular, bold, italic, bold
italic and small caps in each, with Light and Black besides — so a deck can reach
for any of them and get a real face rather than a silent substitution.

**Computer Modern is gone, deliberately**, because it was the weakest option in
both of the roles it was left holding. As a code face `cmtt` is at once the
*lightest* and the *widest* of the candidates, which is the wrong pair of
properties for frames full of long macro names: Inconsolata matches the body
weight, is 4% narrower, and `varqu` keeps its quotes straight — which matters
when every code sample is LaTeX. In mathematics, CM's delicate serif italic sits
badly beside a sturdy sans body, where `newtxsf` is a complete sans math font,
sums and integrals included. `anyfontsize` is loaded for one reason only: to
absorb the 5.5 pt and 6.5 pt size substitutions `newtxsf` and `wasysym` would
otherwise report.

**Size and weight both follow the web theme.** Merriweather's x-height runs large,
so at the same nominal size it reads bigger than Computer Modern Sans did;
`scaled=0.92` restores the old apparent size, and because the option touches only
the sans family the serif headings keep theirs. The body is then set at **weight
300**, as the web theme sets it.

Getting that weight takes three declarations rather than the obvious one, and the
order of discovery is worth recording. The package's `sflight` option alone does
nothing under Beamer, and neither does adding `\mddefault`: the package **resets
`\seriesdefault` to the serif family's series** near the end of its own code, so
that is the load-bearing one. All three together give a light body while leaving
the serif headings at Regular. Block titles are pulled back to medium
explicitly, so a block header still outweighs its own contents.

A light default has one consequence worth understanding: every font family now
gets asked for a `light` series, and a family that has none warns and falls back.
Three such families turn up here — `OT1/cmss`, the math sans `newtxsf` installs,
`T1/zi4`, the Inconsolata this theme loads for code, and `U/wasy`, if the deck
loads `wasysym` — and the theme declares the substitution for all three. Each has
to wait for its `.fd` file to load, hence the `\AtBeginDocument`. **If a deck adds
another symbol font that lacks a light series**, the same one-liner handles it:

```latex
\AtBeginDocument{\DeclareFontShape{<enc>}{<family>}{light}{n}{<->ssub*<family>/m/n}{}}
```

Inconsolata was the late addition, in 1.6.3: it has `m`, `b` and `bx` and no
`light`, but only a deck that typesets *text* in `\ttfamily` ever asks for the
shape — a `verbatim` or `lstlisting` body, not a `\mathtt` declaration — so the
warning waited for the first such deck. The fallback was always the right font,
`T1/zi4/m/n`; what the declaration removes is the noise.

It also brought one trap: `t1zi4.fd` is written in terms of `\zifour@`\* macros,
and `\AtBeginDocument` runs where `@` is not a letter, so a bare `\input` of it
fails with *Undefined control sequence* and the build produces no PDF at all.
NFSS loads an `.fd` inside its own `\makeatletter`; a hand-written `\input` has
to supply it — `\makeatletter\input{t1zi4.fd}\makeatother`. `uwasy.fd` needs
none, which is why the `wasysym` line beside it looks simpler.

**`\speaker` is bold, and that is a fix rather than a flourish.** The command
existed to single out the speaker among the authors, but it set `amsred` on a title
page whose author colour is *already* `amsred` — so from 1.0 to 1.1 it did nothing
visible at all. Weight is what distinguishes it now, which is only possible because
1.2 has a real bold. Note what it deliberately does **not** do: it leaves the author
colour alone, so decks that never call `\speaker` are untouched by it. Dimming the
co-authors instead would have recoloured every unmarked author in every deck.

`\sspeaker`, the short form that appears in the footline, had the same fault the
other way round. It was `amsgreyline` and italic, on a footline whose own text is
white — so it made the speaker *quieter* than the co-authors beside them, which
is the opposite of the command's purpose. It is now simply bold, with **no
colour of its own**: it inherits whatever surface it sits on, so it reads
white-on-green in the footline and dark on a light surface, and needs no
light-and-dark pair.

**Small caps.** Computer Modern Sans has no small-caps shape, so under it every
`\textsc` — `\textsc{Alma Mater Studiorum}` on a title page, say — fell back to
the *serif* small caps and warned
``Font shape `T1/cmss/m/sc' in size <n> not available``. Merriweather Sans has a
real small-caps shape, so this no longer arises. The substitution is still
declared, as a safety net for a deck that overrides the family back to Computer
Modern Sans.

## the references frame

An entry's citation key and its title used to read as the same kind of thing,
because they were the same colour at the same weight. The colour half was not a
decision: the title is `amsred` deliberately, while the key was `amsred` **by
inheritance** — beamer parents `bibliography item` on `item`, which this style
sets to red for bullets, and nothing here had ever named `bibliography item`. It
is now `amsgreymid`: a key is a pointer, not a bullet.

The weight half is done in the `.bst`, and deliberately not in the theme, which
was the first thing tried. Beamer parents `bibliography entry author`,
`location` and `note` on the *title's* font, so
`\setbeamerfont{bibliography entry title}{series=\bfseries}` bolds the author and
the location too — it flattens an entry rather than ranking it. Resetting those
three to `\mdseries` is worse still: with a light body weight that asks every
family for a light series, which Inconsolata does not have, so the build warned
and the wrong weight reached the PDF. That half of the argument expired in 1.6.3,
which declares the `T1/zi4` substitution; the flattening is what still rules
it out.

BibTeX, by contrast, knows which field is a title. `apalike-AMS.bst` therefore
gains `embolden`, a counterpart to the `emphasize` it already had, applied at the
two places a title is formatted: `format.title` for articles and `format.btitle`
for books, the latter keeping its italic and so becoming bold italic. One
cosmetic consequence, for the record: the full stop appended after a title falls
outside the bold and stays at body weight.

The last line of an entry holds the APICe marker and then the DOI or the URL, and
those two used to touch. The `.bst` does put two spaces between them, but BibTeX
wraps the `.bbl` line at exactly that point and the newline collapses them into
one space — set at `\tiny`, so it is narrower still, and `(APICe)DOI:10.…` reads
as a single token. The gap therefore belongs to `\apicepubpar`, which ends in a
`\mbox{~~~}` of its own; it sits *outside* the `\href`, so the link hotspot
stops at the word rather than covering the blank. The parentheses went with it:
the marker is a green sans word among grey monospace URLs and already looks like
a separate thing.

### subtitles

Since 1.7.2 `apalike-AMS.bst` reads a `subtitle` field, which APICe's
Publications write apart from the title, and prints it after the title past a
colon: *Multi-Agent Oriented Programming: Programming Multi-Agent Systems Using
JaCaMo*. The pair is treated as one title everywhere a title is
formatted—sentence case for a paper (BibTeX keeps the capital after the colon),
bold italic for a book, as written for a thesis from APICe's Theses. Sorting
still reads the title alone. An entry with no `subtitle` prints exactly as
before.

Since 1.7.3 a contained entry—`inproceedings`, `incollection`, `inbook`,
`conference`—with a `crossref` prints its title alone. BibTeX copies into such an
entry every field it lacks from the volume it points to, the volume's `subtitle`
included, so a chapter would otherwise wear its proceedings' subtitle, and in
sentence case at that. BibTeX cannot tell an inherited field from the entry's
own, so a contained entry with a `crossref` and a subtitle of its own loses it
too; one without a `crossref` keeps it.

### talks

Since 1.7.1 `apalike-AMS.bst` has a `talk` entry type, for the records APICe's
Talks application writes (`@talk{…}`). It reads the classical fields where they
mean what they mean elsewhere, and two of its own:

<!-- markdownlint-disable MD013 -->

| BibTeX field | from APICe's Talks | printed as |
| --- | --- | --- |
| `author`, `year` | authors, the date's year | label, sort key and the year after the names, as everywhere |
| `title` | title | bold, sentence case as for papers—protect capitals with braces, `{FIPA}` |
| `type` | the sort's label | the venue line's first word: *Talk*, *Invited Talk*, *Tutorial*, … |
| `howpublished` | context | the venue |
| `address` | place | after the venue |
| `date` | date, `yyyy-mm-dd` | last on the venue line, written out: *12 October 2004* |
| `speaker` | speakers | *Speaker:* or *Speakers:*, only when it differs from `author` |
| `note`, `url` | note, external link | as for every other type |
| `apice` | the page | the APICe marker, `\apicetalkpar`: it links the talk's short address, `talks.apice.unibo.it/<Name>`, where a publication's `\apicepubpar` links `pubs.apice.unibo.it/<Name>` |

<!-- markdownlint-enable MD013 -->

So a venue line reads *Tutorial, Tutorial on the Java Agent Development
Framework (JADE), IEEE SMC 2004, The Hague, The Netherlands, 12 October 2004*.
Everything else a Talks record carries—`annote`, `abstract`, `sort`, `language`,
the translations, `externallabel`, `slideshare`, `prezi`—is left unprinted.
`note` is the short bibliographic note, as in a publication; the talk's own
detail (session, room, chair) belongs in `annote`, which no style prints. A
record with no `date` simply ends its venue line earlier.

### journal issues

Since 1.8.2 `apalike-AMS.bst` has an `issue` entry type, for a whole journal
issue cited by its editors—a special issue, typically—which no classical type
holds: `article` has authors and no editors, and `proceedings` drops `number`
whenever `volume` is there.

<!-- markdownlint-disable MD013 -->

| BibTeX field | printed as |
| --- | --- |
| `editor`, `year` | label, sort key and the names, with *editors*, as for `proceedings` |
| `title` | the issue's title, bold, sentence case as for papers |
| `journal`, `volume`, `number`, `pages` | as in `article`: *Journal*, 14(1) |
| `publisher` | after the volume |
| `note`, `doi`, `url`, `apice` | as for every other type |

<!-- markdownlint-enable MD013 -->

So `@issue{…, editor = {Weyns, Danny and Parunak, H. Van Dyke}, title =
{Environments for Multi-Agent Systems}, journal = {Autonomous Agents and
Multi-Agent Systems}, volume = 14, number = 1, publisher = {Springer}, year =
2007}` reads *Weyns, D. and Parunak, H. V. D., editors (2007)* **Environments
for multi-agent systems** *Autonomous Agents and Multi-Agent Systems, 14(1),
Springer*. Other styles do not know the type: BibTeX warns and falls back to
`misc`.

### article numbers

Since 1.8.3 `apalike-AMS.bst` reads `articleno`, the article number APICe gives
journals that number their articles instead of paging them. Since 1.8.4 the
number replaces `pages` whenever it is there, since such pages count from 1
inside the article, and `numpages` follows it: *ACM Computing Surveys*, 47(3),
article 42, 36 pages for an `article`, and article 42, 36 pages where the pages
would go for any other type. Without `articleno`, `pages` print as before.

### web pages

Since 1.8.5 `apalike-AMS.bst` has a `webpage` entry type, also reached as
`@online`, `@www` and `@electronic`, for a web page cited as such: a tool's site,
a piece of documentation, a repository. Every field but a link may be missing,
so a bare entry needs nothing invented:

<!-- markdownlint-disable MD013 -->

| BibTeX field | printed as |
| --- | --- |
| `title` | bold, in the title's colour, **as written**: no sentence case, since a web page's title is usually a name (*MetalLB*). With no author or organisation it opens the entry |
| `url` | on its own line after the title, through `\wwwurl`: the colour of a journal's name, at the size of the references |
| `author`, else `organization` | first, with the year, as everywhere; `organization` beside an author goes on the venue line |
| `year`, else `date` | after the first item, `(2025)`, only when there is one |
| `howpublished`, `note` | the venue line, after the URL |
| `apice`, `doi` | the last line, as for every other type: the APICe marker, then the DOI |
| `urldate` | not printed, as in every type |

<!-- markdownlint-enable MD013 -->

The label is the author's, else `key`, else the organisation, else the title,
with `, <year>` only when there is a year; two equal labels with no year read
`[Kubernetes, a]` and `[Kubernetes, b]`, the letter in the year's place. So
`@webpage{docker, title = {Docker}, url = {https://www.docker.com/}}` reads
*[Docker]* **Docker** and the address below it. BibTeX warns only when an entry has
neither `url` nor `doi`. `@url` cannot be a type: `url` is a field, BibTeX refuses
a function of that name, and an entry so typed silently prints as `misc`;
`check/checkdeck.py` flags it.

Since 1.8.5 the `.bst` is one file, byte for byte the same in all six AMS styles:
its comments name no style.

### theses

APICe's Theses write `@phdthesis` and `@mastersthesis`, the classical types,
with fields of their own beside the classical ones. Since 1.7.1 the `.bst` reads
them; a record from Theses is recognised by its `cycle`, which nothing else
carries.

<!-- markdownlint-disable MD013 -->

| BibTeX field | from APICe's Theses | printed as |
| --- | --- | --- |
| `title` | title | as written, bold—bold italic for a PhD; never put into sentence case |
| `translatedtitle` | translated title | after the title, in brackets |
| `type` | the cycle's wording | *Bachelor's thesis*, *Master's thesis*, *PhD thesis*, as written |
| `supervisor`, `cosupervisor` | supervisors, co-supervisors | *Supervisor: A. Natali; Co-supervisors: A. Omicini and M. Viroli* |
| `amsphdeprint`, `amseprint` | the AMS Dottorato and AMS Laurea e-print numbers | the link, when there is neither `doi` nor `url`: `amsdottorato.unibo.it/id/eprint/<n>/`, `amslaurea.unibo.it/id/eprint/<n>/` |
| `apice` | the page | `\apicethesispar`, linking `apice.unibo.it/bin/view/Thesis/<Name>`—no short address works for a thesis yet |

<!-- markdownlint-enable MD013 -->

The rest—`abstract`, `keywords`, `reviewer`, `opponent`, `contact`, `cycle`,
`language`, `description`, `amspractice`, `start`, `available`—is not printed. A
thesis that comes from APICe's Publications instead (no `cycle`) is a
publication and keeps `\apicepubpar` and the classical rules.

Names other than the authors—supervisors, speakers—are printed as said, *A.
Natali*; the author list keeps *Natali, A.*

## the palette

*The `amsunibo` colour theme, the `AMSUniBo` preset's; the other palettes and their sources are in their own
repositories' READMEs (see [usage](#usage)).*

Every value is the one used by the AMSUniBo theme on APICe, and each is used in
the role its web counterpart has there. Red is the identity colour — the navbar,
links, primary actions. Green is the structural colour — rules, separators,
headings, tabs.

<!-- markdownlint-disable MD013 -->
| colour | value | web theme | where it goes on a slide |
| --- | --- | --- | --- |
| `amsred` | `#BB2E29` | `@ams-red`, `navbar-default-bg`, `link-color` | head line, author, bullets, alerted text, URLs, DOIs, alerted block headers |
| `amsreddark` | `#8E2320` | `@ams-red-dark`, `navbar-default-link-active-bg` | reserved for active states |
| `amsblack` | `#000000` | `@ams-black`, `headings-color` | title, frame titles |
| `amstext` | `#040404` | `@ams-text`, `text-color` | body text |
| `amsgreen` | `#56A49A` | `@ams-green`, `brand-success` | separation lines; the base the example-block fills are derived from |
| `amsgreenlight` | `#74BDAD` | `@ams-green-light`, `brand-info` | reserved |
| `amsgreendark` | `#366861` | `@ams-green-dark`, `state-success-text` | structure, block headers, emphasis, section in TOC |
| `amsgreentint` | `#DDEDEB` | `@ams-green-tint`, `breadcrumb-bg`, `.fieldrow1` | frame title band, block bodies, foot line |
| `amsgreentint2` | `#CCE4E1` | `@ams-green-tint2`, selected tabs | foot line, frame title right |
| `amsgrey` | `#464A51` | `@ams-grey` | institute |
| `amsgreymid` | `#535353` | `@ams-grey-mid`, `breadcrumb-color` | secondary text, footnotes, subtitle, date |
| `amsgreyline` | `#C7C9CB` | `@ams-grey-line`, `table-border-color` | `\ccite` and the doubled URL, DOI and APICe commands on a light surface, `\alert` and `\aalert` on a dark one |
| `amsgreybg` | `#F0F1F1` | `@ams-grey-bg` | citations, URLs, DOIs, APICe addresses on a dark surface |

<!-- markdownlint-enable MD013 -->

`amsredfill`, `amsredborder`, `amsgreenfill` and `amsgreenborder` are the block
fills, computed exactly as the web theme's LESS computes its `@state-danger-*`
and `@state-success-*` values. `block` and `alertblock` take a solid header, as
the wiki's panels and primary buttons do; `exampleblock` takes the lighter
pairing the wiki uses for its own success alerts, `amsgreenborder` over
`amsgreenfill`.

Two contrast facts inherited from the web theme, and observed here: **white on
`#56A49A` is 2.93:1 and fails WCAG AA**, so every full-green surface carries dark
text instead; white on `#BB2E29` is 5.94:1 and passes. Every text-on-fill pair in
this style is at AA or better, except the deliberately quiet `\alert` and
`\aalert` on a block header, 3.82:1; citations and addresses there reach
5.61:1. `\sspeaker` was in that set until 1.2 and is no longer: it now inherits
its surface's colour, which *raises* its contrast to whatever the surrounding
text has. Citations in running text are fainter still, which is how
AMSBolognaFC renders them too.

### where the colours come from

* **Red and black** — *Sistema di identità di Ateneo*, "I colori istituzionali":
  rosso istituzionale, Pantone 1805, C0 M91 Y100 K23.
* **Grey `#464A51`** — the same manual, p. 16, "La versione in negativo".
* **Green** — *Brochure di Ateneo 2026*, the cover dots and the closing page.
* **Green light** — the official *PPT Unibo 2026* template.
* **Body text** — the same PPT templates.
* The rest are derived, as the table above records.

Note the drift in the sources: the brochure and the PowerPoint templates both
use `#BC2802` / `#BD2B0B`, which is the institutional red as naively converted
from its CMYK build. The manual's own stated HEX, `#BB2E29`, is the one meant
for screen, and is the one used here.

The manual's 16 disciplinary-area colours — for Ambiti, Dipartimenti and
Scuole — are deliberately **not** used: they identify structures, not the
Ateneo.

## versioning

The version is declared in `beamerthemealmamater.sty` as `\stylemajor` / `\styleminor` / `\stylepatch`, giving
`Major.Minor[.Patch]`; `\stylepatch` is optional. One version for the family, from **2.0.0** (Andrea, 2026-11-08);
each PDF records what built it in its Info dictionary, `/Style (almamater 2.0.0, <colour theme>, <font theme>)`.

Releases are tagged `Major.Minor[.Patch]-<UTC time-stamp>`, the time-stamp appended by the CI, so two commits
that both forget to bump the version still make two distinct releases.

## licence

This work is distributed under the
[LaTeX Project Public License](LICENSE), version 1.3c or later, and has the
LPPL maintenance status `maintained`.

One file is **not** covered by that licence: `apalike-AMS.bst` is a modified,
renamed derivative of Oren Patashnik's `apalike.bst` (Copyright © 1988, 2010
Oren Patashnik) and remains subject to its own terms, which permit modification
and redistribution provided the resulting file is renamed — as it is here.

The colours are those of the Alma Mater Studiorum's institutional identity, taken
from *Sistema di identità di Ateneo* and the 2026 institutional documents. Their
use is governed by the Ateneo's own rules, not by the licence above.
