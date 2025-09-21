from __future__ import annotations
import re, datetime as dt
from typing import Any, Dict, List

ALLOWED_TOP_KEYS = {
    "name","surname","gender","age","date_of_birth","summary",
    "contacts","education","experience","skills","languages",
    "projects","awards","hobbies","request"
}

DATE_FORMATS = [
    "%d/%m/%Y", "%d.%m.%Y", "%Y-%m-%d", "%d-%m-%Y",
    "%m/%d/%Y", "%m-%d-%Y"
]

def _parse_dob(dob: str) -> dt.date | None:
    dob = (dob or "").strip()
    if not dob:
        return None
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(dob, fmt).date()
        except Exception:
            pass
    return None

def _calc_age(born: dt.date, today: dt.date) -> int:
    years = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        years -= 1
    return max(years, 0)

def _normalize_phone(p: str) -> str:
    return re.sub(r"[^\d+]", "", p or "")

def _norm_gender(g: Any) -> str:
    if not isinstance(g, str):
        return ""
    v = g.strip().lower()
    if v == "male": return "Male"
    if v == "female": return "Female"
    return ""

def _title_case_lang(name: str) -> str:
    name = (name or "").strip()
    if not name:
        return ""
    return name.lower().capitalize()

def _prune_top_keys(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if k in ALLOWED_TOP_KEYS}

def _ensure_types(payload: Dict[str, Any]) -> None:
    for key in ["name","surname","date_of_birth","summary"]:
        if not isinstance(payload.get(key), str):
            payload[key] = "" if key != "summary" else (payload.get(key) or "")
    if not isinstance(payload.get("age"), int):
        payload["age"] = None
    ct = payload.get("contacts") or {}
    emails = ct.get("emails") or []
    phones = ct.get("phones") or []
    urls   = ct.get("urls") or []
    ct["emails"] = [e for e in emails if isinstance(e, str) and e.strip()]
    ct["phones"] = [_normalize_phone(p) for p in phones if isinstance(p, str) and p.strip()]
    ct["urls"]   = [u for u in urls if isinstance(u, str) and u.strip()]
    payload["contacts"] = ct
    # skills
    sk = payload.get("skills") or {}
    hard = sk.get("hard") or []
    soft = sk.get("soft") or []
    sk["hard"] = [s for s in hard if isinstance(s, str) and s.strip()]
    sk["soft"] = [s for s in soft if isinstance(s, str) and s.strip()]
    payload["skills"] = sk
    # languages — нормализуем имя языка в Title Case
    langs = payload.get("languages") or []
    norm_langs: List[Dict[str, Any]] = []
    for it in langs:
        if not isinstance(it, dict) or not it:
            continue
        if "language" in it:
            it["language"] = _title_case_lang(it.get("language",""))
        norm_langs.append(it)
    payload["languages"] = norm_langs
    # request
    rq = payload.get("request") or {}
    rq["type"] = "resume"
    rq["format"] = "json"
    rq["model"] = rq.get("model") or ""
    payload["request"] = rq

def _fallback_summary(payload: Dict[str, Any]) -> None:
    if (payload.get("summary") or "").strip():
        return
    name = " ".join([payload.get("name") or "", payload.get("surname") or ""]).strip()
    edu  = ""
    if payload.get("education"):
        e0 = payload["education"][0]
        deg = e0.get("degree") or ""
        inst = e0.get("institution") or ""
        edu = f"{deg} at {inst}".strip()
    hard = payload.get("skills", {}).get("hard") or []
    top = ", ".join(hard[:4])
    parts = []
    if name: parts.append(name)
    if edu: parts.append(edu)
    if top: parts.append(f"skills: {top}")
    payload["summary"] = " — ".join(parts) if parts else ""

def sanitize_resume(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload = _prune_top_keys(payload)

    payload["gender"] = _norm_gender(payload.get("gender"))
    _ensure_types(payload)

    dob = payload.get("date_of_birth") or ""
    dob_date = _parse_dob(dob) if isinstance(dob, str) else None
    if dob_date:
        today = dt.datetime.now(dt.timezone.utc).date()
        payload["age"] = _calc_age(dob_date, today)

    _fallback_summary(payload)

    return payload