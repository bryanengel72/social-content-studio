# State Schema: Social Content Studio

Two files. A CSV that tracks the plan and a Markdown doc that holds the actual
captions to copy from. Same split the other skills use: the CSV is the source of
truth for scheduling and status; the Markdown is the human-facing working
document, generated and disposable.

```
social/
├── content-calendar.csv   ← one row per planned post, the tracker
└── content-plan.md        ← the full captions, grouped by week, copy-paste ready
```

No database, no connectors, and — importantly — **no auto-posting**. This skill
never publishes. It produces drafts the photographer reviews and posts themselves,
in their own hands, on their own accounts.

## content-calendar.csv

`build_calendar.py` lays down the dated slots; everything after that is filled in
as posts get written and go out.

| Column | Filled by | What it holds |
|---|---|---|
| `date` | Script | `YYYY-MM-DD`. When to post. A starting point the photographer can shift. |
| `platform` | Script | instagram, tiktok, linkedin, facebook, pinterest… |
| `content_type` | Script | hero, educational, behind-the-scenes, social-proof, personal, cta. The job of the post. |
| `status` | You | `Idea` → `Drafted` → `Scheduled` → `Posted`. Where the post is. |
| `hook` | You | The first line / the scroll-stopper. A quick label for the row; the full caption lives in content-plan.md. |
| `hashtag_set` | You | Which named set this post used (corporate, local, educational…), so you rotate them deliberately. |
| `visual_note` | You | What image or clip goes with it — "hero frame from Meridian shoot", "setup BTS clip". |
| `source_shoot` | You | Which real shoot this came from, so the month stays traceable and you don't run dry. |
| `performance` | You | After posting: what happened. "strong saves", "best reach this month", "flopped". The feedback loop. |

The status flow is the honest bit: a post is not `Posted` until it actually went
out. `calendar_status.py` reads these to tell you what's coming, what's still an
Idea, and — once `performance` has entries — what your audience rewards.

## content-plan.md

The captions themselves, grouped by week, each with its hook, full body, hashtag
set, and visual note, formatted to copy straight into the app. This is generated
from the calendar and the photographer's voice; regenerate it freely. Keeping the
long captions here rather than jammed into a CSV cell is what makes them actually
editable.

## Reading state back in a fresh session

The calendar spans weeks across separate sessions. On a machine with a writable
disk the two files persist on their own. In a plain chat they do not, so download
`content-calendar.csv` (and `content-plan.md` if mid-draft) at the end of a
session and upload them at the start of the next. Never reconstruct a calendar
from memory — a half-remembered plan is how a feed goes silent for a fortnight.

## The brand config lives in SKILL.md, not here

The photographer's voice notes, niche, location, booking link, and platform
cadence live in the `metadata` blocks of SKILL.md, because they describe the
business, not any one month's plan. The calendar is per-month and rolling; the
brand is constant. See [brand-voice.md](brand-voice.md).
