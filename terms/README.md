# Terms

One folder per cohort. Everything belonging to a single run of the course — that
term's project, notes and submissions — lives in its own folder.

| Term | What is here |
|------|-------------|
| [undated](undated/) | A completed term project by a previous student |

## How a term folder is laid out

```
terms/2026-2027-fall/
├── README.md          instructor, dates, and who took the course this term
├── course/            what the instructor gave everyone: syllabus, slides, lab sheets
├── people/
│   ├── efe-kurucay/   one folder per person
│   │   ├── notes/week-01.md …
│   │   ├── assignments/
│   │   └── exams/
│   └── zeynep-yilmaz/
└── unattributed/      material from this term whose author is not known
```

`course/` is shared by everyone in that term. `people/<name>/` belongs to one
person and nobody else edits it. Several students in the same term work side by
side without ever touching the same file.

Use a lowercase, hyphenated folder name — `efe-kurucay`, not `Efe Kuruçay`.

Copy [`_notes-template/_template.md`](_notes-template/_template.md) into your own
`notes/` folder when you start a week.
