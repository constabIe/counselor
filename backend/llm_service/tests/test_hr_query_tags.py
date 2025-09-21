from __future__ import annotations
import os, sys, json, pathlib
THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[1]; SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.tags import generate_hr_query_tags_llm

PREFS = {
  "query": "Нужен бэкенд, ownership, английский C1+",
  "filters": {
    "department": "Engineering",
    "experience_years_min": 2,
    "experience_years_max": 5,
    "skills": ["Python","FastAPI","PostgreSQL","Docker","K8s"],
    "level": "Middle",
    "languages": ["English C1","Russian native"],
    "education_level": "Bachelor+",
    "age_min": 26,
    "age_max": 35
  }
}

def main():
    api_key = os.getenv("SCIBOX_API_KEY","")
    if not api_key:
        print("Ошибка: SCIBOX_API_KEY is empty"); return

    cfg = SciBoxConfig(
        api_key=api_key,
        base_url=os.getenv("SCIBOX_BASE_URL","https://llm.t1v.scibox.tech/v1"),
        chat_model=os.getenv("SCIBOX_MODEL","Qwen2.5-72B-Instruct-AWQ"),
    )

    res = generate_hr_query_tags_llm(PREFS, k=20, cfg=cfg)

    tags = res.get("tags", [])
    print("\nСгенерированные теги:")
    for t in tags:
        print("-", t)

if __name__ == "__main__":
    main()