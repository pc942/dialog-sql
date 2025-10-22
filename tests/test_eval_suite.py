
from scripts.evaluate_nl2sql import normalize
from services.api.app.sql.compiler import NLCompiler

def test_eval_subset_passes():
    c = NLCompiler()
    sql = normalize(c.compile("average order value by product line in Q1 2025").sql)
    assert "avg" in sql and "product_line" in sql and "created_at" in sql
