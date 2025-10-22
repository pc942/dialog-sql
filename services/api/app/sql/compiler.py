
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import re
import sqlglot
from sqlglot import expressions as exp

TIME_QUARTER = re.compile(r"(q([1-4]))\s*(20\d{2})", re.I)

@dataclass
class Plan:
    sql: str
    tables: List[str]

class NLCompiler:
    """
    Minimal hybrid parser for common analytics phrasing.
    You can later add a transformer to improve recall.
    """

    def compile(self, text: str) -> Plan:
        t = text.lower()
        agg_func = "AVG" if any(k in t for k in ("avg", "average", "mean")) else None
        metric = "amount" if ("order value" in t or "amount" in t) else "amount"
        group_by = "product_line" if ("by product line" in t or "product line" in t) else None

        time_pred = None
        mq = TIME_QUARTER.search(t)
        if mq:
            q = int(mq.group(2))
            y = int(mq.group(3))
            start_month = 1 + (q - 1) * 3
            end_month = start_month + 3
            time_pred = f"o.created_at >= DATE '{y}-{start_month:02d}-01' AND o.created_at < DATE '{y}-{end_month:02d}-01'"

        selects = []
        if group_by:
            selects.append(exp.column(group_by, table="o"))
        if agg_func:
            selects.append(exp.alias_(exp.Func(agg_func, expressions=[exp.column(metric, table="o")]), "avg_order_value"))
        else:
            selects.append(exp.Star())

        from_orders = exp.alias_("orders", "o")
        join_customers = exp.Join(
            this=exp.to_table("customers").as_("c"),
            on=exp.condition(
                exp.EQ(
                    this=exp.column("customer_id", table="c"),
                    expression=exp.column("customer_id", table="o"),
                )
            ),
            join_type="INNER",
        )

        where = sqlglot.parse_one(time_pred, read="duckdb") if time_pred else None
        query = (exp.select(*selects).from_(from_orders).join(join_customers))
        if where:
            query = query.where(where)
        if group_by:
            query.set("group", exp.Group(expressions=[exp.column(group_by, table="o")]))

        sql = query.sql(dialect="duckdb")
        return Plan(sql=sql, tables=["customers", "orders"])

    def inject_predicate(self, sql: str, predicate: str) -> str:
        if not predicate:
            return sql
        # Wrap and filter
        return f"SELECT * FROM ({sql}) AS sub WHERE {predicate}"
