# Editor upstream

This directory is a source snapshot of
[PlayCanvas SuperSplat](https://github.com/playcanvas/supersplat).

- Upstream commit: `30b5a42c6a90f46e4b698356a7b597290fb9fea1`
- Commit date: 2026-11-17
- Upstream license: MIT; see `LICENSE` in this directory
- Imported for SGD3DGS: 2026-11-17

Local dependency-only security updates applied after import:

- `eslint` 10.14.0 → 10.15.0
- `serve` 14.2.7 → 14.2.8
- transitive development dependencies refreshed with `npm audit fix`
- six pre-existing trailing-whitespace/blank-line warnings normalized

These versions resolve the advisories reported by `npm audit` for the imported
development toolchain. They do not change editor source code.

## Local modification policy

Keep changes small and identifiable. Prefer new SGD3DGS modules over unrelated
rewrites of upstream files. Every pull request touching this directory should
state whether it:

1. is project-specific and should remain local;
2. could be contributed upstream; or
3. resolves a conflict introduced by refreshing the snapshot.

Before updating upstream:

1. create a dedicated `chore/update-supersplat-<date>` branch;
2. record the old and new commit hashes;
3. compare upstream license and package changes;
4. apply the update without mixing feature work;
5. run `make editor-test` and `make editor-build`;
6. manually test import, selection, transform, undo, export, and reload;
7. update this file and `THIRD_PARTY.md`.

Do not replace this directory with a nested Git repository or submodule. Keeping
a normal source snapshot makes a fresh SGD3DGS clone self-contained while the
pin and update policy preserve provenance.
