# Scoring guide

DO NOT ATTACH THIS FILE (or anything in keys/ or source/) to a test chat. It describes the answers.

The key (`keys/answer_key.csv`) has three kinds of rows:
- FLAG (16 rows across 15 reps): the brief should flag these.
- DO_NOT_FLAG (9 rows): decoys that look like problems but do not meet the rule. Flagging one is a "trap hit".
- NEEDS_HUMAN_LOOK (3 rows): the best outcome is listing them under "Needs a human look".

| Measure | A1 | A2 | A3 | B1 | B2 | B3 |
|---|---|---|---|---|---|---|
| FLAG rows caught (of 16) | | | | | | |
| FLAG rows missed | | | | | | |
| Trap hits (decoys flagged, of 9) | | | | | | |
| Flags not in the key at all | | | | | | |
| Human-look items placed correctly (of 3) | | | | | | |
| Wrong evidence (days, dates, counts) | | | | | | |
| Invented reps or numbers | | | | | | |
| Coaching tone (supportive, no labeling people) | | | | | | |

Formulas: recall = caught / 16. Precision = caught / (caught + trap hits + flags not in key).

## What the decoys test

- Xenia Whitaker: 3 meetings from 90 calls. Low rate, but under the 100-call minimum.
- Xenia Hayes: meeting rate exactly half of the benchmark. The rule needs less than half.
- Pedro Jacobs and Luca Iverson: days in seat exactly equal to p75. The rule needs more than p75.
- Tessa Santos (10 days) and Farid Hayes (13 days): under the 14-day minimum.
- Tessa Hayes and Farid Santos: late on first call, but every milestone is now achieved.
- Farid Fischer: first close one day slower than p25, so not ahead of pace.

## What the human-look rows test

- Xenia Vasquez and Luca Gallagher: meet the behind-pace rule, but territory tier is C, so a person decides.
- Pedro Morales: segment is blank, so no benchmark can be chosen.

## Compare across runs

- Are the same reps flagged every time?
- Do the exact-at-threshold cases flip between runs?
- Does the tier C exception hold?
- Does the output recognize reps who are ahead of pace?

## Note on the as-of date

Prompt A gives no date, so the model uses its own clock. In these runs that was one day after the dataset's date, which pushed every days-in-seat figure up by one and moved the exact-at-p75 reps over the line.
