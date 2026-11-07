## Decision records

A decision record explains one decision whose reasons the code does not show:
what was decided, why, and which alternatives were rejected, and by whom.
Records live in `docs/decisions/`, one file per decision, named
`NNNN-a-few-words.md`. `ADR-NNNN` anywhere in the repository cites the record
with that number. `docs/DECISIONS.md` holds the conventions, the template, and
the index: one row per record, grouped by area.

- **Read before you change.** Before changing code that cites a record, read the
  record and every record that amends it, directly or through another
  amendment; the _amended by_ notes in the index list them. Then search the
  repository for the record's number: every citation marks code or a test that
  relies on the decision. Before changing behaviour in an area, read that
  area's rows in the index. Do not propose an option a record rejected unless
  something has changed since, and then say what. If a record says the user
  made the decision or rejected the option, only the user can reverse it.
- **Cite, don't copy.** A decision's reasons live in its record and nowhere
  else. A comment at the code that implements the decision says what the code
  does and cites the record, as in `// Expire idle sessions (ADR-NNNN).` A test
  that enforces the decision cites the record too. Neither repeats the reasons.
- **Amend, don't rewrite.** Never change what an accepted record decided;
  correcting a stale path or name in it is fine. A change of mind is a new
  record. Records are written only by the user through `/adr`; do not create
  or edit records on your own.
- **Keep this file short.** It says how to work in this repository and where
  to look. A decision belongs in a record: this file may name the record, but
  does not restate it.
