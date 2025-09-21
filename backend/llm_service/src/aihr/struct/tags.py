# src/aihr/struct/tags.py
from __future__ import annotations
import json, datetime as dt
from typing import Any, Dict, List, Iterable

from aihr.llm.scibox_client import SciBoxConfig
from aihr.llm.tasks import (
    task_resume_tags,
    task_generate_tags,
    task_hr_query_tags,
    TaskResult,
)


AGE_BUCKETS = [
    (18, 25, "18-25"),
    (26, 30, "26-30"),
    (31, 45, "31-45"),
    (46, 50, "46-50"),
    (51, 55, "51-55"),
    (56, 60, "56-60"),
]

def _upper_list_unique(tags: Iterable[str]) -> List[str]:
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

def _bucket_from_age(age: int | None) -> str | None:
    if age is None:
        return None
    try:
        a = int(age)
    except Exception:
        return None
    for lo, hi, tag in AGE_BUCKETS:
        if lo <= a <= hi:
            return tag
    return None

def _bucket_from_birthdate(date_str: str | None) -> str | None:
    if not date_str or not isinstance(date_str, str):
        return None
    s = date_str.strip()
    if not s:
        return None
    fmts = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y", "%m/%d/%Y"]
    for f in fmts:
        try:
            d = dt.datetime.strptime(s, f).date()
            today = dt.date.today()
            age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
            return _bucket_from_age(age)
        except Exception:
            continue
    return None

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

def _resume_json_to_text(resume: Dict[str, Any]) -> str:
    parts: List[str] = []
    name = " ".join([str(resume.get("name") or ""), str(resume.get("surname") or "")]).strip()
    if name:
        parts.append(name)

    summary = resume.get("summary") or ""
    if summary:
        parts.append(summary)

    skills = resume.get("skills") or {}
    hard = skills.get("hard") or []
    soft = skills.get("soft") or []
    if hard:
        parts.append("Hard skills: " + ", ".join([str(x) for x in hard if isinstance(x, str)]))
    if soft:
        parts.append("Soft skills: " + ", ".join([str(x) for x in soft if isinstance(x, str)]))

    edu = resume.get("education") or []
    for e in edu if isinstance(edu, list) else []:
        if not isinstance(e, dict): continue
        deg = e.get("degree") or ""
        inst = e.get("institution") or ""
        loc = e.get("location") or ""
        per = e.get("period") or ""
        row = ", ".join([v for v in [deg, inst, loc, per] if v])
        if row: parts.append(f"Education: {row}")

    exp = resume.get("experience") or []
    for r in exp if isinstance(exp, list) else []:
        if not isinstance(r, dict): continue
        comp = r.get("company") or ""
        role = r.get("role") or ""
        loc  = r.get("location") or ""
        start= r.get("start") or ""
        end  = r.get("end") or ""
        resp = r.get("responsibilities") or []
        row1 = ", ".join([v for v in [role, comp, loc] if v])
        row2 = " ".join([v for v in [start, "-", end] if v])
        if row1: parts.append(f"Experience: {row1} {row2}".strip())
        if isinstance(resp, list) and resp:
            parts.append("Responsibilities: " + "; ".join([str(x) for x in resp if isinstance(x, str)]))

    langs = resume.get("languages") or []
    if isinstance(langs, list) and langs:
        arr = []
        for l in langs:
            if not isinstance(l, dict): continue
            nm = l.get("language") or ""
            lv = l.get("level") or ""
            if nm:
                arr.append(f"{nm} {lv}".strip())
        if arr:
            parts.append("Languages: " + ", ".join(arr))

    hobbies = resume.get("hobbies") or []
    if isinstance(hobbies, list) and hobbies:
        parts.append("Hobbies: " + ", ".join([str(x) for x in hobbies if isinstance(x, str)]))

    return "\n".join(parts)

def generate_tags(
    data: Dict[str, Any] | str,
    *,
    k: int = 15,
    cfg: SciBoxConfig | None = None,
) -> Dict[str, Any]:
    cfg = cfg or SciBoxConfig()

    if isinstance(data, dict):
        text = _resume_json_to_text(data)
        age_hint = _bucket_from_age(data.get("age")) or _bucket_from_birthdate(data.get("date_of_birth"))

        res: TaskResult = task_resume_tags(
            text,
            k=k,
            age_bucket_hint=age_hint or "",
            cfg=cfg,
        )
        raw = []
        if isinstance(res.payload, dict):
            raw = res.payload.get("tags") or []
        tags = _upper_list_unique(raw)[:k]

        if age_hint:
            up = age_hint.upper()
            if up not in tags:
                tags.insert(0, up)
                tags = tags[:k]

        model_used = res.meta.get("model") or ""
        return {"tags": tags, "request": {"type": "tags", "format": "json", "model": model_used}}

    text = str(data or "")
    res: TaskResult = task_generate_tags(text, k=k, cfg=cfg)
    payload = res.payload if isinstance(res.payload, dict) else {}
    tags = _upper_list_unique(payload.get("tags") or [])[:k]
    model_used = res.meta.get("model") or ""
    return {"tags": tags, "request": {"type": "tags", "format": "json", "model": model_used}}

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
    if isinstance(exp_min, (int, float)) or isinstance(exp_max, (int, float)):
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

    cfg = cfg or SciBoxConfig()
    f = prefs.get("filters") or {}
    age_hint = _bucket_from_range(f.get("age_min"), f.get("age_max"))

    prefs_json = json.dumps(prefs, ensure_ascii=False, indent=2)
    summary_text = _prefs_summary_text(prefs)

    res: TaskResult = task_hr_query_tags(
        prefs_json=prefs_json,
        summary_text=summary_text,
        k=k,
        age_bucket_hint=age_hint or "",
        cfg=cfg,
    )

    raw = []
    if isinstance(res.payload, dict):
        raw = res.payload.get("tags") or []
    tags = _upper_list_unique(raw)

    if age_hint:
        up = age_hint.upper()
        if up not in tags:
            tags.insert(0, up)

    tags = tags[:k]
    return {
        "tags": tags,
        "request": {
            "type": "tags_hr_query",
            "format": "json",
            "model": res.meta.get("model") or "",
        },
    }