# Results

Six scored runs: three of Prompt A, three of Prompt B. Each was a fresh chat with only `new_reps.csv` and `benchmark_summary.csv` attached.

| File | Prompt | Status |
|---|---|---|
| A1.txt, A2.txt, A3.txt | A (vague) | Valid |
| B1.txt, B2.txt, B3.txt | B (structured) | Valid |
| extra_review_pass.txt | Reviewer check of a B brief | Not scored. Kept because of what it shows. |

## Runs that were discarded

Four earlier runs (two of each prompt) used an earlier version of `new_reps.csv`. In that version, nine reps had call and meeting counts that contradicted their blank milestone dates (for example, meetings logged but no first-meeting date). That was an error in the data generator, and it made some cases genuinely ambiguous. The generator was fixed to keep counts consistent with the dates, the data was re-verified against the key, and all runs were repeated. Those four runs are not included and are not part of any number in this repo. Both prompts behaved the same way on them as on the corrected data, apart from the structured prompt treating the contradictory reps as either flags or human-look cases.

The outputs were copied from the chat window into text files. Tables were reformatted. Wording is unchanged, except for bracketed scoring notes where labeled.
