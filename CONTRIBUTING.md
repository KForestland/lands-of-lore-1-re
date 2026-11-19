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
- `examples/` holds three small example images; `tools/example_images.py --check` must pass after any change to the tools that make them.
- `tools/` holds the readers and extractors; each needs `--data` and has `--check`.
- `data/` holds structured inventories and parsed outputs.

## Checks without game files

Run `python3 -m unittest` and `python3 tools/repo_guard.py --check`
from the repository root. The tests build their own fixtures in memory or
in a temporary directory. GitHub Actions runs these same commands on
pushes and pull requests. CI uses the runner's Python (3.12); the minimum version in the README is not tested there.

## Release procedure (maintainers)

Every commit that reaches a public branch must carry the project's noreply identity as author and committer:

```bash
git -c user.name=KForestland -c user.email=261564562+KForestland@users.noreply.github.com commit ...
```

Before a release branch is pushed:

1. Contributor work is squash-merged and committed with the identity above.
2. In a fresh clone of the release branch, with `$LOL1_DATA` set to your game files, `python3 tools/check_all.py` must end with `ALL ... CHECKS PASSED` and `python3 -m unittest` must pass. It includes `tools/repo_guard.py`, which fails on game files and media, on files over 300 KB, and on machine paths and on the words in an optional local word list (`.git/info/private_words`, never tracked). Then run `python3 tools/repo_guard.py --check --release`: it also fails on any author or committer address in the branch history other than the allowed noreply ones (`ALLOWED_AUTHORS`; GitHub web merges may commit as `noreply@github.com`). Contributors do not need `--release`.
3. The tree must be clean after the checks, and the tools must write nothing into the repository.

## Pull Requests

Small, focused PRs are preferred:

- one doc cleanup pass
- one tool cleanup pass
- one examples/data pass
