# Decision records

Short records of decisions whose reasons the code does not show. One file per
decision, under `decisions/`, named `NNNN-a-few-words.md`, numbered in the order
the decisions were taken and never renumbered. This file is the index: a
citation of the form `ADR-NNNN`, anywhere in the tree, resolves through the
list below.

## Conventions

- **The status line** is `**Status:** accepted · **Date:** YYYY-MM-DD`, with
  `_amends ADR-NNNN_` appended when the record changes an earlier one.
- **An index row** is
  `- **[ADR-NNNN](decisions/NNNN-a-few-words.md)** — The record's title`,
  under the heading of its area, with `<br>_amended by ADR-NNNN_` appended once
  a later record amends it.
- **Amending, not rewriting.** An older record stays as it was decided. What
  changed is a new record that says so, and the older record's row gets the
  _amended by_ note.
- **`adr-check: ignore`** on a line that mentions an ADR number without citing
  one, such as a plan proposing the number the next record would take.

## Template

```markdown
# ADR-NNNN — A sentence that says what was decided

**Status:** accepted · **Date:** YYYY-MM-DD · _amends ADR-NNNN_

### Context

What was true before, and what forced a choice. This is a historical record:
when it names something that has since moved, correct it in place rather than
rewriting what happened.

### Decision

What was decided, who decided it, and the constraint behind each part of it.

### Consequences

What follows, including the failure modes a reader could not derive from the
code, which are most of what a record is worth.

### Revisit when

Optional. The condition under which this should be reopened.

### Alternatives considered

Every option that was weighed, why it lost, and who decided. Nothing else in
the tree records this, and it is what a future reader most often comes for.
```

## The records

One `###` heading per area of the system, with that area's rows under it.
