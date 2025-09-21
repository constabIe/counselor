from __future__ import annotations
import os, sys, json, pathlib

THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[1]
SRC  = ROOT / "src"
sys.path.insert(0, str(SRC))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.tags import generate_resume_tags_llm

RESUME_JSON = {
    "name": "Khasan",
    "surname": "Sadykov",
    "summary": "CS bachelor student with interests in backend and robotics.",
    "contacts": {
        "emails": ["k.sadykov@innopolis.university","xasanFN@mail.ru"],
        "phones": ["+7 (917) 866-01-08"],
        "urls": ["https://tomatocoder.tech/","https://github.com/khasan"]
    },
    "education": [
        {"degree": "BACHELOR IN COMPUTER SCIENCE", "institution": "Innopolis University"}
    ],
    "skills": {
        "hard": ["Gin","Arduino C","Python","Go","FastAPI","C++","MongoDB","PostgreSQL","SQLite","Git/Github","Linux"],
        "soft": ["Multitasking","Time Management","Creativity"]
    },
    "languages": [
        {"language":"English","level":"C2"},
        {"language":"Russian","level":"native"}
    ],
    "experience": [],
    "projects": [],
    "awards": [],
    "hobbies": ["Piano","Snowboarding"],
    "request": {"type":"resume","format":"json","model":""},
    "date_of_birth": "03/01/2007",
    "age": 18,
}

def main():
    api_key = os.getenv("SCIBOX_API_KEY", "")
    if not api_key:
        print(json.dumps({"error": "SCIBOX_API_KEY is empty"}, ensure_ascii=False))
        sys.exit(1)

    cfg = SciBoxConfig(
        api_key=api_key,
        base_url=os.getenv("SCIBOX_BASE_URL", "https://llm.t1v.scibox.tech/v1"),
        chat_model=os.getenv("SCIBOX_MODEL", "Qwen2.5-72B-Instruct-AWQ"),
    )

    payload = generate_resume_tags_llm(RESUME_JSON, k=20, cfg=cfg)

    print(json.dumps(payload.get("tags", []), ensure_ascii=False))

if __name__ == "__main__":
    main()