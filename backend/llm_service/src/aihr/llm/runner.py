from __future__ import annotations
from typing import Any, Dict

from .scibox_client import SciBoxConfig
from .tasks import (
    task_structure_resume, task_generate_tags, task_classify, task_embed, TaskResult
)

def run_task(kind: str, payload: Dict[str, Any], *, cfg: SciBoxConfig | None = None) -> TaskResult:
    """
    Унифицированная точка входа:
      - kind="structure_resume"  payload: {"text": "...", "schema": optional}
      - kind="tags"              payload: {"text": "...", "k": 15}
      - kind="classify"          payload: {"text": "...", "labels": ["A","B"], "multi": true}
      - kind="embed"             payload: {"chunks": ["...","..."]}
    """
    if kind == "structure_resume":
        return task_structure_resume(payload["text"], cfg=cfg, schema=payload.get("schema"))
    if kind == "tags":
        return task_generate_tags(payload["text"], k=payload.get("k", 15), cfg=cfg)
    if kind == "classify":
        return task_classify(payload["text"], labels=payload["labels"], cfg=cfg, multi=payload.get("multi", True))
    if kind == "embed":
        return task_embed(payload["chunks"], cfg=cfg)
    raise ValueError(f"Unknown task kind: {kind}")