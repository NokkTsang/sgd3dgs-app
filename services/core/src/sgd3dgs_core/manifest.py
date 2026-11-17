"""Manifest loading and file-integrity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sgd3dgs_core.models import ArtifactRef, SceneManifest


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> SceneManifest:
    with path.open(encoding="utf-8") as stream:
        payload = json.load(stream)
    return SceneManifest.model_validate(payload)


def iter_artifacts(manifest: SceneManifest) -> list[ArtifactRef]:
    artifacts: list[ArtifactRef] = [manifest.source]
    if manifest.cameras:
        artifacts.append(manifest.cameras)
    if manifest.labels:
        artifacts.append(manifest.labels)
    return artifacts


def verify_artifacts(manifest_path: Path, manifest: SceneManifest) -> list[str]:
    errors: list[str] = []
    root = manifest_path.parent
    for artifact in iter_artifacts(manifest):
        artifact_path = root / artifact.path
        if not artifact_path.is_file():
            errors.append(f"missing artifact: {artifact.path}")
            continue
        actual = sha256_file(artifact_path)
        if actual != artifact.sha256:
            errors.append(
                f"checksum mismatch for {artifact.path}: expected {artifact.sha256}, got {actual}"
            )
    return errors
