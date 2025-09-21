import os, sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.pipeline import structure_from_extract_json

EXTRACT = {
  "engine": "pymupdf",
  "meta": {"pages": 2},
  "text": """Khasan Sadykov
Date of birth: 03/01/2007
Place of birth: Kazan
Nationality: Russian
Phone number: (+7) 9178660108 (Home)
Email address: k.sadykov@innopolis.university
Email address: xasanFN@mail.ru
Website: https://tomatocoder.tech/
Address: Kazan, Russia (Home)

01/09/2024 – CURRENT Innopolis, Russia
BACHELOR IN COMPUTER SCIENCE Innopolis University
Mother tongue(s): RUSSIAN
Other language(s):

UNDERSTANDING SPEAKING WRITING
Listening Reading Spoken production Spoken interaction
ENGLISH C2 C2 C1 C1 B2
GERMAN  B1 B1 B1 B1 B1
KOREAN  A1 A1 A1 A1 A1

Programming Languages/Libs/Frameworks
Gin, Arduino C, Python, Go, FastAPI, C++
Databases
MongoDB, PostgreSQL, SQLite
Other tools
Git/Github, Linux (Terminal Commands, Bash/Shell)

03/07/2022 3rd place at the National stage of All-Russian Robotics Olympiad – Federation of Sport and Educational Robotics
15/05/2022 1st place at the Regional Stage of All-Russian Olympiad – Federation of Sport and Educational Robotics
21/05/2021 2nd place at the Regional Stage of All-Russian Olympiad – Federation of Sport and Educational Robotics
03/11/2019 Letter of Appreciation (FINA Swimming World Cup) – FINA

Piano; Photo Art; Snowboarding; Swimming
Multitasking; Critical Thinking; Time Management; Creativity; Logical Reasoning
"""
}

def main():
    cfg = SciBoxConfig(
        api_key=os.getenv("SCIBOX_API_KEY",""),
        base_url=os.getenv("SCIBOX_BASE_URL","https://llm.t1v.scibox.tech/v1"),
        chat_model=os.getenv("SCIBOX_MODEL","Qwen2.5-72B-Instruct-AWQ"),
    )
    structured = structure_from_extract_json(EXTRACT, cfg=cfg)

    out_dir = pathlib.Path.cwd() / "structured_out"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "cv.structured.json"
    out.write_text(json.dumps(structured, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Saved:", out)
    print("Top-level keys:", list(structured.keys()))
    print("request:", structured.get("request"))

if __name__ == "__main__":
    main()