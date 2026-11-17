# Minimal scene fixture

This directory contains two tiny text fixtures, not real PLY/NumPy data. Their
real SHA-256 values let tests and onboarding exercise both schema and file
integrity validation without committing scene artifacts.

```bash
./scripts/uv.sh run sgd3dgs validate --check-files examples/minimal-scene/scene.json
```

Real scene packages belong under the ignored `data/scenes/` hierarchy or on
shared storage. Research inputs and method runs belong in `sgd3dgs-research`.
