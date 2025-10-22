
from __future__ import annotations
import pyarrow as pa
import pyarrow.flight as fl
from app.exec.duckdb_gateway import DuckDBGateway
from app.config import Settings

class QueryFlightServer(fl.FlightServerBase):
    def __init__(self, location: str, gateway: DuckDBGateway):
        super().__init__(location)
        self.gateway = gateway

    def do_get(self, context, ticket: fl.Ticket) -> fl.FlightDataStream:
        sql = ticket.ticket.decode()
        rows = self.gateway.execute(sql)
        if not rows:
            empty = pa.table({})
            return fl.RecordBatchStream(empty)
        cols = rows[0].keys()
        arrays = {c: pa.array([r[c] for r in rows]) for c in cols}
        table = pa.table(arrays)
        return fl.RecordBatchStream(table)

def make_server() -> QueryFlightServer:
    settings = Settings()
    gw = DuckDBGateway(settings.database_url)
    return QueryFlightServer(f"grpc://{settings.flight_addr}:{settings.flight_port}", gw)
