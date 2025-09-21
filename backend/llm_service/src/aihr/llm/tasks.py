from __future__ import annotations
import json
from dataclasses import dataclass

from .scibox_client import SciBoxClient, SciBoxConfig
from .schemas import ensure_valid_resume


@dataclass
class TaskResult:
    type: str
    payload: dict | list | str
    meta: dict


# ---------- 1) Структуризация резюме ----------
SYSTEM_STRUCTURE = (
    "Ты — сервис структурирования резюме. "
    "Верни строго JSON."
)

USER_STRUCTURE_TMPL = """Структурируй текст резюме в JSON по схеме и правилам ниже.

Требования к ответу:
- Ответ — только валидный JSON-объект и СТРОГО по схеме. Не добавляй никаких лишних полей.
- summary: краткое общее впечатление о кандидате (1–3 предложения). Если совсем нечего добавить — одна короткая фраза по профилю навыков.
- Не добавляй поля, которых нет в схеме (например, "source"). Если таких полей в тексте много — игнорируй их.
- Следи за типами: строки — только строки; числа — только числа или null. Не возвращай "null" как строку.
- Приводи названия языков в Title Case (English, Russian, German, Korean).

Схема JSON (пустые значения допустимы):
```json
{schema}
{text}
```"""

DEFAULT_SCHEMA = {
    "name": "",
    "surname": "",
    "gender": "",
    "age": None,
    "date_of_birth": "",
    "summary": "",
    "contacts": {"emails": [], "phones": [], "urls": []},
    "education": [],
    "experience": [],
    "skills": {"hard": [], "soft": []},
    "languages": [],
    "projects": [],
    "awards": [],
    "hobbies": [],
    "request": {
        "type": "resume",
        "format": "json",
        "model": ""
    }
}


def _coerce_json(text: str) -> dict:
    import re, json as _json
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.S) or re.search(r"(\{.*\})", text, flags=re.S)
    if not m:
        raise ValueError("LLM response has no JSON")
    return _json.loads(m.group(1))


def task_structure_resume(
    text: str,
    *,
    cfg: SciBoxConfig | None = None,
    schema: dict | None = None
) -> TaskResult:
    client = SciBoxClient(cfg or SciBoxConfig())
    effective_schema = schema or DEFAULT_SCHEMA

    user = USER_STRUCTURE_TMPL.format(
        schema=json.dumps(effective_schema, ensure_ascii=False, indent=2),
        text=text[:120000]
    )

    content = client.chat(
        messages=[{"role": "system", "content": SYSTEM_STRUCTURE},
                  {"role": "user", "content":user}],
        response_json=True,
        temperature=0.0,
        top_p=1.0,
        max_tokens=2000,
    )

    payload = _coerce_json(content)
    used_model = getattr(client, "chat_model", None) or (cfg or SciBoxConfig()).chat_model

    payload.setdefault("request", {})
    payload["request"].setdefault("type", "resume")
    payload["request"].setdefault("format", "json")
    payload["request"]["model"] = payload["request"].get("model") or used_model

    ensure_valid_resume(payload)
    return TaskResult(type="structured_resume", payload=payload, meta={"model": used_model})


# ---------- 2) Теги резюме (HR-формат) ----------
SYSTEM_RESUME_TAGS = (
    "Ты — ассистент по тегированию резюме для HR. "
    "Всегда возвращай ТОЛЬКО валидный JSON вида {\"tags\": [\"...\"]}. "
    "Без комментариев, без пояснений, без Markdown."
)

USER_RESUME_TAGS_TMPL = """Сгенерируй до {k} тегов для кандидата по тексту резюме ниже.
ТРЕБОВАНИЯ К ФОРМАТУ:
- Верни ТОЛЬКО JSON: {{"tags": ["...", "..."]}}
- Каждый тег — СТРОКА в ВЕРХНЕМ РЕГИСТРЕ.
- Обязательно включи ОДИН возрастной диапазон из набора: "18-25", "26-30", "31-45", "46-50", "51-55", "56-60".
- Остальные теги — полезные навыки (технологии/инструменты), а также важные должности/направления из опыта.
- Не используй персональные данные (имя, почта, телефоны) в тегах.
- Не добавляй ничего, кроме списка тегов.

Подсказка по возрасту (можешь использовать или проверить по тексту): {age_bucket_hint}

ТЕКСТ РЕЗЮМЕ:
```text
{text}
```"""


def task_resume_tags(
    text: str,
    *,
    k: int = 20,
    age_bucket_hint: str = "",
    cfg: SciBoxConfig | None = None,
) -> TaskResult:
    client = SciBoxClient(cfg or SciBoxConfig())
    content = client.chat(
        messages=[
            {"role": "system", "content": SYSTEM_RESUME_TAGS},
            {"role": "user", "content": USER_RESUME_TAGS_TMPL.format(
                k=k,
                age_bucket_hint=age_bucket_hint or "неизвестно",
                text=text[:120000]
            )}
        ],
        response_json=True,
        temperature=0.0,
        top_p=1.0,
        max_tokens=600,
    )
    data = _coerce_json(content)
    tags = data.get("tags") or []
    if not isinstance(tags, list):
        raise ValueError("LLM returned invalid resume tags payload")

    used_model = getattr(client, "chat_model", None) or (cfg or SciBoxConfig()).chat_model
    return TaskResult(type="resume_tags", payload={"tags": tags}, meta={"model": used_model})

# ---------- 6) Теги для HR-запроса (по предпочтениям) ----------
SYSTEM_HR_QUERY_TAGS = (
    "Ты — ассистент по тегированию для HR. "
    "Всегда возвращай ТОЛЬКО валидный JSON вида {\"tags\": [\"...\"]}. "
    "Без комментариев, без пояснений, без Markdown."
)

USER_HR_QUERY_TAGS_TMPL = """Сгенерируй до {k} тегов, отражающих HR-предпочтения ниже.
ТРЕБОВАНИЯ К ФОРМАТУ:
- Верни ТОЛЬКО JSON: {{"tags": ["...", "..."]}}
- Каждый тег — СТРОКА в ВЕРХНЕМ РЕГИСТРЕ.
- Обязательно включи ОДИН возрастной диапазон из набора: "18-25", "26-30", "31-45", "46-50", "51-55", "56-60".
- Остальные теги — целевые навыки/технологии/ролі/уровни и важные признаки из запроса (департамент, уровень, языки, образование, опыт).
- Не добавляй персональные данные. Только признаки профиля.

Подсказка по возрасту (используй, если релевантно): {age_bucket_hint}

HR-ПРЕДПОЧТЕНИЯ (JSON):
```json
{prefs_json}
{summary_text}
```"""

def task_hr_query_tags(
    *,
    prefs_json: str,
    summary_text: str,
    k: int = 20,
    age_bucket_hint: str = "",
    cfg: SciBoxConfig | None = None,
) -> TaskResult:
    client = SciBoxClient(cfg or SciBoxConfig())
    content = client.chat(
        messages=[
            {"role": "system", "content": SYSTEM_HR_QUERY_TAGS},
            {"role": "user", "content": USER_HR_QUERY_TAGS_TMPL.format(
                k=k,
                age_bucket_hint=age_bucket_hint or "неизвестно",
                prefs_json=prefs_json[:20000],
                summary_text=summary_text[:4000],
            )}
        ],
        response_json=True,
        temperature=0.0,
        top_p=1.0,
        max_tokens=600,
    )
    data = _coerce_json(content)
    tags = data.get("tags") or []
    if not isinstance(tags, list):
        raise ValueError("LLM returned invalid HR query tags payload")

    used_model = getattr(client, "chat_model", None) or (cfg or SciBoxConfig()).chat_model
    return TaskResult(type="hr_query_tags", payload={"tags": tags}, meta={"model": used_model})
