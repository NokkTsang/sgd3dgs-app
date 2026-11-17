# Third-party software in SGD3DGS App

This is an engineering inventory, not legal advice. Verify exact terms before
shipping a binary, hosted service, or combined source distribution.

## Bundled source

### PlayCanvas SuperSplat

- Location: `apps/editor/`
- Upstream: <https://github.com/playcanvas/supersplat>
- Pinned commit: `30b5a42c6a90f46e4b698356a7b597290fb9fea1`
- License: MIT
- Purpose: WebGPU Gaussian editor, selection, transforms, history, import/export
- Attribution: the original license is preserved at `apps/editor/LICENSE`

Local dependency-only security updates and whitespace normalization are listed
in `apps/editor/UPSTREAM.md`.

## Research dependencies are not bundled

Gaussian Grouping, SAGA, gsplat, SAM, inpainting, and generation frameworks are
owned and inventoried by `sgd3dgs-research`. They must not be copied into this
repository or its application container merely to simplify local setup.

The app may consume their output only through the documented scene contract.
That separation does not erase output/model license obligations; provenance
must accompany imported artifacts.
