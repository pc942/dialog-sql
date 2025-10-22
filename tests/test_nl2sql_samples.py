
from services.api.app.sql.compiler import NLCompiler

def test_avg_by_product_line_quarter():
    c = NLCompiler()
    plan = c.compile("average order value by product line in Q1 2025")
    assert "AVG" in plan.sql
    assert "product_line" in plan.sql
    assert "created_at" in plan.sql
