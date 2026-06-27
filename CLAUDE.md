# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## Repository status

**This repository is currently empty** — it was freshly initialized and
contains no application code, build configuration, or history yet. There is no
codebase to document at this time.

This file establishes the conventions to follow and should be **kept up to date
as the project takes shape**. When real code is added, replace the placeholder
sections below with concrete details (architecture, build/test commands,
directory layout, key modules, and domain conventions).

- **Name:** `research` (`free2007free/research`)
- **Default working directory:** `/home/user/research`

## Git workflow

- **Develop on the feature branch** `claude/claude-md-docs-slucre`. Create it
  locally if it does not exist. Do not push to any other branch without
  explicit permission.
- **Commit** with clear, descriptive messages.
- **Push** with `git push -u origin <branch-name>`. On network failure, retry up
  to 4 times with exponential backoff (2s, 4s, 8s, 16s).
- **Do not open a pull request** unless explicitly asked.
- When fetching/pulling, prefer specifying the branch: `git fetch origin <branch>`.

## Conventions to honor

- Keep this file current. Whenever the structure, workflow, or conventions
  change, update CLAUDE.md in the same change.
- Use the repository's scratchpad/temp directory for throwaway files rather than
  committing them.
- Don't introduce a tool, framework, or dependency without confirming it fits
  the (future) project's stack — there is no established stack to match yet.

## To fill in as the codebase grows

Replace this section with real content once code lands:

- **Project overview** — what the project does and who it's for.
- **Architecture** — major components and how they fit together.
- **Directory layout** — what lives where.
- **Build / run / test** — the exact commands to build, run, and test.
- **Code style & conventions** — linting, formatting, naming, patterns.
- **Testing** — how tests are organized and run; expectations for new code.
- **Gotchas** — non-obvious constraints worth knowing before making changes.
