#!/usr/bin/env python3
"""
Build the skeleton of a posting calendar: the right number of posts, spread
across the week, cycling through content types so the month has variety.

Left to themselves, photographers post five hero shots in a row and then go dark
for three weeks. Both failures are the same failure — no system — and both are
deterministic to fix. This lays down the dated slots at a realistic cadence and
rotates the content type on each one so no single kind of post takes over. It
does NOT write captions; that is the skill's job, in the photographer's own
voice. This just guarantees the shape of the month is sound before a word is
written.

Standard library only. No pip install.

Usage:
    python3 build_calendar.py --start 2026-09-01 --weeks 4 \
        --platforms "instagram:3,tiktok:2,linkedin:1" --out content-calendar.csv

    # override the content-type rotation
    python3 build_calendar.py --start 2026-09-01 --weeks 4 \
        --platforms "instagram:3" \
        --types "hero,educational,behind-the-scenes,social-proof,personal,cta"
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

# The default mix. Order matters: it interleaves reach posts (hero, educational)
# with trust posts (behind-the-scenes, social-proof, personal) and a recurring
# ask (cta), so a booking prompt lands roughly every sixth post instead of never.
DEFAULT_TYPES = ["hero", "educational", "behind-the-scenes",
                 "social-proof", "personal", "cta"]

COLUMNS = ["date", "platform", "content_type", "status", "hook",
           "hashtag_set", "visual_note", "source_shoot", "performance"]

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def spread_days(k):
    """k posts across a 7-day week, spread out rather than bunched.

    A single weekly post lands midweek; more than one fans across the week so a
    platform never posts twice in a day while sitting silent for five."""
    if k <= 0:
        return []
    if k == 1:
        return [2]  # Wednesday — a lone post does best midweek
    if k >= 7:
        return list(range(7))
    return sorted({round(i * 7 / k) % 7 for i in range(k)})


def parse_platforms(spec):
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            sys.exit(f"--platforms wants name:count pairs, got '{part}' "
                     f"(e.g. \"instagram:3,tiktok:2\")")
        name, _, count = part.partition(":")
        name = name.strip().lower()
        try:
            n = int(count)
        except ValueError:
            sys.exit(f"--platforms: '{count}' after '{name}:' is not a number")
        if n < 0:
            sys.exit(f"--platforms: negative count for {name}")
        if n > 0:
            out.append((name, n))
    if not out:
        sys.exit("No platforms with a positive post count. Nothing to schedule.")
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Build a posting-calendar skeleton with cadence and content variety.")
    ap.add_argument("--start", required=True, help="First Monday of the plan, YYYY-MM-DD")
    ap.add_argument("--weeks", type=int, default=4)
    ap.add_argument("--platforms", required=True,
                    help='Per-week counts, e.g. "instagram:3,tiktok:2,linkedin:1"')
    ap.add_argument("--types", default=",".join(DEFAULT_TYPES),
                    help="Content-type rotation, comma-separated. See references/content-types.md")
    ap.add_argument("--out", default="content-calendar.csv")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite an existing calendar instead of refusing")
    args = ap.parse_args()

    try:
        start = datetime.strptime(args.start, "%Y-%m-%d").date()
    except ValueError:
        sys.exit("--start must be YYYY-MM-DD")
    if args.weeks < 1:
        sys.exit("--weeks must be at least 1")

    # Anchor to the Monday of the start week so the day-spread lines up.
    monday = start - timedelta(days=start.weekday())
    if monday != start:
        print(f"Note: {args.start} is a {WEEKDAYS[start.weekday()]}; anchoring the "
              f"plan to that week's Monday, {monday}.")

    platforms = parse_platforms(args.platforms)
    types = [t.strip() for t in args.types.split(",") if t.strip()]
    if not types:
        sys.exit("No content types given.")

    out_path = Path(args.out)
    if out_path.exists() and not args.force:
        sys.exit(f"{out_path} already exists. Re-run with --force to replace it, or "
                 f"point --out somewhere else so you don't lose planned posts.")

    # Lay down every (date, platform) slot.
    slots = []
    for w in range(args.weeks):
        week_start = monday + timedelta(days=7 * w)
        for name, n in platforms:
            for d in spread_days(n):
                slots.append((week_start + timedelta(days=d), name))

    # Chronological order, then rotate the content type across the whole run so
    # variety is enforced across the feed, not just within one platform.
    slots.sort(key=lambda s: (s[0], s[1]))
    rows = []
    for i, (day, name) in enumerate(slots):
        rows.append({
            "date": day.isoformat(),
            "platform": name,
            "content_type": types[i % len(types)],
            "status": "Idea",
            "hook": "", "hashtag_set": "", "visual_note": "",
            "source_shoot": "", "performance": "",
        })

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    # Summary so the shape is visible before any caption is written.
    per_platform = {}
    per_type = {}
    for r in rows:
        per_platform[r["platform"]] = per_platform.get(r["platform"], 0) + 1
        per_type[r["content_type"]] = per_type.get(r["content_type"], 0) + 1

    print(f"Wrote {out_path} — {len(rows)} posts over {args.weeks} week(s), "
          f"{monday} to {monday + timedelta(days=7*args.weeks-1)}.\n")
    print("By platform:")
    for k, v in sorted(per_platform.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}")
    print("\nBy content type:")
    for k, v in sorted(per_type.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}")
    ctas = per_type.get("cta", 0)
    if ctas == 0:
        print("\n! No CTA posts in the rotation. Soft content builds an audience but "
              "never asks for the booking — add 'cta' to --types.")
    else:
        print(f"\n{ctas} booking prompt(s) across the plan — roughly one every "
              f"{round(len(rows)/ctas)} posts.")
    print("\nEvery row is an Idea. Fill the hook, caption (in content-plan.md) and "
          "hashtag_set in the photographer's own voice, then move status to Drafted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
