
from __future__ import annotations
import pathlib

def materialize_view(models_outdir: str, model_name: str, sql: str) -> str:
    """
    Write a dbt model that materializes the provided SQL as a view.
    Returns the path to the generated model file.
    """
    safe = "".join(c if (c.isalnum() or c in ("_", "-")) else "_" for c in model_name).lower()
    outdir = pathlib.Path(models_outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / f"{safe}.sql"
    payload = "{{ config(materialized='view') }}\n" + sql + "\n"
    path.write_text(payload, encoding="utf-8")
    return str(path)
