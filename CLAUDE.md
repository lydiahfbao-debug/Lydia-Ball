# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

As of the last update, this repository is a freshly initialized project. It
contains only `README.md` (the project title, "Lydia-Ball") and has no source
code, build configuration, dependencies, tests, or tooling yet.

There is therefore no architecture to describe and no build/lint/test commands
to run. Do not invent any — the sections below are intentionally empty until
real code exists.

## What to do as the project grows

When you add the first meaningful code to this repository, update this file in
the same change so it stays accurate. Specifically, fill in:

- **Commands** — once a build system or package manager is introduced (e.g.
  `package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`), document the
  exact commands to install dependencies, build, run, lint, and test, including
  how to run a single test.
- **Architecture** — once the codebase spans multiple files/modules, describe
  the big-picture structure and how the pieces fit together, focusing on what
  can't be learned by reading a single file.
- **Conventions** — capture any project-specific patterns, naming rules, or
  workflows that aren't obvious from the code itself.

Keep this file concise and specific to this repository; omit generic advice.
