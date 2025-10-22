
from pydantic import BaseModel
import os

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://dialog:dialog@postgres:5432/dialog")
    opa_url: str = os.getenv("OPA_URL", "http://opa:8181/v1/data/rowfilter/allow")
    dbt_models_outdir: str = os.getenv("DBT_MODELS_OUTDIR", "/app/analytics/dbt/models/generated")
    dbt_materialize_on_query: bool = os.getenv("DBT_MATERIALIZE_ON_QUERY", "false").lower() == "true"
    llm_model_name: str = os.getenv("LLM_MODEL_NAME", "sshleifer/tiny-distilroberta-base")
    flight_addr: str = os.getenv("FLIGHT_ADDR", "0.0.0.0")
    flight_port: int = int(os.getenv("FLIGHT_PORT", "8815"))
    opa_cache_ttl_seconds: int = int(os.getenv("OPA_CACHE_TTL_SECONDS", "60"))
