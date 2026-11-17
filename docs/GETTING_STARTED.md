# Getting started with SGD3DGS App

## 1. Sustainable commitment

A project week runs Wednesday through the Tuesday evening meeting. A normal
contribution is one focused day or two to three evenings, approximately 5–8
hours. Tasks are weekly outcomes, not daily assignments.

## 2. Local workspace

The recommended layout is:

```text
SGD3DGS/
├── sgd3dgs-app/
└── sgd3dgs-research/
```

This repository can build independently. The sibling is needed only when
producing or validating real research artifacts.

## 3. Concepts to understand

- A Gaussian stores position, anisotropic size/orientation, opacity, and
  view-dependent appearance.
- A pixel blends many depth-sorted Gaussians; it is not a mesh surface.
- Per-Gaussian labels are arrays whose order must match the source scene.
- Moving captured content exposes unseen background/object surfaces.
- The app consumes artifacts; it does not train segmentation models.

Use [GLOSSARY.md](GLOSSARY.md) while reading the code.

## 4. Prerequisites

- Git 2.40+
- Node.js 20.19+ and npm
- uv
- Chrome or Edge with WebGPU

```bash
./scripts/check_system.sh
```

Python 3.12 is pinned. Use repository commands rather than the system Python.

## 5. Editor setup

```bash
make editor-install
make editor-test
make editor-dev
```

Open `http://localhost:3000`. Before editing code, practice:

1. load a normal 3DGS PLY;
2. orbit and fly through the scene;
3. use depth-aware rectangle/brush/sphere selection;
4. translate and rotate a selected subset;
5. undo and redo;
6. save and reload a project.

## 6. Core setup

```bash
make core-sync
make core-check
make validate-sample
```

Useful commands:

```bash
./scripts/uv.sh run sgd3dgs --help
./scripts/uv.sh run sgd3dgs validate path/to/scene.json
./scripts/uv.sh run sgd3dgs validate --check-files path/to/scene.json
./scripts/uv.sh run sgd3dgs checksum path/to/scene.ply
```

Optional local API:

```bash
./scripts/uv.sh run uvicorn sgd3dgs_core.api:app --reload --host 127.0.0.1 --port 8080
```

The uv wrapper uses `venv/` rather than `.venv/`, avoiding a macOS hidden-file
flag problem seen in Desktop/Documents locations.

## 7. Importing research output

The sibling research repository writes complete derived scene packages to
shared storage. Never copy its Python environment or method modules into this
repository. Validate a package here:

```bash
./scripts/uv.sh run sgd3dgs validate --check-files /shared/scenes/example/scene.json
```

If it fails, fix the producer or create a reviewed schema change; do not weaken
validation locally.

## 8. First pull request

Good starter PRs include an onboarding correction, a manifest validation test,
a narrow editor integration point, or a reproducible browser issue. Before
review:

```bash
make verify
./scripts/verify_repository.sh
```

Editor behavior changes include a screenshot or short recording.

## 9. Common mistakes

- Adding labels to a reordered scene without an index map.
- Importing legacy research code into `services/core`.
- Committing a PLY, capture, label array, weight, token, or generated output.
- Building a job dashboard before a stable artifact workflow exists.
- Starting completion UI before selection and transform correctness work.
- Letting a side-project task grow beyond its weekly time box.
