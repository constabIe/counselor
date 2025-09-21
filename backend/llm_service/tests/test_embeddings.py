import os, sys, pathlib, json
THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[1]; SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.embeddings import embed_tags

DATA = {"tags": ["PYTHON", "FASTAPI", "POSTGRESQL", "BACKEND", "26-30"]}

def main():
    cfg = SciBoxConfig(
        api_key=os.getenv("SCIBOX_API_KEY", ""),
        base_url=os.getenv("SCIBOX_BASE_URL", "https://llm.t1v.scibox.tech/v1"),
        embed_model=os.getenv("SCIBOX_EMBED_MODEL", "bge-m3"),
    )
    res = embed_tags(DATA, cfg=cfg)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()