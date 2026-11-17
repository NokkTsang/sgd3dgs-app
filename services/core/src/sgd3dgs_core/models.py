"""Versioned scene-manifest models.

The manifest is intentionally small. Large Gaussian arrays, label arrays, source
images, and generated artifacts stay in external files referenced by checksum.
"""

from __future__ import annotations

from pathlib import PurePosixPath, PureWindowsPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Sha256 = str


def validate_artifact_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    if PurePosixPath(normalized).is_absolute() or PureWindowsPath(value).is_absolute():
        raise ValueError("artifact path must be relative and may not contain '..'")
    if any(part == ".." for part in normalized.split("/")):
        raise ValueError("artifact path must be relative and may not contain '..'")
    return normalized


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ArtifactRef(StrictModel):
    path: str = Field(min_length=1)
    sha256: Sha256

    @field_validator("path")
    @classmethod
    def path_is_relative_and_contained(cls, value: str) -> str:
        return validate_artifact_path(value)

    @field_validator("sha256")
    @classmethod
    def valid_sha256(cls, value: str) -> str:
        normalized = value.lower()
        if len(normalized) != 64 or any(char not in "0123456789abcdef" for char in normalized):
            raise ValueError("sha256 must contain exactly 64 hexadecimal characters")
        return normalized


class CoordinateSystem(StrictModel):
    up_axis: Literal["+X", "-X", "+Y", "-Y", "+Z", "-Z"]
    handedness: Literal["left", "right"] = "right"
    unit: Literal["unknown", "meter"] = "unknown"
    meters_per_unit: float | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def metric_scale_is_consistent(self) -> CoordinateSystem:
        if self.unit == "meter" and self.meters_per_unit is None:
            self.meters_per_unit = 1.0
        return self


class SourceScene(ArtifactRef):
    format: Literal["3dgs-ply", "sog-v2"]
    gaussian_count: int = Field(gt=0)


class LabelSet(ArtifactRef):
    format: Literal["npy-uint16", "ply-property-uint16"]
    gaussian_count: int = Field(gt=0)
    method: str = Field(min_length=1)
    method_version: str = Field(min_length=1)
    confidence_path: str | None = None

    @field_validator("confidence_path")
    @classmethod
    def confidence_path_is_relative_and_contained(cls, value: str | None) -> str | None:
        return validate_artifact_path(value) if value is not None else None


class Transform(StrictModel):
    translation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation_xyzw: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    uniform_scale: float = Field(default=1.0, gt=0)


class ObjectRecord(StrictModel):
    object_id: int = Field(ge=1, le=65533)
    name: str = Field(min_length=1)
    movable: bool = True
    initial_transform: Transform = Field(default_factory=Transform)
    notes: str | None = None


class SceneManifest(StrictModel):
    schema_version: Literal["0.1"]
    scene_id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    display_name: str = Field(min_length=1)
    coordinate_system: CoordinateSystem
    source: SourceScene
    cameras: ArtifactRef | None = None
    labels: LabelSet | None = None
    objects: list[ObjectRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def counts_and_ids_are_consistent(self) -> SceneManifest:
        if self.labels and self.labels.gaussian_count != self.source.gaussian_count:
            raise ValueError("label and source Gaussian counts must match")
        ids = [record.object_id for record in self.objects]
        if len(ids) != len(set(ids)):
            raise ValueError("object_id values must be unique")
        if self.objects and self.labels is None:
            raise ValueError("objects require a label set")
        return self
