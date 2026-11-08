import csv, math, random, statistics
from datetime import date, timedelta

random.seed(11)
AS_OF = date(2026, 11, 7)
MS = ["days_to_first_call", "days_to_first_meeting", "days_to_first_opp", "days_to_first_close"]

# ---------------- Past reps: the benchmark ----------------
past = []
def gen_past(seg, n, start_idx):
    for i in range(n):
        if seg == "SMB":
            c = random.randint(2, 8); m = c + random.randint(3, 12)
            o = m + random.randint(4, 14); cl = o + random.randint(10, 35)
            rate = random.uniform(0.15, 0.25)
        else:
            c = random.randint(3, 10); m = c + random.randint(5, 16)
            o = m + random.randint(8, 24); cl = o + random.randint(25, 70)
            rate = random.uniform(0.22, 0.38)
        calls = random.randint(300, 700)
        meetings = round(calls * rate)
        past.append(dict(rep_id=f"PAST-{start_idx + i:03d}", segment=seg,
                         days_to_first_call=c, days_to_first_meeting=m,
                         days_to_first_opp=o, days_to_first_close=cl,
                         calls_first_60d=calls, meetings_first_60d=meetings))
gen_past("SMB", 120, 1)
gen_past("Commercial", 80, 121)

def pct(vals, p):
    s = sorted(vals)
    return s[max(0, math.ceil(p * len(s)) - 1)]

B, RATE = {}, {}
summary = []
for seg in ("SMB", "Commercial"):
    rs = [r for r in past if r["segment"] == seg]
    B[seg] = []
    for k in MS:
        vals = [r[k] for r in rs]
        t = (pct(vals, 0.25), pct(vals, 0.5), pct(vals, 0.75))
        B[seg].append(t)
        summary.append([seg, k, *t])
    ratios = [r["meetings_first_60d"] / r["calls_first_60d"] for r in rs]
    RATE[seg] = round(round(statistics.median(ratios), 2) * 100)  # hundredths, integer
    summary.append([seg, "meeting_rate_meetings_per_call", "", RATE[seg] / 100, ""])

# ---------------- New reps ----------------
first = ["Alex", "Bianca", "Carlos", "Dani", "Elena", "Farid", "Gia", "Hector", "Imani", "Jonah",
         "Keiko", "Luca", "Maya", "Nico", "Opal", "Pedro", "Quinn", "Rosa", "Sam", "Tessa",
         "Uri", "Vera", "Wes", "Xenia", "Yusuf", "Zara"]
last = ["Alvarez", "Bennett", "Chowdhury", "Dalton", "Everett", "Fischer", "Gallagher", "Hayes",
        "Iverson", "Jacobs", "Kimura", "Lindqvist", "Morales", "Nakamura", "Okafor", "Pereira",
        "Quigley", "Rasmussen", "Santos", "Tran", "Underwood", "Vasquez", "Whitaker", "Yamada"]
name_pool = [f"{a} {b}" for a in first for b in last]
random.shuffle(name_pool)
managers = ["Dana Whitfield", "Omar Castillo", "Helen Brooks", "Victor Lang"]

def onpace(seg):
    b, out, prev = B[seg], [], 0
    for k in range(4):
        lo = max(b[k][0] + 1, prev + 1); hi = b[k][2]
        d = random.randint(lo, hi) if lo <= hi else max(hi, prev)
        out.append(d); prev = d
    return out

def trim(dl, days):
    return [d if d is not None and d <= days else None for d in dl]

def default_calls(seg, days):
    return days * (random.randint(6, 12) if seg == "SMB" else random.randint(4, 9))

def default_meetings(seg, calls):
    return round(calls * RATE[seg] / 100 * random.uniform(0.85, 1.3))

reps, key = [], []
def mk(seg, days, ms, calls=None, meetings=None, tier=None, seg_blank=False):
    seg_for_data = seg
    calls = default_calls(seg_for_data, days) if calls is None else calls
    meetings = default_meetings(seg_for_data, calls) if meetings is None else meetings
    r = dict(rep_name=name_pool.pop(), segment="" if seg_blank else seg,
             manager=random.choice(managers),
             territory_tier=tier or random.choice(["A", "B"]),
             start_date=AS_OF - timedelta(days=days),
             calls_to_date=calls, meetings_to_date=meetings, _seg=seg, _days=days)
    for k, v in zip(MS, ms):
        r[k] = v
    reps.append(r)
    return r

def add(r, rule, action, note):
    key.append((r, rule, action, note))

def unmet(r):
    seg, days = r["_seg"], r["_days"]
    return [MS[k].replace("days_to_first_", "first ") for k in range(4)
            if r[MS[k]] is None and days > B[seg][k][2]]

# Baseline, on pace, no issues
for _ in range(18):
    seg = random.choice(["SMB", "SMB", "Commercial"])
    days = random.randint(20, 110)
    tier = random.choices(["A", "B", "C"], weights=[40, 40, 20])[0]
    mk(seg, days, trim(onpace(seg), days), tier=tier)

p75 = lambda seg, k: B[seg][k][2]
p25 = lambda seg, k: B[seg][k][0]

# BEHIND_PACE (flag)
r = mk("SMB", p75("SMB", 1) + 6, [onpace("SMB")[0], None, None, None])
add(r, "BEHIND_PACE", "FLAG", "Behind on: " + ", ".join(unmet(r)))
r = mk("SMB", p75("SMB", 2) + 5, onpace("SMB")[:2] + [None, None])
add(r, "BEHIND_PACE", "FLAG", "Behind on: " + ", ".join(unmet(r)))
r = mk("Commercial", p75("Commercial", 3) + 8, onpace("Commercial")[:3] + [None])
add(r, "BEHIND_PACE", "FLAG", "Behind on: " + ", ".join(unmet(r)))
r = mk("Commercial", 40, [None, None, None, None])
add(r, "BEHIND_PACE", "FLAG", "Behind on: " + ", ".join(unmet(r)))
r = mk("Commercial", p75("Commercial", 1) + 4, [onpace("Commercial")[0], None, None, None])
add(r, "BEHIND_PACE", "FLAG", "Behind on: " + ", ".join(unmet(r)))
r = mk("SMB", 14, [None, None, None, None])
add(r, "BEHIND_PACE", "FLAG", "Exactly 14 days in seat, boundary case that is assessed. Behind on: " + ", ".join(unmet(r)))

# Boundary decoys: days in seat equals p75 exactly
r = mk("SMB", p75("SMB", 1), [onpace("SMB")[0], None, None, None])
add(r, "BEHIND_PACE", "DO_NOT_FLAG", "Days in seat equals the p75 for first meeting exactly, rule needs more than p75")
r = mk("Commercial", p75("Commercial", 2), onpace("Commercial")[:2] + [None, None])
add(r, "BEHIND_PACE", "DO_NOT_FLAG", "Days in seat equals the p75 for first opp exactly, rule needs more than p75")

# Too early to assess
r = mk("SMB", 10, [None, None, None, None])
add(r, "BEHIND_PACE", "DO_NOT_FLAG", "Only 10 days in seat, under the 14 day minimum, too early to assess")
r = mk("Commercial", 13, [None, None, None, None])
add(r, "BEHIND_PACE", "DO_NOT_FLAG", "Only 13 days in seat, under the 14 day minimum, too early to assess")

# Slow start but caught up
for seg in ("SMB", "Commercial"):
    days = p75(seg, 3) + 10
    dl = onpace(seg)
    dl[0] = p75(seg, 0) + (4 if seg == "SMB" else 5)
    for k in range(1, 4):
        dl[k] = max(dl[k], dl[k - 1] + 1)
        if dl[k] > days:
            dl[k] = days
    r = mk(seg, days, dl)
    add(r, "BEHIND_PACE", "DO_NOT_FLAG", "Reached first call late but every milestone is now achieved, nothing outstanding past p75")

# LOW_CONVERSION (flag)
for seg, days, calls in (("SMB", 60, 220), ("Commercial", 70, 160), ("SMB", 55, 260)):
    meetings = int(calls * RATE[seg] / 100 * 0.35)
    r = mk(seg, days, trim(onpace(seg), days), calls=calls, meetings=meetings)
    add(r, "LOW_CONVERSION", "FLAG", f"{meetings} meetings on {calls} calls, well under half of the benchmark rate")
r = mk("SMB", 60, trim(onpace("SMB"), 60), calls=200, meetings=RATE["SMB"])
add(r, "LOW_CONVERSION", "DO_NOT_FLAG", "Meeting rate is exactly half the benchmark, rule needs less than half")
r = mk("Commercial", 80, trim(onpace("Commercial"), 80), calls=90, meetings=3)
add(r, "LOW_CONVERSION", "DO_NOT_FLAG", "Only 90 calls, under the 100 call minimum for this rule")

# Multi-issue: behind pace and low conversion
days = max(p75("SMB", 2) + 8, 50)
r = mk("SMB", days, onpace("SMB")[:2] + [None, None], calls=180, meetings=int(180 * RATE["SMB"] / 100 * 0.3))
add(r, "BEHIND_PACE", "FLAG", "Multi-issue rep. Behind on: " + ", ".join(unmet(r)))
add(r, "LOW_CONVERSION", "FLAG", "Multi-issue rep. Low meeting rate on 180 calls")

# Territory tier C: behind pace goes to human look
r = mk("SMB", p75("SMB", 1) + 5, [onpace("SMB")[0], None, None, None], tier="C")
add(r, "BEHIND_PACE", "NEEDS_HUMAN_LOOK", "Meets the behind-pace rule but territory tier is C, route to a human. Behind on: " + ", ".join(unmet(r)))
r = mk("Commercial", p75("Commercial", 1) + 6, [onpace("Commercial")[0], None, None, None], tier="C")
add(r, "BEHIND_PACE", "NEEDS_HUMAN_LOOK", "Meets the behind-pace rule but territory tier is C, route to a human. Behind on: " + ", ".join(unmet(r)))

# AHEAD_OF_PACE
def ahead_ms(close_day):
    o = close_day - random.randint(6, 12)
    m = o - random.randint(3, 8)
    c = max(1, m - random.randint(3, 6))
    return [c, m, o, close_day]
for seg, k in (("SMB", 0), ("SMB", 4), ("Commercial", 5)):
    cd = p25(seg, 3) - k
    r = mk(seg, cd + 15, ahead_ms(cd))
    note = "First close exactly at p25, boundary case that counts as ahead" if k == 0 else "First close earlier than p25"
    add(r, "AHEAD_OF_PACE", "FLAG", note)
cd = p25("SMB", 3) + 1
r = mk("SMB", cd + 15, ahead_ms(cd))
add(r, "AHEAD_OF_PACE", "DO_NOT_FLAG", "First close is one day slower than p25, not ahead")

# DATA_ORDER
dl = onpace("SMB"); dl[1] = dl[0] - 2
r = mk("SMB", 60, trim(dl, 60))
add(r, "DATA_ORDER", "FLAG", "First meeting day is earlier than first call day")
dl = onpace("Commercial"); dl[2] = dl[3] + 5
r = mk("Commercial", 140, trim(dl, 140))
add(r, "DATA_ORDER", "FLAG", "First opp day is later than first close day")

# Missing segment
r = mk("SMB", 40, trim(onpace("SMB"), 40), seg_blank=True)
add(r, "BENCHMARK_SEGMENT", "NEEDS_HUMAN_LOOK", "Segment is blank, cannot choose a benchmark")

# ---------------- Consistency pass ----------------
# Activity counts must agree with milestone dates: no first call date means no
# calls or meetings were logged, and no first meeting date means no meetings.
for r in reps:
    if r[MS[0]] is None:
        r["calls_to_date"], r["meetings_to_date"] = 0, 0
    elif r[MS[1]] is None:
        r["meetings_to_date"] = 0

# ---------------- Write ----------------
random.shuffle(reps)
for i, r in enumerate(reps):
    r["rep_id"] = f"REP-{3001 + i}"
reps.sort(key=lambda r: r["rep_id"])

fmt = lambda v: "" if v is None else v
fields = ["rep_id", "rep_name", "segment", "manager", "territory_tier", "start_date"] + MS + ["calls_to_date", "meetings_to_date"]
with open("new_reps.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(fields)
    for r in reps:
        w.writerow([fmt(r[c]) if c != "start_date" else r[c].isoformat() for c in fields])

with open("past_reps_benchmark.csv", "w", newline="") as f:
    w = csv.writer(f)
    cols = ["rep_id", "segment"] + MS + ["calls_first_60d", "meetings_first_60d"]
    w.writerow(cols)
    for r in past:
        w.writerow([r[c] for c in cols])

with open("benchmark_summary.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["segment", "metric", "p25", "median", "p75"])
    w.writerows(summary)

with open("answer_key.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["rep_id", "rule", "expected_action", "note"])
    for r, rule, action, note in sorted(key, key=lambda x: (x[0]["rep_id"], x[1])):
        w.writerow([r["rep_id"], rule, action, note])

from collections import Counter
print(len(reps), "new reps;", Counter(k[2] for k in key))
print("Benchmark:", {s: B[s] for s in B}, RATE)
