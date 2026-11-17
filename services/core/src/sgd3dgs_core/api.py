"""Local API skeleton.

The service intentionally exposes only a health endpoint at project start. GPU
jobs are added only after their CLI pipeline is reproducible.
"""

from fastapi import FastAPI

from sgd3dgs_core import __version__

app = FastAPI(title="SGD3DGS Core", version=__version__)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}
