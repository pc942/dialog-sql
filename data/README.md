# Dialog SQL

Conversational SQL engine. DuckDB federates Postgres; SQLGlot compiles NL→SQL; OPA enforces row filters.
This repo uses Poetry + Makefile. Keep commits small.

## Dev
- `make dev-up`    # start services
- `make dev-down`
- `make test`
- `make dbt-run`   # build dbt views (optional)

## API
- `GET /health`
- `GET /schemas`
- `POST /query`    # body: {"question": "...", "materialize_as": "optional_name"}

## Notes
- Set `X-User` header for RLS.
- If dbt is enabled, models go to `analytics/dbt/models/generated/`.
