# Scene and label format

## 1. Design goals

The format must make method comparison safe without creating a new 3D asset
container. Standard 3DGS PLY or SOG remains the Gaussian data; SGD3DGS adds a
small manifest and aligned label arrays.

`sgd3dgs-app` owns this contract. `sgd3dgs-research` produces packages against a
specific released schema version and validates them with the app CLI.

The contract optimizes for:

- stable Gaussian identity;
- explicit coordinate systems;
- independent research outputs;
- provenance and checksums;
- efficient browser conversion;
- forward-compatible schema versions.

## 2. Manifest

Version `0.1` is described by `schemas/scene-manifest-0.1.schema.json` and the
Pydantic model in `services/core`.

Important fields:

- `source.path`: relative path from `scene.json` to the source PLY/SOG;
- `source.sha256`: binds labels and edits to exact source bytes;
- `source.gaussian_count`: required length of every per-Gaussian array;
- `coordinate_system`: up axis, handedness, and optional metric scale;
- `labels`: one active label artifact and its producing method;
- `objects`: human-readable metadata and initial transforms.

All paths are relative to the manifest directory unless explicitly documented.

## 3. Labels

The initial interchange format is an uncompressed NumPy array:

```text
object_id.npy
dtype: uint16
shape: [N]
```

Reserved values:

| Value | Meaning |
|---:|---|
| `0` | static background or stuff |
| `1..65533` | movable object instance |
| `65534` | ambiguous boundary |
| `65535` | unknown, invalid, or noise |

An optional `confidence.npy` uses `float32[N]` in `[0, 1]`. Confidence describes
membership evidence, not semantic-class confidence, unless a method-specific
experiment explicitly says otherwise.

PLY `object_id` properties may be generated for interchange with tools that
preserve extra columns. The sidecar array remains canonical until round-trip
preservation is tested across all supported formats.

## 4. Gaussian identity

Array position is the Gaussian ID in schema 0.1. Therefore:

```text
source checksum + Gaussian count + array index = identity
```

Any spatial sorting, filtering, compression, or export may change array order.
Converters must either preserve order or emit an explicit old-to-new index map.
Never infer correspondence from position alone: multiple Gaussians may share
very similar means, and numeric export changes can make matching unstable.

## 5. Object transforms

Transforms are stored as translation, XYZW quaternion, and uniform scale. The
source scene remains unchanged. The editor applies object transforms through
its instance/transform palette and records commands for undo and persistence.

The initial release supports translation and rotation. Uniform scale exists in
the schema for future compatibility but is not part of the first MVP.

## 6. Generated content

Completion artifacts must record:

- generating method and commit/version;
- input source and label checksums;
- prompt/conditioning inputs;
- random seed;
- which Gaussians are observed versus generated;
- alignment transform;
- human approval state.

Generated content must never silently overwrite observed source Gaussians.

## 7. Schema changes

Breaking changes create a new schema file and migration command. Do not edit a
released schema to reinterpret existing data. Before version 1.0, migrations may
be simple, but they must be deterministic and tested. Open the contract/ADR in
the app repository first, then update the linked research adapters.
