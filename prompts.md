# Prompts

Use a fresh chat for every run. Attach only `new_reps.csv` and `benchmark_summary.csv`. Do not attach anything from `keys/` or `source/`, or `scoring.md`.

## Prompt A (vague)

```
Review these new reps against the benchmark and tell me who needs coaching.
```

## Prompt B (structured)

```
You are a sales enablement analyst preparing a weekly ramp coaching brief for sales managers.

Today's date is November 7, 2026. Two files are attached: new_reps.csv (one row per new rep) and benchmark_summary.csv (p25, median, and p75 days for each milestone by segment, plus the benchmark meeting rate per call). Use benchmark_summary.csv exactly as given. Do not recalculate benchmarks.

Days in seat is today minus start_date. A blank milestone means it has not been achieved yet. Milestones happen in this order: first call, first meeting, first opp, first close.

RULES

1. BEHIND_PACE: days in seat is 14 or more, a milestone is blank, and days in seat is more than the segment's p75 for that milestone. List every milestone that meets this. Exception: if territory_tier is C, do not flag the rep. Put them under "Needs a human look" instead, because territory may explain the gap.
2. LOW_CONVERSION: days in seat is 45 or more, calls_to_date is 100 or more, and meetings_to_date divided by calls_to_date is less than half of the segment's benchmark meeting rate.
3. AHEAD_OF_PACE: first close is achieved at or before the segment's p25 for first close. This is good news to recognize.
4. DATA_ORDER: an achieved milestone has a smaller day count than an earlier milestone (for example, first meeting before first call). This is a data quality problem.

OTHER RULES

- Reps with fewer than 14 days in seat are too early to assess. Never flag them as BEHIND_PACE.
- A rep who reached a milestone late but has no blank milestone past its p75 is not behind.
- If segment is blank, you cannot choose a benchmark. Put the rep under "Needs a human look."
- A rep can hit more than one rule. List each rule as its own row.
- Every flag must show the exact values behind it (for example, days in seat and the p75, or meetings and calls versus the benchmark rate).
- Never invent reps, fields, or numbers. Only give counts you actually counted.
- Only flag a rep if the data clearly meets the rule exactly as written. If something is borderline, ambiguous, or blank, put it under "Needs a human look" and say why.

OUTPUT FORMAT

1. Headline (2 sentences max): the most important thing for managers this week.
2. Top 3 actions: each names the manager, the rep, and a specific coaching action.
3. Flagged reps: a table with rep_id, rep_name, manager, segment, issue type, evidence.
4. Needs a human look: items with the reason, or "None."
5. Counts: flagged rows per issue type, and total reviewed reps.

Keep it to one page, in plain language. Use a supportive coaching tone. Describe patterns, not character, and do not label any rep as a poor performer.
```
