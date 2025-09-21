from __future__ import annotations
import json
from typing import Any, Dict

from aihr.llm.scibox_client import SciBoxConfig
from aihr.llm.tasks import task_structure_resume, TaskResult
from aihr.struct.sanitize import sanitize_resume

def structure_from_extract_json(
    extract_json: Dict[str, Any],
    *,
    cfg: SciBoxConfig | None = None,
    schema: dict | None = None,
) -> Dict[str, Any]:
    if not isinstance(extract_json, dict):
        raise TypeError("extract_json must be a dict")

    raw_text = (extract_json.get("text") or "").strip()
    if not raw_text:
        raise ValueError("extract_json['text'] is empty")

    res: TaskResult = task_structure_resume(raw_text, cfg=cfg, schema=schema)
    payload = res.payload if isinstance(res.payload, dict) else {}

    payload.setdefault("request", {})
    payload["request"].setdefault("type", "resume")
    payload["request"].setdefault("format", "json")
    payload["request"].setdefault("model", res.meta.get("model"))

    payload = sanitize_resume(payload)

    return payload

def structure_from_extract_json_str(extract_json_str: str, *, cfg: SciBoxConfig | None = None, schema: dict | None = None) -> Dict[str, Any]:
    obj = json.loads(extract_json_str)
    return structure_from_extract_json(obj, cfg=cfg, schema=schema)