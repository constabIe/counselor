from __future__ import annotations
import os, sys, json, pathlib
THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[1]; SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.embeddings import embed_tags

cfg = SciBoxConfig()
data = {"tags": ["Python", "FastAPI", "PostgreSQL", "26-30"]}
res = embed_tags(data, cfg=cfg)

print("model:", res["request"]["model"])
print("count:", len(res["vectors"]))
print(res["vectors"][0]["tag"], "→", res["vectors"][0]["vector"][:5], "...")