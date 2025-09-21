import os, sys, pathlib, json
THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[1]; SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.pipeline import structure_from_extract_json

EXTRACT = {
    "engine": "pymupdf",
    "meta": {"pages": 2},
    "text": "Ivan Ivanov\nDate of birth: 01/01/1990\nEmail: ivan@example.com\nPython developer..."
}

def main():
    cfg = SciBoxConfig(
        api_key=os.getenv("SCIBOX_API_KEY", ""),
        base_url=os.getenv("SCIBOX_BASE_URL", "https://llm.t1v.scibox.tech/v1"),
        chat_model=os.getenv("SCIBOX_MODEL", "Qwen2.5-72B-Instruct-AWQ"),
    )
    res = structure_from_extract_json(EXTRACT, cfg=cfg)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()