# Lydia-Ball

Automated **monthly GCC banking sector ratings intelligence**, focused on the
**UAE**, compiled from **S&P Global Ratings**, **Fitch Ratings**, and **Moody's
Ratings**.

A scheduled trigger runs in the **last week of every month**, researches the
trailing ~30 days of rating actions and sector commentary, and delivers a report
both in-session and as a committed file under [`reports/`](./reports/).

## Contents

- [`prompts/monthly-gcc-uae-banking-ratings.md`](./prompts/monthly-gcc-uae-banking-ratings.md)
  — the self-contained prompt each scheduled run executes.
- [`docs/scheduled-trigger-setup.md`](./docs/scheduled-trigger-setup.md)
  — how to wire up the monthly scheduled trigger (one-time setup).
- [`reports/`](./reports/) — the growing archive of monthly reports, plus
  [`TEMPLATE.md`](./reports/TEMPLATE.md).

## Quick start

1. Follow [`docs/scheduled-trigger-setup.md`](./docs/scheduled-trigger-setup.md)
   to create the monthly trigger in Claude Code on the web.
2. Reports appear here each month, and in that run's chat.

## Scope & limitations

- **Focus:** UAE banking sector, with broader GCC (Saudi, Qatar, Kuwait,
  Bahrain, Oman) as secondary context.
- **Paywalls:** Full agency reports are subscription-only. These reports
  summarize publicly available rating action commentaries, press releases, and
  sector outlooks, always with sources cited.
