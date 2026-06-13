# Setting up the monthly scheduled trigger

This repo is set up to produce a **monthly GCC/UAE banking sector ratings
report** from S&P, Fitch, and Moody's. The research itself is run by Claude; you
just need to wire up a **scheduled trigger** so it runs automatically in the
last week of every month.

## Why a scheduled trigger (and not "just keep this chat open")

Claude Code on the web runs each session in an **ephemeral container** that is
reclaimed after inactivity. A single chat session cannot reliably wake itself up
a month later. A **scheduled trigger** solves this: it launches a fresh session
on a schedule and runs a saved prompt. Docs:
https://code.claude.com/docs/en/claude-code-on-the-web

## One-time setup

1. Open **Claude Code on the web** and go to this repository
   (`lydiahfbao-debug/lydia-ball`).
2. Create a new **Scheduled trigger** (also called a scheduled session).
3. Configure it:
   - **Repository:** `lydiahfbao-debug/lydia-ball`
   - **Branch:** `claude/gcc-banking-rating-reports-ev3itl` (or merge this to
     `main` and point the trigger at `main`)
   - **Schedule:** monthly, timed for the **last week of the month**. If the UI
     only offers a cron expression, use one of:
     - `0 9 25 * *` — 09:00 UTC on the 25th of every month (always in the last
       week), **recommended** for simplicity.
     - `0 9 28 * *` — 09:00 UTC on the 28th of every month.
   - **Prompt:** paste the contents of
     [`prompts/monthly-gcc-uae-banking-ratings.md`](../prompts/monthly-gcc-uae-banking-ratings.md),
     **or** simply point the prompt at that file with:
     > Run the saved prompt in `prompts/monthly-gcc-uae-banking-ratings.md`.
   - **Network policy:** ensure outbound web access is enabled so the session
     can reach the agency sites and financial press. Without it, the report will
     only contain a "sources could not be reached" notice.
4. Save and enable the trigger.

## What each run does

- Researches the trailing ~30 days of rating activity for UAE banks (with GCC
  context) across S&P, Fitch, and Moody's.
- Writes the report to `reports/<YYYY>-<MM>.md` and commits it.
- Delivers the full report in the session chat.

## Where reports land

- In the **session chat** for that scheduled run (delivered "here" each month).
- Committed to **`reports/<YYYY>-<MM>.md`** in this repo, so you have a durable,
  growing archive.

## Adjusting scope

Edit `prompts/monthly-gcc-uae-banking-ratings.md` to change focus (e.g. add
issuers, widen to full GCC, or narrow to UAE only). The next scheduled run picks
up the change automatically.

## A note on paywalls

The agencies' full reports are subscription-only. These monthly runs capture
**publicly available** rating action commentaries, press releases, and sector
outlooks, always with sources. If you have paid S&P/Fitch/Moody's logins and
want the full reports incorporated, that requires a different (authenticated)
setup — open an issue or ask in a session and we can discuss options.
