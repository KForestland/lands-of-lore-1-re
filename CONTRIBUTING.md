# Contributing

Thanks for contributing to the public *Lands of Lore I* reverse-engineering repo.

## Scope

Good contributions for this repo:

- clearer wording in the documentation
- tool fixes and new readers (no game data in the repository)
- evidence-backed corrections
- answers to the numbered open questions in `docs/OPEN_QUESTIONS.md`
- small data-table improvements that match the documentation

Out of scope:

- retail game files
- full extracted asset dumps
- speculative claims presented as settled truth
- private working notes

## Working Rules

- Prefer technically honest wording over maximal wording.
- Keep extraction facts, interpretation, and edition comparison clearly separated.
- Update the format page and `tools/README.md` with any change; mark claims CONFIRMED or UNCONFIRMED and cite the evidence.

## Repo Shape

- `docs/` holds the format pages, the rules and script pages, status and open questions.
- `examples/` holds three small example images.
- `tools/` holds the readers and extractors; each needs `--data` and has `--check`.
- `data/` holds structured inventories and parsed outputs.

## Pull Requests

Small, focused PRs are preferred:

- one doc cleanup pass
- one tool cleanup pass
- one examples/data pass
