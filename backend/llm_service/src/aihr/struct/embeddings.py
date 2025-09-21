from __future__ import annotations
from typing import Any, Dict, Iterable, List

from aihr.llm.scibox_client import SciBoxConfig, SciBoxClient

def _upper_unique(seq: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for s in seq:
        if not isinstance(s, str):
            continue
        u = s.strip().upper()
        if not u:
            continue
        k = u.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(u)
    return out

def _extract_tags(obj: Any) -> List[str]:
    if isinstance(obj, dict):
        tags = obj.get("tags")
        if isinstance(tags, list):
            return [t for t in tags if isinstance(t, str)]
        raise TypeError("JSON dict must contain 'tags': List[str]")
    if isinstance(obj, list):
        return [t for t in obj if isinstance(t, str)]
    raise TypeError("Input must be dict with 'tags' or list[str]")

def embed_tags(
    tags_json_or_list: Any,
    *,
    cfg: SciBoxConfig | None = None,
    normalize_upper: bool = True,
    batch: int = 128,
    model: str | None = None,
) -> Dict[str, Any]:
    cfg = cfg or SciBoxConfig()
    tags = _extract_tags(tags_json_or_list)
    tags = _upper_unique(tags) if normalize_upper else [t.strip() for t in tags if t and t.strip()]

    client = SciBoxClient(cfg)
    model_name = model or cfg.embed_model or "bge-m3"

    vecs: List[List[float]] = []
    for i in range(0, len(tags), batch):
        part = tags[i:i+batch]
        if not part:
            continue
        vecs.extend(client.embed(part, model=model_name))

    items = []
    n = min(len(tags), len(vecs))
    for i in range(n):
        items.append({"tag": tags[i], "vector": vecs[i]})

    return {
        "vectors": items,
        "request": {"type": "tag_embeddings", "format": "json", "model": model_name},
    }