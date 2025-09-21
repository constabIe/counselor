import os, sys, pathlib, json
THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[1]; SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.tags import generate_hr_query_tags_llm

PREFS = {
  "query": "Нужен backend, английский C1, ответственность",
  "filters": {
    "department": "Engineering",
    "experience_years_min": 3,
    "experience_years_max": 6,
    "skills": ["Python","FastAPI","PostgreSQL"],
    "level": "Middle",
    "languages": ["English C1","Russian native"],
    "education_level": "Bachelor+",
    "age_min": 26,
    "age_max": 35
  }
}

def main():
    cfg = SciBoxConfig(
        api_key=os.getenv("SCIBOX_API_KEY", ""),
        base_url=os.getenv("SCIBOX_BASE_URL", "https://llm.t1v.scibox.tech/v1"),
        chat_model=os.getenv("SCIBOX_MODEL", "Qwen2.5-72B-Instruct-AWQ"),
    )
    res = generate_hr_query_tags_llm(PREFS, k=20, cfg=cfg)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()