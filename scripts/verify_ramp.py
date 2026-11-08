"""Recompute every ramp coach rule from the CSVs and compare to the answer key.

Usage (from the repo root): python3 scripts/verify_ramp.py
Needs new_reps.csv and benchmark_summary.csv in the root and keys/answer_key.csv.
A clean run means the answer key matches the rules exactly.
"""
import csv
from datetime import date

AS_OF = date(2026, 11, 7)
MS = ["days_to_first_call", "days_to_first_meeting", "days_to_first_opp", "days_to_first_close"]

reps = list(csv.DictReader(open("new_reps.csv")))
key = list(csv.DictReader(open("keys/answer_key.csv")))

bench, rate = {}, {}
for r in csv.DictReader(open("benchmark_summary.csv")):
    if r["metric"] == "meeting_rate_meetings_per_call":
        rate[r["segment"]] = round(float(r["median"]) * 100)  # hundredths
    else:
        bench[(r["segment"], r["metric"])] = (int(r["p25"]), int(r["median"]), int(r["p75"]))

flag, nhl = set(), set()
for r in reps:
    rid, seg = r["rep_id"], r["segment"]
    days = (AS_OF - date.fromisoformat(r["start_date"])).days
    vals = [int(r[m]) if r[m] != "" else None for m in MS]
    calls, meetings = int(r["calls_to_date"]), int(r["meetings_to_date"])

    # Data order: achieved milestones must not go backwards
    achieved = [v for v in vals if v is not None]
    if any(b < a for a, b in zip(achieved, achieved[1:])):
        flag.add((rid, "DATA_ORDER"))

    if seg == "":
        nhl.add((rid, "BENCHMARK_SEGMENT"))
        continue

    if days >= 14:
        behind = [m for m, v in zip(MS, vals) if v is None and days > bench[(seg, m)][2]]
        if behind:
            (nhl if r["territory_tier"] == "C" else flag).add((rid, "BEHIND_PACE"))

    if days >= 45 and calls >= 100 and meetings * 200 < calls * rate[seg]:
        flag.add((rid, "LOW_CONVERSION"))

    close = vals[3]
    if close is not None and close <= bench[(seg, MS[3])][0]:
        flag.add((rid, "AHEAD_OF_PACE"))

exp_flag = {(k["rep_id"], k["rule"]) for k in key if k["expected_action"] == "FLAG"}
exp_nhl = {(k["rep_id"], k["rule"]) for k in key if k["expected_action"] == "NEEDS_HUMAN_LOOK"}
decoys = {(k["rep_id"], k["rule"]) for k in key if k["expected_action"] == "DO_NOT_FLAG"}

print(f"Rules found {len(flag)} flags and {len(nhl)} human-look items; key expects {len(exp_flag)} and {len(exp_nhl)}.")
print("Flags in key but not found:", sorted(exp_flag - flag) or "none")
print("Flags found but not in key:", sorted(flag - exp_flag) or "none")
print("Human-look in key but not found:", sorted(exp_nhl - nhl) or "none")
print("Human-look found but not in key:", sorted(nhl - exp_nhl) or "none")
print("Decoys that trigger a rule:", sorted(decoys & (flag | nhl)) or "none")
