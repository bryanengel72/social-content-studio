---
name: social-content-studio
description: >
  Reusable client template for a photography business. Turns one shoot, or a month's plan,
  into social content in the photographer's own voice: builds a posting calendar at a
  realistic cadence, rotates content types so the month isn't thirty identical "look at my
  photo" posts, drafts platform-native captions with scroll-stopping hooks and local-first
  hashtags, and tracks what performed. Learns the photographer's real voice from sample
  captions so nothing reads like AI filler. State in a content-calendar.csv plus a copy-paste
  content-plan.md, no connectors. Never auto-posts — it drafts, the photographer publishes.
  Trigger on "write my social posts", "turn this shoot into content", "content calendar",
  "Instagram captions", "a month of content", "reels ideas", "TikTok hooks", "I never post
  consistently", or "batch my social media". Always use this skill for the full
  plan-write-track workflow — the cadence and content mix have to run in code, or you post
  five hero shots and go dark.
compatibility: >
  No connectors required. Python 3 (standard library only, no pip install) for the two bundled
  scripts. State lives in a plain content-calendar.csv and a content-plan.md the photographer
  owns. This skill never publishes to any platform — there is no posting connector and there is
  not meant to be; it produces drafts the photographer reviews and posts themselves. Optional:
  the photographer can paste engagement numbers back into the calendar to close the feedback
  loop.
metadata:
  brand:
    status: not yet configured
    photographer: "{{PHOTOGRAPHER}}"
    business_name: "{{BUSINESS_NAME}}"
    niche: "{{e.g. corporate headshots | weddings | families | personal branding}}"
    location: "{{city / metro — drives the local-first hashtags}}"
    booking_url: "{{where a CTA sends people}}"
    emoji_policy: "{{none | sparing | as in the samples}}"
    voice_status: not yet calibrated
    note: >
      voice is the whole game — see references/brand-voice.md. Do not guess it. At setup, collect
      3–5 of the photographer's real captions, derive the concrete voice rules, and record them in
      LEARNINGS.md §0. location is the highest-value marketing field here: local hashtags are
      where a photographer's clients actually find them.
  platforms:
    status: not yet configured
    cadence: "{{e.g. instagram:3,linkedin:1 — platform:posts-per-week}}"
    note: >
      Fewer platforms done well beats many done thinly. Pick the rooms where the actual buyer is
      (LinkedIn for corporate headshots, Pinterest and Instagram for weddings and families,
      Facebook for local referral markets) and set only the cadence the photographer will keep.
      See references/platforms.md. This string is passed straight to build_calendar.py.
  posting:
    status: configured
    publish_channel: draft-only
    note: >
      draft-only is not negotiable and there is no auto-post path. Every post is drafted and handed
      to the photographer to publish in their own hands. And before any post is built around an
      identifiable client, confirm the photographer has permission to feature them — a paid shoot
      is not a marketing release. See references/brand-voice.md.
  storage:
    status: configured
    backend: csv
    calendar_file: "content-calendar.csv"
    note: >
      One content-calendar.csv per rolling plan (the tracker) plus a generated content-plan.md
      (the copy-paste captions). Schema in references/state-schema.md. The CSV is the source of
      truth for scheduling and status.
---

# Social Content Studio Skill

Turns shoots into a steady, on-brand social presence. It plans the month at a cadence the
photographer will actually keep, rotates the kind of post so the feed has variety and purpose,
writes captions that sound like the photographer instead of like a robot, and tracks what worked
so the next month is sharper than the last.

Photographers are inconsistent posters, and when they do post it's often a lone hero shot with a
limp caption. Both are the same problem — no system — and both cost bookings quietly, because a
starved or samey feed gives a prospect no reason to trust, learn from, or hire them. This is the
system.

**This is a template.** Clone the folder per photographer, rename it, and fill in the `brand` and
`platforms` blocks under `metadata` before first use. The single most important setup step is
calibrating the voice — a block still marked `not yet configured` or `not yet calibrated` means
the content will sound generic, which is the one failure that makes the whole thing worthless.

> **Read [references/brand-voice.md](references/brand-voice.md) first, every time.** Voice is the
> difference between content that books and content that reads as AI filler. It cannot be skipped.
>
> **Read [LEARNINGS.md](LEARNINGS.md) first, every time, too.** It holds the photographer's
> calibrated voice and what has actually performed. Generate against both.
>
> **Read [references/state-schema.md](references/state-schema.md)** before touching the calendar.
>
> **Precedence when things disagree:** the calibrated voice in LEARNINGS.md and what has performed
> win over any generic best practice. The frontmatter config wins on everything else about the
> business. state-schema.md wins on file structure. Flag conflicts rather than guessing.

---

## Setup (once per photographer)

1. Fill in the `brand` block. **Calibrate the voice**: collect 3–5 of the photographer's real
   captions, derive the concrete rules (sentence rhythm, pronoun, formality, emoji rate, signature
   phrases, what they never do), and write them into LEARNINGS.md §0. See
   [references/brand-voice.md](references/brand-voice.md). Nothing else matters as much.
2. Set the `platforms` cadence to the rooms where the buyer is and the pace the photographer will
   keep. See [references/platforms.md](references/platforms.md).
3. Confirm where the photographer works. On a machine with a writable disk the calendar persists.
   In a plain chat it does not, and they must download `content-calendar.csv` at the end of a
   session and upload it at the start of the next. Say this once, plainly.

---

## Workflow A: Build the calendar

Trigger phrases: "plan my posts", "content calendar", "a month of content", "set up my posting".

1. Run the skeleton builder with the configured cadence:
   ```
   python3 scripts/build_calendar.py --start 2026-09-07 --weeks 4 \
     --platforms "instagram:3,linkedin:1" --out content-calendar.csv
   ```
   It lays down dated slots, spreads them across each week, and rotates the content type so the
   month has variety before a word is written.
2. **Read the mix summary.** If it warns there are no CTA posts, add `cta` to the rotation — soft
   content that never asks for the booking doesn't pay. See
   [references/content-types.md](references/content-types.md).
3. The dates are a starting point. Shift any slot the photographer wants; the point is the shape
   and cadence, not rigid days.

---

## Workflow B: Write the posts

Trigger phrases: "write my captions", "turn this shoot into content", "captions for this session".

1. **Read the voice from LEARNINGS.md and [references/brand-voice.md](references/brand-voice.md)
   before writing a single caption.** Generate in the photographer's voice, not the model's.
2. For each slot, write to its `content_type`'s job (hero, educational, social-proof, cta…). One
   good shoot can feed several types — the hero frame, the setup, the client's reaction, the
   lesson. Note the `source_shoot`.
3. Write **platform-native**, not once-and-paste — see [references/platforms.md](references/platforms.md).
   A LinkedIn post and an Instagram caption are different shapes of the same voice.
4. Lead every post with a real **hook**, and offer the photographer two or three to choose from.
   Attach a tiered, **local-first hashtag** set. See
   [references/hooks-and-hashtags.md](references/hooks-and-hashtags.md).
5. Write the full captions into `content-plan.md`, grouped by week, copy-paste ready. Put the hook
   and the hashtag-set name in the calendar row and move `status` to `Drafted`.
6. **Say only true things.** Never invent a testimonial, a statistic, or false scarcity. Use
   `[CONFIRM: ...]` for anything not known — including client permission to feature them.

---

## Workflow C: Track and learn

Trigger phrases: "what should I post next", "how's my content doing", "what's working".

1. Run the status report for what's coming and what's unwritten:
   ```
   python3 scripts/calendar_status.py --calendar content-calendar.csv --days 7 --mix
   ```
   It shows the next posts, flags anything past-due and unposted, and — with `--mix` — warns if one
   content type or platform is taking over.
2. As posts go out, set `status` to `Posted`. After a while, drop what happened into the
   `performance` column — "strong saves", "best reach this month", "flopped".
3. Once performance data exists, read it for the pattern: the types, hooks, and platforms the
   audience rewards. Record the pattern in LEARNINGS.md §1 and weight next month toward it. That
   feedback loop is the only thing that makes the content compound.

---

## No-Fabrication Rule

Never invent a client quote, a testimonial, a statistic, a result, or a sense of urgency that
isn't literally true. Never state that a post was published when it was only drafted. Never
present the model's generic voice as the photographer's — if the voice isn't calibrated, say so
rather than guessing it. Never tag a location the photographer doesn't serve. Never build a post
around an identifiable client without confirming permission. Use `[CONFIRM: ...]` for anything not
known to be true.

---

## Error Handling

| Error | Response |
|---|---|
| `brand` block `not yet configured` / voice `not yet calibrated` | Stop and calibrate the voice first. Generic content is the one failure that makes this worthless. |
| No real caption samples to calibrate from | Ask for 3–5. If truly none exist, draft in a plainly-stated provisional voice and flag every batch as needing the photographer's ear until samples arrive. |
| content-calendar.csv missing at session start | Expected in a plain chat between sessions. Ask for the upload. Never reconstruct the plan from memory. |
| build_calendar.py refuses (file exists) | It won't clobber planned posts. Use `--force` only if the photographer means to replace, or a new `--out`. |
| Mix summary warns no CTA posts | Add `cta` to `--types`. An audience you never ask doesn't book. |
| One content type is >50% of the plan | `calendar_status.py --mix` flags it. Rebalance — a samey feed is the default failure. |
| Photographer wants it posted automatically | There is no auto-post and there won't be. Draft it, hand it over, they publish. |
| Asked to write a testimonial or a result | Never fabricate one. Get a real quote (with consent) or leave it out. |
| Post features an identifiable client | Confirm permission before drafting. A paid shoot is not a marketing release. |
| Asked to invent local hashtags for cities they don't serve | Refuse. Only tag places the photographer actually works. |
| Content sounds generic / like AI | Re-read brand-voice.md, pull a concrete true detail into the post, show the photographer two options, and tighten the voice model from their pick. |

---

## Full Workflow Checklist

- [ ] `brand` and `platforms` blocks filled in
- [ ] Voice calibrated from 3–5 real captions and recorded in LEARNINGS.md §0
- [ ] Calendar built with the script, cadence and mix checked, CTA present
- [ ] Captions written in the photographer's voice, not the model's
- [ ] Platform-native drafts — not one caption pasted everywhere
- [ ] A real hook on every post, two or three options offered
- [ ] Tiered, local-first hashtag sets attached and rotated
- [ ] Nothing fabricated: no fake quotes, stats, or urgency; `[CONFIRM: ...]` on unknowns
- [ ] Client permission confirmed before featuring anyone identifiable
- [ ] Full captions in content-plan.md; calendar rows moved to Drafted
- [ ] status set to Posted as posts go out; performance logged after
- [ ] What performed read for the pattern and recorded in LEARNINGS.md §1

---

## Reference Files

| File | When to Read |
|---|---|
| [references/brand-voice.md](references/brand-voice.md) | Read first, every time. Capturing and applying the photographer's real voice, and the anti-AI-slop rules. |
| [LEARNINGS.md](LEARNINGS.md) | Read first, every time (apply the voice and what performs) and after posting (record it). Starts empty. |
| [references/content-types.md](references/content-types.md) | Read at Workflow A/B. The six content types, the job each does, and why the mix matters. |
| [references/platforms.md](references/platforms.md) | Read at Workflow B before writing. Per-platform shape — same voice, different room. |
| [references/hooks-and-hashtags.md](references/hooks-and-hashtags.md) | Read at Workflow B. Writing hooks that stop the scroll and a tiered, local-first hashtag strategy. |
| [references/state-schema.md](references/state-schema.md) | Read before touching the calendar. The two files, the status flow, reading state back in a fresh session. |

## Bundled Scripts

Standard library only. No pip install, no virtualenv.

| Script | Purpose |
|---|---|
| `scripts/build_calendar.py` | Lays down the posting-calendar skeleton: the right number of posts per platform, spread across each week, cycling through content types so variety is enforced before any caption is written. Warns if the mix has no CTA. Refuses to clobber an existing calendar without `--force`. |
| `scripts/calendar_status.py` | Reads content-calendar.csv and reports what's coming up, what's still unwritten, anything past-due and unposted, and — with `--mix` — whether one platform or content type is dominating. Once the `performance` column is filled, surfaces what the audience rewards. |
