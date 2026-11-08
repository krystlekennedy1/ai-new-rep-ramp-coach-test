# Results summary

Scored against `keys/answer_key.csv`. 16 flag rows, 9 decoys, 3 human-look rows.

| Measure | A1 | A2 | A3 | B1 | B2 | B3 |
|---|---|---|---|---|---|---|
| FLAG rows clearly caught (of 16) | 10 | 11 | 12 | 16 | 16 | 16 |
| Partly caught | 4 | 3 | 3 | 0 | 0 | 0 |
| Missed | 2 | 2 | 1 | 0 | 0 | 0 |
| Decoys flagged (of 9) | 3 clear, 3 soft | 4 clear, 2 soft | 4 clear, 2 soft | 0 | 0 | 0 |
| Human-look items correct (of 3) | 0 | 1 | 1 | 3 | 3 | 3 |
| Tier C exception respected | No | No | No | Yes | Yes | Yes |
| Invented reps or numbers | None | None | None | None | None | None |
| Supportive tone | Yes | Yes | Yes | Yes | Yes | Yes |

"Partly caught" means the rep appeared in the output, but under the wrong label (for example, a rep who closed ahead of pace listed under "coach first") or as a watch item, not as the rule's flag.

## Findings

1. The vague prompt found the main patterns every time: low meeting conversion, one rep with no close after 99 days, and the data-order problems. It read supportive and never labeled a rep as poor.
2. It never respected the tier C exception. Both reps whose gaps may be explained by territory were listed as coaching targets in all three runs.
3. It flagged between 4 and 6 of the 9 decoys in each run, mostly the exact-at-threshold ones.
4. It missed or underplayed the reps who were ahead of pace. One rep with a first close well ahead of p25 never received recognition in any run.
5. It invented its own cutoffs ("under 75% of the median", "under 60% of the median"), and they differed from run to run. The same data could produce different priority lists.
6. Without an as-of date, Prompt A counted one day later than the data. That moved reps who sit exactly at p75 over the line and into the coaching list.
7. The structured prompt matched the key on every row in all three runs. The exact-at-threshold cases and the tier C exception held every time.
8. Structured does not mean error-free. In run B2 the headline said two reps were ahead of pace while the table listed three.
9. A separate reviewer that had the data but not the rules (`extra_review_pass.txt`) recommended adding a false flag for a rep who is correctly excluded by the 100-call rule. Any AI check step has to be given the same rules as the step it checks.
