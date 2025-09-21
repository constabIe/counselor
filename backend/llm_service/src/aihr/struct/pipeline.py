from __future__ import annotations
from typing import Any, Dict
from aihr.llm.scibox_client import SciBoxConfig
from aihr.llm.tasks import task_structure_resume, TaskResult
from aihr.struct.sanitize import sanitize_resume
from aihr.struct.tags import generate_tags

def structure_from_extract_json(extract: Dict[str, Any], *, cfg: SciBoxConfig | None = None) -> Dict[str, Any]:
    raw_text: str = extract.get("text") or ""
    res: TaskResult = task_structure_resume(raw_text, cfg=cfg)
    payload = res.payload if isinstance(res.payload, dict) else {}
    clean = sanitize_resume(payload)
    return clean

def structure_and_tags_from_extract_json(extract: Dict[str, Any], *, cfg: SciBoxConfig | None = None, k_tags: int = 15) -> Dict[str, Any]:
    resume = structure_from_extract_json(extract, cfg=cfg)
    tags = generate_tags(resume, k=k_tags, cfg=cfg)
    return {"resume": resume, "tags": tags}