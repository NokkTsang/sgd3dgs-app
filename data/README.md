# Local application data

Only this file is committed. Scene packages under `data/scenes/`, temporary
cache, and editor outputs are ignored.

```text
data/
├── scenes/<scene-id>/       # Validated packages produced by research
├── cache/                   # Re-creatable local cache
└── outputs/                 # Local editor exports
```

The source scene remains immutable. A package imported here must pass:

```bash
./scripts/uv.sh run sgd3dgs validate --check-files data/scenes/<scene-id>/scene.json
```

Raw captures, training data, model weights, segmentation runs, and completion
experiments belong in `sgd3dgs-research` or approved shared storage—not here.
