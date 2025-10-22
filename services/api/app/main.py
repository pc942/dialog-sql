
<<<<<<< HEAD
from fastapi import FastAPI
app = FastAPI(title="Dialog SQL API", version="0.1.0")

@app.get("/health")
async def health():
    return {"ok": True}
=======
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import subprocess

from app.config import Settings
from app.sql.compiler import NLCompiler
from app.exec.duckdb_gateway import DuckDBGateway
from app.security.opa import OPAAuthorizer
from app.lineage.dbt_capture import materialize_view

APP_NAME = "dialog-sql-api"
app = FastAPI(title="Dialog SQL API", version="0.2.0")

settings = Settings()
compiler = NLCompiler()
gateway = DuckDBGateway(settings.database_url)
authorizer = OPAAuthorizer(settings.opa_url, ttl_seconds=settings.opa_cache_ttl_seconds)

class QueryIn(BaseModel):
    question: str
    dry_run: bool = False
    materialize_as: Optional[str] = None

@app.get("/health")
async def health():
    return {"ok": True, "service": APP_NAME}
>>>>>>> 6d1d32e (Final push)

@app.get("/schemas")
async def schemas():
    return {
        "tables": {
            "customers": ["customer_id", "name", "region"],
            "orders": ["order_id", "customer_id", "product_line", "amount", "created_at"],
        }
    }
<<<<<<< HEAD
=======

@app.post("/query")
async def query(q: QueryIn, x_user: Optional[str] = Header(default=None, alias="X-User")):
    if x_user is None:
        raise HTTPException(status_code=400, detail="X-User header required for policy evaluation")
    plan = compiler.compile(q.question)
    predicate = authorizer.get_row_predicate(user=x_user, tables=["customers", "orders"])
    sql = compiler.inject_predicate(plan.sql, predicate) if predicate else plan.sql

    materialized = None
    if q.materialize_as:
        materialized = materialize_view(settings.dbt_models_outdir, q.materialize_as, sql)
        if settings.dbt_materialize_on_query:
            try:
                subprocess.run(["dbt", "run"], cwd="/app/analytics/dbt", check=False)
            except Exception:
                pass

    if q.dry_run:
        explain = gateway.explain(sql)
        return JSONResponse({"sql": sql, "explain": explain, "materialized": materialized})

    rows = gateway.execute(sql)
    return JSONResponse({"sql": sql, "rows": rows, "rowcount": len(rows), "materialized": materialized})
>>>>>>> 6d1d32e (Final push)
