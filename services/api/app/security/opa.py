
from __future__ import annotations
import httpx, time
from typing import List, Tuple

class OPAAuthorizer:
    def __init__(self, opa_url: str, ttl_seconds: int = 60):
        self.opa_url = opa_url
        self.ttl = ttl_seconds
        self._cache: dict[Tuple[str, tuple], tuple[float, str]] = {}

    def get_row_predicate(self, user: str, tables: List[str]) -> str:
        key = (user, tuple(sorted(tables)))
        now = time.time()
        if key in self._cache:
            exp, value = self._cache[key]
            if now < exp:
                return value

        predicate = ""
        try:
            payload = {"input": {"user": user, "tables": list(key[1])}}
            r = httpx.post(self.opa_url, json=payload, timeout=2.0)
            r.raise_for_status()
            data = r.json()
            result = data.get("result", data)
            if result.get("allow") and result.get("predicate"):
                predicate = result["predicate"]
        except Exception:
            predicate = ""

        self._cache[key] = (now + self.ttl, predicate)
        return predicate
