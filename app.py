"""FastAPI service exposing the pivot JSON Schemas of the VLM title-page extraction."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

SCHEMAS_DIR = Path(__file__).parent / "schemas"
# Loaded once: the schemas only change with a new deployment.
SCHEMAS: dict[str, dict[str, Any]] = {
    path.name.removesuffix(".schema.json"): json.loads(path.read_text(encoding="utf-8"))
    for path in sorted(SCHEMAS_DIR.glob("*.schema.json"))
}

app = FastAPI(
    title="Humatheque Extraction Schemas",
    version="0.1.0",
    description=(
        "Pivot JSON Schemas of the VLM title-page extraction. They describe the POST body "
        "of the downstream APIs (alma-checker, sudoc-checker, idref-linker), which fetch "
        "them from here instead of each embedding a copy."
    ),
)
# Read-only public documents: any front end (Gradio, docs) may fetch them.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "service": "humatheque-extraction-schemas",
        "version": app.version,
        "docs": "/docs",
        "schemas": "/schemas",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True}


@app.get("/schemas")
def list_schemas() -> dict[str, Any]:
    return {
        "schemas": [
            {"kind": kind, "title": schema.get("title"), "id": schema.get("$id"), "url": f"/schemas/{kind}"}
            for kind, schema in SCHEMAS.items()
        ]
    }


@app.get("/schemas/{kind}")
def get_schema(kind: str) -> dict[str, Any]:
    """JSON Schema for `thesis` or `dissertation`.

    `/schemas/thesis.schema.json` is accepted too, so a client built on the raw GitHub
    layout (`{base}/{kind}.schema.json`) only has to change its base URL.
    """
    kind = kind.removesuffix(".schema.json")
    if kind not in SCHEMAS:
        raise HTTPException(status_code=404, detail=f"Unknown schema {kind!r}. Available: {sorted(SCHEMAS)}.")
    return SCHEMAS[kind]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
