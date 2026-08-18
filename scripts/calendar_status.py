#!/usr/bin/env python3
"""
Report the state of the content calendar: what's coming up, what still needs
writing, whether the mix is healthy, and what actually performed.

A calendar only helps if it's looked at. This answers the three questions a
photographer actually has: what do I post next, what have I not written yet, and
is my month secretly all one kind of post again. With a performance column
filled in, it also starts telling them what their audience rewards, which is the
only feedback loop that makes the next month better than this one.

Standard library only. No pip install.

Usage:
    python3 calendar_status.py --calendar content-calendar.csv
    python3 calendar_status.py --calendar content-calendar.csv --today 2026-09-05 --days 7
    python3 calendar_status.py --calendar content-calendar.csv --mix
"""

import argparse
import csv
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DONE = {"posted"}


def load(path):
    p = Path(path)
    if not p.exists():
        sys.exit(f"Calendar not found: {p}. Run build_calendar.py first.")
    with p.open(newline="", encoding="utf-8-sig") as f:
        rows = [{(k or "").strip().lower(): (v or "").strip()
                 for k, v in r.items() if k is not None}
                for r in csv.DictReader(f)]
    rows = [r for r in rows if any(r.values())]
    if not rows:
        sys.exit(f"Calendar is empty: {p}")
    return rows


def tally(rows, field):
    out = {}
    for r in rows:
        key = r.get(field) or "(blank)"
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def parse_day(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description="Report the content calendar's state.")
    ap.add_argument("--calendar", required=True)
    ap.add_argument("--today", help="Override today's date, YYYY-MM-DD")
    ap.add_argument("--days", type=int, default=7, help="Look-ahead window (default 7)")
    ap.add_argument("--mix", action="store_true",
                    help="Show platform/content-type balance and flag over-reliance")
    args = ap.parse_args()

    rows = load(args.calendar)
    today = parse_day(args.today) if args.today else date.today()
    if args.today and today is None:
        sys.exit("--today must be YYYY-MM-DD")

    total = len(rows)
    print(f"Calendar: {total} posts\n")

    print("Status")
    for k, v in tally(rows, "status").items():
        print(f"  {k}: {v}")

    unwritten = [r for r in rows if (r.get("status") or "").lower() in ("idea", "")]
    print(f"\n{len(unwritten)} of {total} still need writing "
          f"(Idea), {sum(1 for r in rows if (r.get('status') or '').lower() in DONE)} posted.")

    # --- upcoming window ---
    dated = [(parse_day(r.get("date", "")), r) for r in rows]
    window_end = today + timedelta(days=args.days)
    upcoming = sorted(((d, r) for d, r in dated if d and today <= d <= window_end),
                      key=lambda t: t[0])
    print(f"\nNext {args.days} days (from {today}):")
    if upcoming:
        for d, r in upcoming:
            flag = "" if (r.get("status") or "").lower() not in ("idea", "") \
                   else "  ← still an Idea, write it"
            print(f"  {d}  {r.get('platform','?'):<10} {r.get('content_type','?'):<18}"
                  f"{flag}")
    else:
        print("  Nothing scheduled. The calendar may have run out — build the next block.")

    # posts already past but never marked Posted: quietly slipping
    missed = sorted(((d, r) for d, r in dated
                     if d and d < today and (r.get("status") or "").lower() != "posted"),
                    key=lambda t: t[0])
    if missed:
        print(f"\nPAST DUE — dated before today, not marked Posted ({len(missed)}):")
        for d, r in missed[:10]:
            print(f"  {d}  {r.get('platform','?')} / {r.get('content_type','?')} "
                  f"[{r.get('status') or 'Idea'}]")
        if len(missed) > 10:
            print(f"  ... and {len(missed) - 10} more")

    if args.mix:
        print("\n--- Mix ---")
        print("Platform:")
        for k, v in tally(rows, "platform").items():
            print(f"  {k}: {v} ({round(100*v/total)}%)")
        tmix = tally(rows, "content_type")
        print("Content type:")
        for k, v in tmix.items():
            print(f"  {k}: {v} ({round(100*v/total)}%)")
        top_type, top_n = next(iter(tmix.items()))
        if top_n / total > 0.5:
            print(f"\n! {top_type} is {round(100*top_n/total)}% of the plan. One kind of "
                  f"post dominating is how a feed gets boring — spread the mix.")
        if not any(t == "cta" for t in tmix):
            print("\n! No CTA posts. You're building an audience but never asking for the "
                  "booking.")

    # --- performance, if the column has anything in it ---
    perf = [r for r in rows if r.get("performance")]
    if perf:
        print(f"\n--- Performance ({len(perf)} posts with data) ---")
        by_type = {}
        for r in perf:
            by_type.setdefault(r.get("content_type", "?"), []).append(r["performance"])
        print("What you logged, grouped by content type:")
        for t, notes in sorted(by_type.items()):
            print(f"  {t}: " + "; ".join(notes[:3]) + (" ..." if len(notes) > 3 else ""))
        print("Read this for the pattern — the types your audience rewards get more of "
              "next month. Record the pattern in LEARNINGS.md.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
