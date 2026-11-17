# Contributing to SGD3DGS App

## Scope routing

Open work in the repository that owns the output:

| Work | Repository |
|---|---|
| Editor, picking, transforms, undo, persistence | `sgd3dgs-app` |
| Scene schema, validation, import/export contract | `sgd3dgs-app` |
| Segmentation methods and GPU environments | `sgd3dgs-research` |
| Completion/inpainting experiments and metrics | `sgd3dgs-research` |
| Research adapter output consumed by the editor | Lead issue in research; linked integration issue in app |

Do not solve a cross-repository dependency by copying source files. Agree on an
artifact/schema change and link the two issues.

## Rhythm and task size

Weeks run Wednesday–Tuesday. Tuesday evening is for demonstrations, integration
decisions, and assigning the next bounded outcome. Expected effort is 5–8 hours
per person, with no daily status requirement.

## Branches and pull requests

- Use short branches such as `feat/object-id-index` or `docs/onboarding`.
- Keep schema changes separate from editor feature work where practical.
- Never mix a SuperSplat refresh with local features.
- Prefer PRs reviewable in under 30 minutes.
- Link the issue and the research issue when applicable.
- Include exact verification commands and visual evidence for UI behavior.

## Required checks

```bash
make verify
./scripts/verify_repository.sh
```

Use Ruff formatting and strict mypy for Python. Follow the bundled SuperSplat
TypeScript configuration under `apps/editor`.

## Definition of done

A task is done when its agreed behavior exists, another person can inspect or
reproduce it, tests/docs are updated, provenance is preserved, no private or
large artifact is committed, and its reviewer approves it.

## Contract changes

Changes to schema versions, Gaussian ordering, coordinate systems, transforms,
or generated-content meaning require an ADR under `docs/decisions/`. Include a
migration/compatibility note and a linked research-repository adoption issue.

## Data and secrets

Never commit real scenes, captured images, model weights, label arrays, `.env`
files, tokens, or signed URLs. If a secret enters history, rotate it immediately.
