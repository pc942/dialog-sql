
from __future__ import annotations
import duckdb
from typing import Any, List, Dict

class DuckDBGateway:
    def __init__(self, postgres_url: str):
        self.con = duckdb.connect()
        self.con.install_extension("postgres")
        self.con.load_extension("postgres")
        # Attach Postgres
        self.con.execute("ATTACH 'dbname=dialog user=dialog password=dialog host=postgres port=5432' AS pg (TYPE POSTGRES)")

    def execute(self, sql: str) -> List[Dict[str, Any]]:
        rs = self.con.execute(sql).fetchall()
        cols = [d[0] for d in self.con.description]
        return [dict(zip(cols, row)) for row in rs]

    def explain(self, sql: str) -> str:
        # DuckDB EXPLAIN returns a single-row plan text in column 1
        plan = self.con.execute(f"EXPLAIN {sql}").fetchall()
        return "\n".join(str(r[0]) for r in plan)
