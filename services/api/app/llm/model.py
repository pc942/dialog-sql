
from __future__ import annotations
from typing import Optional, Dict, Any
import os

Intent = Dict[str, Any]

class TinyIntentModel:
    """
    Tries to use a small HF pipeline if available; otherwise falls back to regex cues.
    Set env LLM_MODEL_NAME to a local model directory to avoid downloads.
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv("LLM_MODEL_NAME", "sshleifer/tiny-distilroberta-base")
        self.pipe = None
        try:
            from transformers import pipeline
            self.pipe = pipeline("zero-shot-classification", model=self.model_name)
            _ = self.pipe("test", candidate_labels=["aggregation", "time", "group"])
        except Exception:
            self.pipe = None

    def infer(self, text: str) -> Intent:
        t = text.lower()
        intent: Intent = {
            "agg": "avg" if any(k in t for k in ("avg", "average", "mean")) else ("sum" if "total" in t or "sum" in t else None),
            "group_by": "product_line" if "product line" in t or "by product line" in t else None,
            "time_hint": "quarter" if any(q in t for q in ("q1","q2","q3","q4")) else None,
        }
        if self.pipe:
            try:
                res = self.pipe(t, candidate_labels=["average","sum","count","group by product","by region","by product line"])
                top = res["labels"][0].lower()
                if "average" in top:
                    intent["agg"] = "avg"
                if "sum" in top:
                    intent["agg"] = "sum"
                if "product" in top:
                    intent["group_by"] = "product_line"
            except Exception:
                pass
        return intent
