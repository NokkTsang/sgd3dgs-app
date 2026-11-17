# SGD3DGS Core

The core package owns scene contracts, provenance, validation, stable geometry
utilities, and the future local application API. Browser rendering belongs to
`apps/editor`; training and method-specific adapters belong to
`sgd3dgs-research`.

Current commands:

```bash
./scripts/uv.sh run sgd3dgs validate examples/minimal-scene/scene.json
./scripts/uv.sh run sgd3dgs checksum path/to/scene.ply
./scripts/uv.sh run uvicorn sgd3dgs_core.api:app --reload --host 127.0.0.1 --port 8080
```

GPU frameworks are intentionally excluded. The app consumes validated artifacts
from the research repository rather than importing its environments.
