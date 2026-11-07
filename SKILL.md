---
name: adr
description: Use when the user invokes /adr to record one architecture decision as an ADR in the project's docs/decisions/.
disable-model-invocation: true
argument-hint: "[the decision and its context, in free text]"
allowed-tools: Bash(python3 -I ${CLAUDE_SKILL_DIR}/scripts/adr_check.py *)
---

# Recording a decision

One decision, one record, in the form `docs/DECISIONS.md` defines. The user
decides. You interview, draft, write, check. The user's text: `$ARGUMENTS`.

## 1. Set up once

If `docs/DECISIONS.md` does not exist: `mkdir -p docs/decisions`, copy
`${CLAUDE_SKILL_DIR}/assets/DECISIONS.md` to `docs/DECISIONS.md`, and tell the
user in one line that `${CLAUDE_SKILL_DIR}/assets/claude-md-section.md` holds
the section they can paste into `CLAUDE.md` themselves. Never edit `CLAUDE.md`.

If `CLAUDE.md` or a page under `docs/` already names another place for
decisions (search them for "decision"), say so in one line: two homes drift.
From now on the reasons live in the record, and that place cites `ADR-NNNN`.

## 2. Read before asking

Read `docs/DECISIONS.md`. Read every record in the area the decision touches,
and grep the tree for their numbers. If the new decision changes what an earlier
record decided, the new record amends it. What the repository already says is
filled in, not asked.

## 3. Interview: one question per message

The record has these slots. Fill them from `$ARGUMENTS` and the repository
first. Ask only for slots still empty.

| Slot | What fills it |
|---|---|
| Context | What was true before, and what forced a choice now |
| Decision | What was decided, and the constraint behind each part |
| Decided by | Written as "the project owner" when the user decided; a role when the text names someone else. Never "the user" or "the owner" alone: domain words |
| Date | When the decision was taken. The text says "we agreed", "since", or names a past event: ask for the date. Otherwise today |
| Consequences | What follows, including failure modes the code will not show |
| Alternatives | Every option weighed: why it lost, who rejected it |
| Revisit when | Optional. Ask once; "none" is an answer |
| Area | An existing `###` heading in the index. None fits: the name of the matching page in the project's docs (such as `docs/domains/*.md`), then a new name |

The interview:

- One question per message, in the user's language. Wait for the answer.
- A question names the slot it fills and offers 2–4 concrete options grounded
  in the repository and the domain, with the one you would pick marked. The
  user can always answer in their own words.
- For alternatives, first ask what else was on the table. Then propose the
  likely options from the domain for the user to confirm or strike.
- Settled without asking: number is the next free one, file name comes from
  the title, status is `accepted`, language is the language of the project's
  documentation (English when there is none).
- Out of scope: code changes, tests, tickets, commits, the `CLAUDE.md`
  section. The record names what the code must do; the change is another task.
- When the user says "enough", stop. An empty slot reads `Not recorded.`

## 4. Draft, then wait

Show the full record, the index row, and any `_amended by_` change to an
existing row. Ask whether to write it or what to change. Write nothing before
the user says yes.

## 5. Write and check

Write `docs/decisions/NNNN-slug.md`. Add the row under its area heading. Add
`<br>_amended by ADR-NNNN_` to each amended row. Then run:

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/adr_check.py" .
```

Fix what it reports in the index or the file, never in the script. Reply with
one line, `ADR-NNNN — docs/decisions/NNNN-slug.md`, ready to paste into a
brainstorm. Under it, list the files found in step 2 that implement the
decision, one per line, as places to cite it from: a comment that says what
the code does and ends with `(ADR-NNNN)`. Do not edit them.

## The record

The title is the decision as a sentence: "Sessions expire after 7 days
without use", not "Session expiry". Status line:
`**Status:** accepted · **Date:** YYYY-MM-DD`, with `· _amends ADR-NNNN_`
appended when it amends one. Sections, in order: Context, Decision,
Consequences, Revisit when (only when there is one), Alternatives considered.
Each alternative: the option in bold, why it lost, who rejected it. Template:
`${CLAUDE_SKILL_DIR}/assets/record-template.md`.

## Common mistakes

| Mistake | Instead |
|---|---|
| Several questions in one message | One slot, one question, wait |
| Asking for number, file name, language, status | Settle them by the rules above |
| Dated today when the text says it was decided earlier | Ask for the date; the number stays the next free one |
| "Decided by the owner" or "by the user" | "the project owner", or the role the text names |
| Asking whether to change code or open a ticket | Out of scope; the record only |
| Inventing conventions when `docs/` is empty | Set up from the assets first |
| Writing the file before the draft is approved | Draft, wait, then write |
| Reasons repeated in a code comment | The comment cites `ADR-NNNN`; reasons stay in the record |
