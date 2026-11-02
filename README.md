# CSE 481 — Engineering Economics

Akdeniz University · Computer Engineering (English) · Semester 7

**An open study archive for this course.** A week-by-week plan following the
2026-2027 instructor's roadmap, the instructor's slides, project brief and starter
code, the official syllabus topics, and a completed term project from a previous
student.

**Instructor (Fall 2026-2027):** Dr. Alper Özcan · Course communication on Microsoft Teams

The 2026-2027 course is **BIST 100 financial analytics with Python and MCP AI
agents**: market data → indicators → support/resistance → backtest → AI agent. The
**Weeks 5–6 cover engineering economics and economic equivalence:** feasibility,
costs, interest and cash-flow comparison. Start with the
[midterm study guide](exams/midterm-preparation.md). The
official syllabus's economics topics are kept in
[`syllabus-topics.md`](syllabus-topics.md) as written-exam background.

## Grading

| Component | Count | Weight |
|-----------|-------|--------|
| Midterm | 1 | 20% |
| Quiz | 1 | 10% |
| Term project | 1 | 30% |
| Final | 1 | 40% |

Midterm: **7 multiple-choice questions in 40 minutes**; own calculator allowed
(no sharing), interest factor table and some Turkish terminology provided, no extra
paper. [Instructor announcement](resources/2026-2027-fall/midterm-announcement.md).
Quiz: short checks for weekly learning ·
Project: must be implemented in Python · Final: comprehensive.

## Term project — 30%

**Integrated BIST 100 Agentic Financial Analytics Harness** —
[project brief](resources/2026-2027-fall/term-project-brief.pdf) (Dr. Alper Özcan).

- **Due November 24, 2026, 23:59** on Teams (multiple submissions allowed).
- Proposal + final report; groups of two are allowed; Python.
- Build an educational analysis system for a 30-stock BIST 100 universe that combines
  deterministic Python tools, multiple evidence sources, backtest verification and a
  controlled MCP AI-agent workflow — not a single prediction model.
- Four mandatory research scenarios: sector laggard / catch-up, weekday and multi-day
  patterns, technical reversal events, quarterly fundamentals and price reaction.
- *LLM reasons and explains. Python tools calculate. The harness controls. Backtests
  verify. Evidence is logged. A human makes the final decision.* Strictly educational:
  no broker connection, no real orders, no investment advice.
- Starter code: [`scenario2_thyao_weekday_patterns.py`](resources/2026-2027-fall/code/scenario2_thyao_weekday_patterns.py),
  [`scenario3_technical_reversal_events_3_periods.py`](resources/2026-2027-fall/code/scenario3_technical_reversal_events_3_periods.py).
- A previous student's stock technical-analysis project:
  [`assignments/undated-term-project/`](assignments/undated-term-project/).

Instructor's answers on Teams:
- **Team size:** individually or in groups of two.
- **Data source:** Yahoo Finance / yfinance is only the example. Any reliable, legally
  accessible source is fine; document the source, the date range, the adjustments
  applied and how missing data is handled.
- **News and speech layer:** part of the architecture. KAP disclosures suit
  company-specific events well because they carry official disclosure timestamps
  (financial results, material events, disclosure dates). Speech-to-text may stay small,
  on selected, instructor-approved examples. Text is timestamped contextual evidence,
  not a replacement for numerical financial data.
- **TMS 29 (inflation accounting):** non-bank companies report under TMS 29 after 2024,
  so mixing older nominal statements with the inflation-adjusted ones is misleading.
  Keep the main analysis on post-TMS 29 periods that are consistent with each other;
  tests may use data from 1 January 2025 to November 2026.
- **Model for the harness experiments:** no LLM is mandatory. Keep one model fixed and
  compare the architecture stages: Raw LLM → LLM + Tools → Tools + Stateful Harness →
  + Evidence/Quality Gate → + Memory + Human Review. The question is how much more
  reliable and reproducible the system gets at each stage, not which LLM is better.
- **Harness papers:** [`resources/2026-2027-fall/papers/`](resources/2026-2027-fall/papers/).

## Quiz — 10%

**BIST Algorithmic Trading Challenge** —
[brief](resources/2026-2027-fall/quiz-bist-algo-trading-challenge.pdf): a Python
backtesting assignment, open on Teams for 12 hours from 13:30 on a Tuesday. Questions
about it are taken in class only; none are accepted after the class.

- One rule-based strategy, applied unchanged to six stocks (AKBNK, ASELS, TUPRS, TCELL,
  FROTO, EREGL), 1 January 2025 – 1 October 2026, 100,000 TL initial capital per stock.
- Every stock has to beat its own benchmark; total portfolio profit does not count.
- At least 3 completed trades per stock, no look-ahead, at least one risk-management
  mechanism (stop-loss, ATR stop, trailing stop, maximum holding period, …).
- You may use or improve the four strategies from the
  [week 3 slides](resources/2026-2027-fall/week-03-bist-trading-strategies.pdf) — Volume
  Bubbles, Liquidity Swings, Support & Resistance Channels, Dual-Phase Reversal — or
  design your own.
- Submit a Jupyter notebook with code and outputs visible: every buy and sell time and
  price, profit or loss per trade, trade charts, the required metrics (net profit, final
  capital, total / winning / losing trades, win rate, maximum drawdown, profit factor,
  average trade), the benchmark comparison and the final analysis question.
- **Individual work.** AI tools may assist, but the implementation, decisions and
  analysis must be your own. Submissions with unusually similar code, parameters, trade
  sequences, figures or results may be reviewed for academic integrity (an identical
  final profit alone is not evidence), and you may be asked to explain, justify or
  modify any part of your code in an individual review.

## Weekly plan

Weekly topics and links to the instructor material.
See the [resource guide](resources/2026-2027-fall/README.md) for the slides.

| # | Topic | Note |
|---|-------|------|
| 1 | BIST 100 and Yahoo Finance | [weeks/01](weeks/01-bist-100-and-yahoo-finance.md) |
| 2 | Algorithmic Trading and the Agentic Harness | [weeks/02](weeks/02-algorithmic-trading-and-agentic-harness.md) |
| 3 | Technical Indicators | [weeks/03](weeks/03-technical-indicators.md) |
| 4 | Backtesting Strategies | [weeks/04](weeks/04-backtesting-strategies.md) |
| 5 | Engineering Economics Concepts and Computer Engineering Examples | [weeks/05](weeks/05-time-series-with-pandas.md) |
| 6 | Economic Equivalence | [weeks/06](weeks/06-lab-bist-data.md) |
| 7 | Lab: Support and Resistance | [weeks/07](weeks/07-lab-support-and-resistance.md) |
| 8 | Midterm | [weeks/08](weeks/08-midterm.md) |
| 9 | Engineering Economics Concepts | [weeks/09](weeks/09-engineering-economics-concepts.md) |
| 10 | Fundamental Analysis and Valuation | [weeks/10](weeks/10-fundamental-analysis-and-valuation.md) |
| 11 | Money Management | [weeks/11](weeks/11-money-management.md) |
| 12 | MCP AI Agent | [weeks/12](weeks/12-mcp-ai-agent.md) |
| 13 | Project Presentations I | [weeks/13](weeks/13-project-presentations-i.md) |
| 14 | Project Presentations II | [weeks/14](weeks/14-project-presentations-ii.md) |

## How to study with this repository

**1. Open the week you are on** in [`weeks/`](weeks/): goals, key concepts from the
slides, readings, and a practice list with the code to run.

**2. Practise the examples.** For economics, draw the timeline, choose the factor
and calculate using the table. For financial analytics, use Python —
`pip install yfinance pandas matplotlib` in a virtual environment and reproduce
the slide examples.

**3. Start the project early** — it is 30%, more than the midterm, and due November 24.

**4. For the midterm**, use the [study guide](exams/midterm-preparation.md) and
[Lab review](https://akdenizos.org/lab/cse-481/midterm-review.html), including W5–W6
costs, interest and equivalence. For wider economics background, the official topics are in
[`syllabus-topics.md`](syllabus-topics.md) with book links at the exact page.

**5. Write under your own `## Notes — <Name> (<term>)` section** at the bottom of each week note — see [Taking notes](#taking-notes).

## Books

Two openly licensed textbooks are in this repository; every reading link in
[`syllabus-topics.md`](syllabus-topics.md) opens one of them at the exact page.

| Book | Covers | Licence |
|------|--------|---------|
| [OpenStax, *Principles of Economics* 3e](resources/books/openstax-principles-of-economics-3e.pdf) — 995 pp. | Syllabus topics 1-11 | CC BY-NC-SA 4.0 |
| [Schmid & Vanderby, *Engineering Economics*](resources/books/schmid-vanderby-engineering-economics.pdf) — 254 pp. | Syllabus topics 12-14, week 9 | CC BY 4.0 |

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
course-info.md   Resource map (books, syllabus topic → chapter), Turkish ↔ English glossary
syllabus-topics.md  The official syllabus's 14 economics topics, with book links
weeks/NN-*.md    One file per week: the shared plan on top, everyone's notes below
exams/           Past papers (none collected yet) and how to add one
resources/       Syllabus PDF, books/, 2026-2027-fall/ (slides, project brief, quiz brief, papers/, code/)
assignments/     Term projects and other own work — including a previous student's project
```

## Taking notes

Open the week, scroll to the bottom, write under your own heading:

```markdown
## Notes — <Name> (<term>)
### Lecture
### Code
### Questions
### Exam-worthy
```

Add your heading below the existing ones and never edit someone else's section —
different sections merge in git without conflicts.

## Who changes what

| What | Who edits it | When |
|------|-------------|------|
| Top of `weeks/NN-*.md` and `syllabus-topics.md` | **anyone** | Only when the course itself changes — a new topic, a better reading, a correction. |
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
| Fall 2026-2027 | Dr. Alper Özcan | TBD | Week 8 | TBD | Slides, project brief, papers and starter code in [`resources/2026-2027-fall/`](resources/2026-2027-fall/); project due Nov 24, 2026; Efe — in every week file |
| Undated | — | — | — | — | A completed term project by a previous student: [`assignments/undated-term-project/`](assignments/undated-term-project/) |

Grading in Fall 2026-2027: Midterm 20% · Quiz 10% · Project 30% · Final 40%.
