# Midterm preparation — Fall 2026–2027

## Confirmed format

From the [instructor's Teams announcement](../resources/2026-2027-fall/midterm-announcement.md):
**7 multiple-choice questions, 40 minutes**. Bring your own calculator; sharing it
is forbidden. An interest factor table and Turkish equivalents of some economic
terms will be provided. No extra paper will be provided. Practise compact workings.
The announcement does not specify the date, exact topic distribution, calculator
model restrictions, or permission to bring your own notes.

## Study priorities based on the available slides

Start here without assuming prior study. Learn the W5 concepts first, then cash-flow
timelines and W6 table factors, then attempt the timed test. The priorities below
are a study recommendation based on the slides, not an official scope announcement.

1. **W5 concepts and costs:** [analysis slides](../resources/2026-2027-fall/week-05-engineering-economics-analysis.pdf)
   pp. 2–23; [computer-engineering examples](../resources/2026-2027-fall/week-05-engineering-economics-computer-engineers.pdf)
   pp. 3–13. Life cycle; market, technical and economic feasibility; fixed/variable,
   recurring/non-recurring, sunk/opportunity costs. Sunk costs are excluded from
   today's choice; opportunity cost is the value of the best forgone alternative.
   Fixed and recurring describe different dimensions: an annual licence can be both.
2. **W5 money over time:** analysis pp. 24–45; computer-engineering examples pp. 14–20.
   Cash-flow signs, period-end convention, principal, interest, simple versus compound
   interest. Simple payback = investment / constant annual net savings; it ignores
   discounting and later cash flows. Cloud/server break-even in the example is
   40,000 / (0.01 − 0.002) = 5,000,000 requests for a common cost horizon.
3. **W6 equivalence:** [slides](../resources/2026-2027-fall/week-06-economic-equivalence.pdf)
   pp. 3–25 single payments; pp. 27–51 equal series; pp. 53–69 uneven series.
   Bring every cash flow to a common date at the stated rate. Know which factor
   column to use and where its result lies on the timeline.
4. **Earlier material:** W1–W3 slides, backtest pitfalls, harness roles and the seven
   distinctions in project brief §38 remain useful revision. Their share of the
   seven exam questions has not been announced. A project learning objective is
   not a confirmed exam question.

## Interest table: choose the column before calculating

Notation is **wanted / given**. With rate `i` per period and `n` periods:

| Want, given | Table factor | Calculation |
|---|---|---|
| F, P | F/P | F = P(1+i)^n |
| P, F | P/F | P = F/(1+i)^n |
| F, equal A | F/A | F = A[(1+i)^n−1]/i |
| A, F | A/F · sinking fund | A = Fi/[(1+i)^n−1] |
| P, equal A | P/A | P = A[1−(1+i)^−n]/i |
| A, P | A/P · capital recovery | A = Pi/[1−(1+i)^−n] |

These series factors assume payments at `t=1,…,n`. P lies **one period before the
first A**, F at the last A. For an annuity due with the same payment count, move
each payment one period earlier; value at a fixed comparison date is multiplied
by `(1+i)`. A deferred series must be discounted again to `t=0`.
Match rate and payment periods. At `i=0`, use the limits: F=P, F=nA, P=nA,
A=F/n or P/n. For irregular flows, `PW = Σ C_t/(1+i)^t`, including `C_0`.

Examples checked independently (table rounding can change the last digits):

- W6 p. 24: 20,000(F/P,10%,5) = 32,210.20; four-decimal table ≈ 32,210.
- W6 p. 25: 30,000(P/F,8%,5) = 20,417.50; table ≈ 20,418.
- W6 p. 37: 3,000(F/A,7%,10) = 41,449.34; table ≈ 41,449.20.
- W6 p. 42: 5,000(A/F,7%,5) = 869.45; table ≈ 869.50.
- W6 p. 48: 250,000(A/P,8%,6) = 54,078.85; table ≈ 54,075.
- W6 p. 68: 25,000(P/F,10%,1) + 3,000(P/F,10%,2) +
  5,000(P/F,10%,4) = 28,621.68.

Arithmetic/geometric gradients are listed on W6 p. 17, but the worked teaching
sections cover single, equal and uneven flows. Detailed NPV/IRR/MIRR and other
book extensions on the Lab are not established as midterm topics by this batch.

## Compact English ↔ Turkish vocabulary

| English | Türkçe |
|---|---|
| feasibility; life cycle | yapılabilirlik/fizibilite; yaşam döngüsü |
| fixed / variable cost | sabit / değişken maliyet |
| recurring / non-recurring cost | düzenli tekrarlayan / düzenli tekrarlamayan maliyet |
| sunk / opportunity cost | batık / fırsat maliyeti |
| principal; interest rate | anapara; faiz oranı |
| present / future worth | bugünkü / gelecek değer |
| receipt / disbursement | tahsilat / ödeme |
| inflow / outflow | nakit girişi / çıkışı |
| uniform / uneven series | eşit / düzensiz seri |
| end / beginning of year | yıl sonu / yıl başı |
| sinking fund / capital recovery | birikim fonu / sermaye geri kazanımı |

Only **some** Turkish equivalents are promised in the exam; the exact list is unknown.

## Practice

[AkdenizOS Lab midterm review](https://akdenizos.org/lab/cse-481/midterm-review.html)
contains revision and a **7-question, 40-minute practice test** with a sample
factor table and explanations after submission. It is student-created practice,
not a past paper or a prediction of the exam's topic distribution. Aim for an
initial pass in 28 minutes, a second pass in 9, and 3 minutes for checking. Average
time is about 5 minutes 43 seconds per question; questions need not have equal weight.
