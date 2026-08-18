# Social Content Studio

A Claude Skill that turns your shoots into a steady, on-brand social presence. It
plans the month at a cadence you'll actually keep, rotates the *kind* of post so
your feed isn't thirty identical "look at my photo" shots, writes captions that
sound like **you** instead of like a robot, and tracks what worked so next month
is sharper than the last.

Part of the [Photographer Skills](https://github.com/bryanengel72) family, but it
stands alone — it doesn't need the others.

Photographers are inconsistent posters, and when they do post it's often a lone
hero shot with a limp caption. Both are the same problem — no system — and both
cost bookings quietly, because a starved or samey feed gives a prospect no reason
to trust you, learn from you, or hire you. This is the system.

**No database. No connectors. No pip install. And no auto-posting** — it drafts,
you publish, in your own hands on your own accounts.

## What makes it not sound like AI

The whole thing lives or dies on voice. At setup you give it three to five of your
real captions, and it learns your actual rhythm, your emoji habit (or lack of one),
your tics — and generates against that. No "✨ magic happens ✨", no hollow
superlatives, no engagement-bait. If it can't sound like you, it says so rather
than faking it.

## Install

You do not need to know how to code, and you do not need to open a terminal.

### Step 1 — Download the skill

**[Download social-content-studio.zip](https://github.com/bryanengel72/social-content-studio/releases/latest/download/social-content-studio.zip)** — one file, about 34 KB.

**Leave it zipped for now.** Do not double-click it yet. Which path you take
next decides whether you unzip it at all.

> Ignore the blue **`<> Code`** button at the top of this page. That gives you a
> folder with `-main` stuck on the end of the name, which Claude will not find.
> Use the download link above instead.

### Step 2 — Add it to Claude

Two ways. **Path A is easier.** Pick one, not both.

---

#### Path A — Upload it (Claude web or desktop app)

Nothing gets installed on your computer. Four clicks:

1. In Claude, open **Customize → Skills**.
2. Click **Add**.
3. Choose **Upload a skill**.
4. Pick the `social-content-studio.zip` you just downloaded — still zipped.

It appears in your skills list with a switch beside it. Make sure the switch is
on.

**One setting to check first.** Skills need code execution turned on. Open
**Settings → Capabilities** and switch on **Code execution and file creation**.
Available on Free, Pro, Max, Team and Enterprise plans.

---

#### Path B — Drop the folder in (Claude Code)

If you run Claude Code on your own machine, it reads skills from a folder
instead.

Double-click the ZIP to unzip it. You get a folder called
**`social-content-studio`** — correctly named already, nothing to rename.

**On a Mac**

1. Open **Finder**.
2. In the menu bar, click **Go**, then **Go to Folder...**
   (or press `Shift` + `Command` + `G`).
3. Type this exactly and press Return:

   ```
   ~/.claude/skills
   ```

4. Drag your `social-content-studio` folder into the window that opens.

If it says the folder does not exist, go to `~/.claude` instead, create a new
folder inside it named `skills` (all lowercase), and drag the folder into that.

**On Windows**

1. Open **File Explorer**.
2. Click the address bar at the top, type this exactly, and press Enter:

   ```
   %USERPROFILE%\.claude\skills
   ```

3. Drag your `social-content-studio` folder into the window that opens.

If that folder does not exist, go to `%USERPROFILE%\.claude`, create a folder
named `skills`, and drag `social-content-studio` into that.

You should end up with `SKILL.md` sitting directly inside the folder:

```
.claude/skills/social-content-studio/SKILL.md
```

Then quit Claude and open it again — it only looks for new skills at startup.

### Already comfortable with a terminal?

```bash
git clone https://github.com/bryanengel72/social-content-studio.git
cp -r social-content-studio ~/.claude/skills/
```

### What you need on your computer

Python 3.8 or newer, and nothing else — no libraries to install, no accounts to
create. Python is already on every Mac. On Windows, if Claude tells you Python is
missing, get it from [python.org/downloads](https://www.python.org/downloads/)
and tick **"Add Python to PATH"** on the first screen of the installer.

## Try it in thirty seconds

Talk to Claude:

> Using the Social Content Studio examples, build me a two-week content calendar
> for Instagram and LinkedIn and show me what a week of posts looks like.

The examples folder has a sample calendar, a filled-in week of posts, and a set of
voice samples so you can see how the captions come out sounding like a real person
rather than a brand account.

From a terminal:

```bash
cd examples
python3 ../scripts/build_calendar.py --start 2026-09-07 --weeks 2 \
  --platforms "instagram:3,linkedin:1" --out /tmp/calendar.csv
```

## Setup

Ask Claude:

> Open the Social Content Studio SKILL.md and set it up for my studio — I'll paste
> a few of my real captions so it can learn my voice.

The one step that matters most is **voice calibration**: give it three to five
captions you've actually written, and it derives your real tone and writes in it.
Then set your **niche**, your **location** (this drives the local hashtags that
actually get you found), your **booking link**, and which **platforms** you post
on and how often.

## How state works

Two files:

```
social/
├── content-calendar.csv   ← the plan and tracker, one row per post
└── content-plan.md        ← the full captions, copy-paste ready
```

The calendar carries the date, platform, content type, status, and — after
posting — how each post performed, which is the feedback loop that makes the next
month better. Open it in Excel, Numbers, or Sheets any time.

If you run Claude on a machine with a writable disk, these persist on their own.
In a plain chat they do not, so download them at the end of a session and upload
them at the start of the next.

## Two things the skill won't do

**It won't post for you.** There's no auto-publish and there isn't meant to be —
it hands you drafts to review and post yourself. Your accounts, your final say.

**It won't make things up.** No invented testimonials, no fake statistics, no
"only 2 spots left!" unless it's true, and no building a post around a client's
face without confirming you have permission to use them in your marketing.

## Scripts

| Script | What it does |
|---|---|
| `scripts/build_calendar.py` | Lays down the posting-calendar skeleton — the right number of posts per platform, spread across each week, cycling content types so variety is baked in before you write a word. Warns if you've got no booking prompts in the mix. |
| `scripts/calendar_status.py` | Shows what's coming up, what you still haven't written, anything past-due, and whether one kind of post is quietly taking over your feed. Once you log how posts performed, it surfaces what your audience rewards. |

Both take `--help`.

## A note on your data

`content-calendar.csv`, `content-plan.md`, and a used `LEARNINGS.md` are your
voice and your business. The bundled `.gitignore` excludes them for exactly that
reason. If you fork this for your own use, keep those rules.

## License

MIT. See [LICENSE](LICENSE).
