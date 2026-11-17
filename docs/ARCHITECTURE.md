# Application architecture

## 1. Boundary first

SGD3DGS has two repositories because interactive product code and experimental
GPU code evolve at different speeds and have very different dependencies.

```text
sgd3dgs-research                         sgd3dgs-app
─────────────────                        ───────────
images / cameras / source 3DGS
        │
segmentation / refinement / completion
        │
        └── versioned scene package ───▶ validate and import
                                             │
                                    browser-local interaction
                              click → object ID → selection → transform
```

Research can take minutes or hours on an isolated NVIDIA worker. Picking,
highlighting, dragging, rotation, undo, and save must remain local and
interactive. No model or network request belongs in the mouse-drag loop.

## 2. Repository ownership

### `sgd3dgs-app` — this repository

Owns the editor, canonical schema, validation, local API, product integration,
tests, and releases. A change to Gaussian identity, label meaning, coordinate
systems, or saved edits begins here.

### `sgd3dgs-research`

Owns method reproduction, training/inference environments, adapters,
experiments, metrics, and generated/derived artifacts. It consumes a released
app contract and never imports app internals by filesystem tricks.

The only supported bridge is a versioned artifact. Source code is not shared by
copying modules between repositories.

## 3. Application components

### `apps/editor`

A pinned PlayCanvas SuperSplat source snapshot providing:

- WebGPU Gaussian rendering and sorting;
- camera/input handling and GPU picking;
- per-Gaussian selection state;
- transform tools and command history;
- import/export and project persistence.

SGD3DGS additions should be narrow modules for object metadata, ID lookup,
selection, and derived-variant visualization.

### `services/core`

A small Python package providing:

- manifest and artifact validation;
- checksum and Gaussian-count integrity checks;
- canonical scene/object models;
- converter-independent geometry utilities as they become stable;
- a local API only for proven, asynchronous workflows.

It must run without CUDA. Research frameworks do not become core dependencies.

### `schemas`

The authoritative interchange contract. Breaking changes create a new version
and migration path. Research pins a schema version and reports the producing
method separately.

## 4. Canonical scene model

```text
Scene package
├── scene.json                     # schema version and provenance
├── immutable source Gaussians     # PLY or SOG, checksum-bound
├── optional cameras
├── labels
│   ├── object_id: uint16[N]
│   └── confidence: float32[N]     # optional
├── object metadata
└── optional derived variants      # observed/generated kept distinguishable
```

Reserved IDs:

- `0`: static background;
- `1..65533`: object instances;
- `65534`: ambiguous boundary;
- `65535`: unknown/noise.

Schema `0.1` uses array position as Gaussian identity. A label array is valid
only for the exact source checksum and Gaussian count. Reordering requires an
explicit index map.

## 5. Selection path

1. Pick visible Gaussian index/depth under a click.
2. Look up its `object_id`.
3. Reject background/unknown or resolve a small weighted neighborhood.
4. Use a prebuilt object-ID-to-index/range map.
5. Highlight the complete object.
6. Attach existing transform tools and command history.

The first version optimizes correctness and inspectability, not cleverness.

## 6. Transform correctness

For rotation `R` and translation `t`:

```text
mean:       μ' = Rμ + t
covariance: Σ' = RΣRᵀ
scale:      unchanged
opacity:    unchanged
```

Orientation and view-dependent spherical-harmonic appearance must follow the
object rotation. Edits remain non-destructive transforms until explicit export.

## 7. Repair and completion variants

Research may return background repair or object completion variants. The app
must keep these distinct from observations, show their provenance, and allow
users to disable/remove them. A visually plausible generated surface is not
relabelled as captured truth.

## 8. API evolution

The API starts with `/health`. Endpoints are added only after the equivalent CLI
and artifact workflow are reproducible:

1. validate/import a manifest;
2. inspect objects and provenance;
3. monitor an explicitly configured offline job;
4. retrieve a completed artifact reference.

Large assets stay in files/object storage, not JSON. The API is local and has no
authentication in the initial release, so it must not be internet-exposed.

## 9. Initial non-goals

- A new reconstruction or training framework.
- Diffusion in the interaction loop.
- Perfect relighting or real-time physical shadows.
- Multi-user simultaneous editing.
- Deformable animation.
- Hiding method or license ambiguity inside the app image.
