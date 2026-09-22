# CSE 481 — Engineering Economics

Akdeniz University · Computer Engineering (English) · Semester 7

**An open study archive for this course.** A week-by-week plan built from the
official syllabus, plus a completed term project from a previous student to show
what one looks like.

The course is two halves: **weeks 1-11 are general economics** (micro then macro),
**weeks 12-14 are engineering economics proper** — evaluating design alternatives
in money terms.

## Grading

| Component | Count | Weight |
|-----------|-------|--------|
| Midterm | 1 | 20% |
| Quiz | 1 | 10% |
| Term project | 1 | 30% |
| Final | 1 | 40% |

The project is worth more than the midterm. Start it early — see
[`assignments/undated-term-project/`](assignments/undated-term-project/) for a worked example.

## Weekly plan

| # | Topic | Note |
|---|-------|------|
| 1 | Scarcity, trade-offs, opportunity cost | [weeks/01](weeks/01-scarcity-and-choice.md) |
| 2 | Production factors and economic sectors | [weeks/02](weeks/02-production-and-sectors.md) |
| 3 | Trade, competition, economic systems | [weeks/03](weeks/03-trade-and-markets.md) |
| 4 | Supply, demand, market failure | [weeks/04](weeks/04-supply-demand-market-failure.md) |
| 5 | Living standards and productivity | [weeks/05](weeks/05-living-standards-productivity.md) |
| 6 | Money, inflation, unemployment | [weeks/06](weeks/06-money-inflation-unemployment.md) |
| 7 | Interest rates, exchange rates, deficits | [weeks/07](weeks/07-interest-exchange-deficits.md) |
| 8 | Monetary policy and productivity measures | [weeks/08](weeks/08-monetary-policy-productivity.md) |
| 9 | Production possibilities and efficiency | [weeks/09](weeks/09-production-possibilities.md) |
| 10 | Markets, monetary and fiscal policy | [weeks/10](weeks/10-markets-and-policy.md) |
| 11 | International finance | [weeks/11](weeks/11-international-finance.md) |
| 12 | The engineering decision-making process | [weeks/12](weeks/12-engineering-decision-making.md) |
| 13 | The engineer's role in business | [weeks/13](weeks/13-engineers-in-business.md) |
| 14 | Real-world engineering economic decisions | [weeks/14](weeks/14-real-world-decisions.md) |

## How to study with this repository

**1. Open the week you are on** in [`weeks/`](weeks/). This course is definitional —
each note lists the terms in bold with a one-line meaning. If you can define every
bolded term in a week, you know that week.

**2. Tie every concept to a real example.** The syllabus explicitly says the Turkish
economy is used throughout. Inflation, exchange rates and the TCMB are in the news
daily; use them. [TÜİK](https://www.tuik.gov.tr/) has the data.

**3. Watch the three computational bits.** Most of the course is verbal, but
productivity formulas (week 8), the production possibilities curve (week 9), and
the engineering decision methods (weeks 12-14) are where the calculations are.

**4. Start the project early** — it is 30%, more than the midterm.

**5. Write under your own `## Notes — <Name> (<term>)` section** at the bottom of each week note — see [Taking notes](#taking-notes).

## Books

Two openly licensed textbooks are in this repository, and every reading link in
`weeks/` opens one of them at the exact page.

| Book | Covers | Licence |
|------|--------|---------|
| [OpenStax, *Principles of Economics* 3e](resources/books/openstax-principles-of-economics-3e.pdf) — 995 pp. | Weeks 1-11 | CC BY-NC-SA 4.0 |
| [Schmid & Vanderby, *Engineering Economics*](resources/books/schmid-vanderby-engineering-economics.pdf) — 254 pp. | Weeks 12-14 | CC BY 4.0 |

Neither is the syllabus's cited book, but between them they cover the whole course:
OpenStax follows the same micro-then-macro path as Mankiw, and Schmid & Vanderby
covers the time value of money and project evaluation that Chan S. Park does.

Also cited by the syllabus, not here: Mankiw *Principles of Economics* /
*Principles of Macroeconomics*, Chan S. Park *Fundamentals of Engineering
Economics*, Okka *Mühendislik Ekonomisine Giriş* (TR), Samuelson & Nordhaus
*Economics*.

Statistics: [TÜİK](https://www.tuik.gov.tr/), [Eurostat](https://ec.europa.eu/eurostat), [OECD](https://stats.oecd.org/).

## Layout

```
README.md        This page
course-info.md   Resource map (books, week → chapter), Turkish ↔ English glossary
weeks/NN-*.md    One file per week: the shared plan on top, everyone's notes below
exams/           Past papers (none collected yet) and how to add one
resources/       Syllabus PDF, books/
assignments/     Term projects and other own work — including a previous student's project
```

## Taking notes

Open the week, scroll to the bottom, write under your own heading:

```markdown
## Notes — <Name> (<term>)
### Lecture
### Worked out by hand
### Questions
### Exam-worthy
```

Add your heading below the existing ones and never edit someone else's section —
different sections merge in git without conflicts.

## Who changes what

| What | Who edits it | When |
|------|-------------|------|
| Top of `weeks/NN-*.md` (goals, reading, practice) | **anyone** | Only when the course itself changes — a new topic, a better reading, a correction. |
| `## Notes — <you>` in a week file | **only you** | Every week. This is your notebook. |
| `course-info.md`, `exams/README.md` | **anyone** | When you learn something durable: a new exam pattern, a better source. |
| `assignments/<term>-<you>/` | **only you** | Your assignments, projects, submissions. |
| `resources/<term>/` | **anyone in that term** | Slides, syllabus and lab sheets the instructor issued. |
| `exams/` | **anyone** | When you get hold of a new paper — blank or answered. Put the writer's surname in the filename (`2026-2027-final-answered-<surname>.pdf`). Exam papers never go under `assignments/`. |

Two students in different years never touch the same file except to improve the
shared plan — which is the point.

## Contributing

Add your term to the table below with the instructor and dates, write your notes in
the week files, and put your project under `assignments/<term>-<you>/`. Keep the
shared plan in `weeks/` and `course-info.md` general.
Use a lowercase, hyphenated name in folder names — `efe-kurucay`, not `Efe Kuruçay`.

Previous students' work is here as **reference**, not to hand in.

## Terms

| Term | Instructor | Schedule | Midterm | Final | Notes |
|------|-----------|----------|---------|-------|-------|
| Fall 2026-2027 | TBD — fill in during week 1 | TBD | TBD | TBD | Efe — in every week file; project to come |
| Undated | — | — | — | — | A completed term project by a previous student: [`assignments/undated-term-project/`](assignments/undated-term-project/) |

Grading in Fall 2026-2027: Midterm 20% · Quiz 10% · Project 30% · Final 40%.
