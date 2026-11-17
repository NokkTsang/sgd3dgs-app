"""Small, dependable commands shared by local development and CI."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console

from sgd3dgs_core.manifest import load_manifest, sha256_file, verify_artifacts

app = typer.Typer(no_args_is_help=True, help="SGD3DGS scene-contract utilities.")
console = Console()


@app.command()
def validate(
    manifest_path: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    check_files: Annotated[
        bool,
        typer.Option(
            "--check-files",
            help="Also verify referenced files and their SHA-256 values.",
        ),
    ] = False,
) -> None:
    """Validate a versioned scene manifest."""
    try:
        manifest = load_manifest(manifest_path)
    except ValidationError as validation_error:
        console.print("[red]Manifest validation failed.[/red]")
        console.print(validation_error)
        raise typer.Exit(code=1) from validation_error

    if check_files:
        artifact_errors = verify_artifacts(manifest_path, manifest)
        if artifact_errors:
            console.print("[red]Artifact verification failed:[/red]")
            for artifact_error in artifact_errors:
                console.print(f"- {artifact_error}")
            raise typer.Exit(code=1)

    console.print(
        f"[green]Valid[/green] scene={manifest.scene_id} "
        f"gaussians={manifest.source.gaussian_count:,} objects={len(manifest.objects)}"
    )


@app.command()
def checksum(
    path: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
) -> None:
    """Print a file's SHA-256 checksum."""
    console.print(sha256_file(path))
