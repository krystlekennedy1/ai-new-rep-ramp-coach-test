# New-Rep Ramp Coach: Vague vs Structured Prompt Test

Can an AI tell a sales manager which new reps need coaching, which are on track, and which are ahead, without penalizing the wrong people?

This is a small, scored experiment on **synthetic data**. All reps, managers, and numbers are fictional. No real company, employee, or customer data is used anywhere in this repo.

## The setup

- 45 synthetic new reps (SMB and Commercial) with the days it took each to reach first call, first meeting, first opportunity, and first close, plus calls and meetings to date.
- A benchmark file with p25, median, and p75 days for each milestone and the normal meeting rate, built from 200 synthetic past reps.
- Planted in the data: reps behind pace, reps with a low meeting rate, reps ahead of pace, data-order errors, exact-at-threshold decoys, reps who are too new to judge, tier C territories where a person should decide, and a rep with no segment.
- An answer key and a separate verifier that recomputes every rule from the CSVs and confirms the key.
- Two prompts. **A** is one vague sentence. **B** gives the rules, the date, and an output format.
- Each prompt run three times in fresh chats, with only the two data files attached.

## Results

| | Vague prompt (3 runs) | Structured prompt (3 runs) |
|---|---|---|
| Flag rows caught (of 16) | 10 to 12 clear, plus partials | 16 every time |
| Decoys flagged (of 9) | 4 to 6 | 0 |
| Tier C reps routed to a human | 0 of 3 runs | 3 of 3 runs |
| Reps ahead of pace recognized | Inconsistent, one never | Every time |
| Invented numbers | None | None |

The vague prompt found the real patterns every time and wrote a supportive, readable brief. What it did not do reliably was follow the edges: it coached reps who sit exactly on a threshold, ignored the territory exception, rarely recognized the reps who were ahead, and made up its own cutoffs, which differed from run to run. It also used its own clock for "today", one day off from the data, which moved the exact-at-threshold reps over the line.

Full outputs are in `results/`. The scored table and findings are in `results/summary.md`.

## Limits, stated plainly

- Synthetic data. The patterns were designed to be findable. This tests whether a method finds planted problems and avoids planted decoys, not whether it would work on a real team.
- Three runs per prompt shows consistency, not statistical proof.
- A data error was found along the way. Early on, nine reps had call and meeting counts that contradicted their blank dates, which made some cases ambiguous. It was fixed, the key was re-verified, and the four early runs were discarded. See `results/README.md`.
- The structured prompt still slipped once, in prose: one headline said two reps were ahead of pace while the table listed three. The rules protected the findings, not every sentence.
- A reviewer without the rules recommended adding a false flag (`results/extra_review_pass.txt`). Any check step needs the same rules as the step it checks.
- Outputs were copied from the chat window into text files. Tables were reformatted. Wording is unchanged.
- Coaching is a human job. This workflow prepares the brief and does not decide anything about a person.

## What this means in practice

If an AI is going to point managers at people, give it the rules, the date, and the exceptions, make it show the numbers behind every flag, and send unclear cases to a human. Put the exact rules in code where you can, and use the model for judgment and the write-up.

## Run it yourself

1. Open a fresh chat. Attach only `new_reps.csv` and `benchmark_summary.csv`.
2. Paste Prompt A or Prompt B from `prompts.md`.
3. Compare the output to `scoring.md` and `keys/`. Do not attach those files, or `source/`, to a test chat.
4. To confirm the key is correct: `python3 scripts/verify_ramp.py` from the repo root.

`scripts/generate_ramp_data.py` rebuilds the data. Run it in an empty folder, then move the CSVs into place.

## Files

- `new_reps.csv` and `benchmark_summary.csv`: the two files to attach
- `prompts.md`: Prompt A and Prompt B
- `scoring.md`: scoring table and what each decoy tests (do not attach)
- `keys/`: the answer key (do not attach)
- `source/`: the synthetic past reps the benchmark was built from (do not attach)
- `scripts/`: generator and verifier
- `results/`: all runs, the scored summary, and one reviewer check
