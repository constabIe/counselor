from __future__ import annotations
import json, datetime as dt
from typing import Any, Dict, List

from aihr.llm.scibox_client import SciBoxConfig
from aihr.llm.tasks import task_hr_query_tags, TaskResult

AGE_BUCKETS = [(18,25,"18-25"), (26,30,"26-30"), (31,45,"31-45"),
               (46,50,"46-50"), (51,55,"51-55"), (56,60,"56-60")]

def _bucket_from_range(age_min: int | None, age_max: int | None) -> str | None:
    if age_min is None and age_max is None:
        return None
    mn = 0 if age_min is None else max(0, int(age_min))
    mx = 200 if age_max is None else max(mn, int(age_max))
    best = None
    best_overlap = -1
    for lo, hi, tag in AGE_BUCKETS:
        left = max(mn, lo)
        right = min(mx, hi)
        overlap = max(0, right - left + 1)
        if overlap > best_overlap:
            best_overlap = overlap
            best = tag
    return best if best_overlap > 0 else None

def _upper_list_unique(tags: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for t in tags:
        if not isinstance(t, str): 
            continue
        u = t.strip().upper()
        if not u:
            continue
        key = u.lower()
        if key in seen: 
            continue
        seen.add(key)
        out.append(u)
    return out

def _prefs_summary_text(prefs: Dict[str, Any]) -> str:
    filters = prefs.get("filters") or {}
    parts: List[str] = []

    if prefs.get("query"):
        parts.append(str(prefs["query"]))

    if filters.get("department"):
        parts.append(f"Department: {filters['department']}")
    if filters.get("level"):
        parts.append(f"Level: {filters['level']}")

    exp_min = filters.get("experience_years_min")
    exp_max = filters.get("experience_years_max")
    if isinstance(exp_min, (int,float)) or isinstance(exp_max, (int,float)):
        parts.append(f"Experience: {exp_min or 0}-{exp_max or 50} years")

    skills = filters.get("skills") or []
    if isinstance(skills, list) and skills:
        parts.append("Skills: " + ", ".join([str(s) for s in skills if isinstance(s, str)]))

    langs = filters.get("languages") or []
    if isinstance(langs, list) and langs:
        parts.append("Languages: " + ", ".join([str(l) for l in langs if isinstance(l, str)]))

    if filters.get("education_level"):
        parts.append(f"Education: {filters['education_level']}")

    a_min = filters.get("age_min")
    a_max = filters.get("age_max")
    if isinstance(a_min, int) or isinstance(a_max, int):
        parts.append(f"Age range: {a_min or ''}-{a_max or ''}")

    return "\n".join(parts)

def generate_hr_query_tags_llm(
    prefs: Dict[str, Any],
    *,
    k: int = 20,
    cfg: SciBoxConfig | None = None,
) -> Dict[str, Any]:
    if not isinstance(prefs, dict):
        raise TypeError("prefs must be a dict")

    f = prefs.get("filters") or {}
    hint = _bucket_from_range(
        f.get("experience_years_min" if False else "age_min"),
        f.get("age_max"),
    )

    prefs_json = json.dumps(prefs, ensure_ascii=False, indent=2)
    summary_text = _prefs_summary_text(prefs)

    res: TaskResult = task_hr_query_tags(
        prefs_json=prefs_json,
        summary_text=summary_text,
        k=k,
        age_bucket_hint=hint or "",
        cfg=cfg,
    )

    raw = []
    if isinstance(res.payload, dict):
        raw = res.payload.get("tags") or []
    tags = _upper_list_unique(raw)

    if hint:
        up = hint.upper()
        if up not in tags:
            tags.insert(0, up)

    tags = tags[:k]
    return {
        "tags": tags,
        "request": {"type": "tags_hr_query", "format": "json", "model": res.meta.get("model") or ""}
    }