# adr — a Claude Code skill for decision records

`/adr <decision and its context>` interviews you one question at a time, drafts
one Architecture Decision Record, writes it to `docs/decisions/NNNN-slug.md`,
adds the index row to `docs/DECISIONS.md`, and runs a consistency check.

Only the user invokes it (`disable-model-invocation: true`).

Format and conventions follow "Decisions that outlive the session" (CodeMiner, 2026).

## Install

```bash
git clone git@github.namli:namli/adr-skill.git ~/adr-skill
ln -s ~/adr-skill ~/.claude/skills/adr
```

## Layout

- `SKILL.md` — the skill.
- `assets/DECISIONS.md` — day-one index copied into a project on first use.
- `assets/record-template.md` — record template.
- `assets/claude-md-section.md` — section to paste into the project's `CLAUDE.md` by hand.
- `scripts/adr_check.py` — citation / index / instruction-size check. Stays in the skill, never in the project.
