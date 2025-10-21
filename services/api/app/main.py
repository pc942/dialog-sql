
from fastapi import FastAPI
app = FastAPI(title="Dialog SQL API", version="0.1.0")

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/schemas")
async def schemas():
    return {
        "tables": {
            "customers": ["customer_id", "name", "region"],
            "orders": ["order_id", "customer_id", "product_line", "amount", "created_at"],
        }
    }
