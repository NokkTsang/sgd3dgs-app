# ADR 0001: Separate application and research repositories

- Status: accepted
- Date: 2026-11-17
- Owners: project team

## Context

The browser application needs a stable Node/Python setup, fast CI, a canonical
scene contract, and reviewable product releases. Segmentation and completion
work needs incompatible PyTorch/CUDA stacks, large weights/data, rapidly changing
methods, and many experiments that will never become product features.

A single repository coupled unrelated dependency risk and made it unclear where
experimental outputs became supported. Several literal upstream forks would
preserve history but scatter the project contract, tracking, and owned code.

## Decision

Use two owned repositories under one local workspace:

- `sgd3dgs-app` owns the SuperSplat-based product, schema, validation, and the
  cross-project plan;
- `sgd3dgs-research` owns external methods, isolated environments, adapters,
  experiments, metrics, and completion research.

They integrate only through versioned scene packages. SuperSplat is retained as
a pinned, attributed source snapshot in app. Research baselines are exact,
ignored external checkouts rather than vendored forks.

## Consequences

- App setup and CI remain free of CUDA and model dependencies.
- Failed experiments do not destabilize product history.
- Schema ownership and promotion from experiment to product are explicit.
- Cross-repository work needs linked issues and coordinated versions.
- A contract change is merged in app before research adapters adopt it.
- Upstream refreshes require explicit pin/license review in the owning repo.

## Rejected alternatives

- **One monorepo:** simpler navigation, but poor dependency/release isolation.
- **One repository per upstream method:** too many trackers and no clear owned
  integration layer.
- **Git submodules:** preserve histories but add onboarding/update friction and
  still do not solve environment isolation.
