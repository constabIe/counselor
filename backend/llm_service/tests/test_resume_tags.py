import os, sys, pathlib, json
THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[1]; SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.tags import generate_tags

TEXT = """Ivan Ivanov
Born 1990
Python developer, 5 years backend, speaks English C1, Russian native."""

def main():
    cfg = SciBoxConfig(
        api_key=os.getenv("SCIBOX_API_KEY", ""),
        base_url=os.getenv("SCIBOX_BASE_URL", "https://llm.t1v.scibox.tech/v1"),
        chat_model=os.getenv("SCIBOX_MODEL", "Qwen2.5-72B-Instruct-AWQ"),
    )
    res = generate_tags(TEXT, k=15, cfg=cfg)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()