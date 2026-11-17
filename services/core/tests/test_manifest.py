import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError
from sgd3dgs_core.manifest import load_manifest
from sgd3dgs_core.models import SceneManifest

REPOSITORY_ROOT = Path(__file__).parents[3]


def test_example_manifest_is_valid() -> None:
    manifest = load_manifest(REPOSITORY_ROOT / "examples/minimal-scene/scene.json")

    assert manifest.scene_id == "minimal-fixture"
    assert manifest.source.gaussian_count == 3
    assert manifest.objects[0].object_id == 1


def test_example_manifest_matches_published_json_schema() -> None:
    schema_path = REPOSITORY_ROOT / "schemas/scene-manifest-0.1.schema.json"
    example_path = REPOSITORY_ROOT / "examples/minimal-scene/scene.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(example)


def test_label_count_must_match_source() -> None:
    payload = {
        "schema_version": "0.1",
        "scene_id": "broken",
        "display_name": "Broken fixture",
        "coordinate_system": {"up_axis": "+Y"},
        "source": {
            "path": "scene.ply",
            "sha256": "0" * 64,
            "format": "3dgs-ply",
            "gaussian_count": 10,
        },
        "labels": {
            "path": "object_id.npy",
            "sha256": "1" * 64,
            "format": "npy-uint16",
            "gaussian_count": 9,
            "method": "fixture",
            "method_version": "1",
        },
    }

    with pytest.raises(ValidationError, match="Gaussian counts must match"):
        SceneManifest.model_validate(payload)


def test_duplicate_object_ids_are_rejected() -> None:
    source = {
        "path": "scene.ply",
        "sha256": "0" * 64,
        "format": "3dgs-ply",
        "gaussian_count": 3,
    }
    labels = {
        "path": "object_id.npy",
        "sha256": "1" * 64,
        "format": "npy-uint16",
        "gaussian_count": 3,
        "method": "fixture",
        "method_version": "1",
    }
    payload = {
        "schema_version": "0.1",
        "scene_id": "duplicate-ids",
        "display_name": "Duplicate IDs",
        "coordinate_system": {"up_axis": "+Y"},
        "source": source,
        "labels": labels,
        "objects": [
            {"object_id": 1, "name": "first"},
            {"object_id": 1, "name": "second"},
        ],
    }

    with pytest.raises(ValidationError, match="object_id values must be unique"):
        SceneManifest.model_validate(payload)


@pytest.mark.parametrize(
    "path",
    [
        "/absolute/scene.ply",
        "C:\\absolute\\scene.ply",
        "../outside.ply",
        "nested/../../outside.ply",
    ],
)
def test_artifact_paths_cannot_escape_manifest_directory(path: str) -> None:
    payload = {
        "schema_version": "0.1",
        "scene_id": "unsafe-path",
        "display_name": "Unsafe path",
        "coordinate_system": {"up_axis": "+Y"},
        "source": {
            "path": path,
            "sha256": "0" * 64,
            "format": "3dgs-ply",
            "gaussian_count": 3,
        },
    }

    with pytest.raises(ValidationError, match="artifact path must be relative"):
        SceneManifest.model_validate(payload)
