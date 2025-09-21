from __future__ import annotations
import io
import typing as T

import requests
import fitz
from pdfminer.high_level import extract_text as pdfminer_extract_text


def extract_auto(
    pdf_bytes: bytes,
    nougat_base: str | None = None,
    nougat_token: str | None = None,
    nougat_profile: str = "accurate",
    min_chars_ok: int = 400,
) -> dict:
    meta: dict[str, T.Any] = {}

    # --- 1) PyMuPDF ---
    text1 = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        meta["pages"] = len(doc)
        text1 = "\n".join(page.get_text("text") for page in doc)
    except Exception as e:
        meta["error_pymupdf"] = f"{type(e).__name__}: {e}"

    if len(text1.strip()) >= min_chars_ok:
        return {"engine": "pymupdf", "meta": meta, "text": text1.strip()}

    # --- 2) pdfminer.six ---
    text2 = ""
    try:
        text2 = pdfminer_extract_text(io.BytesIO(pdf_bytes)) or ""
    except Exception as e:
        meta["error_pdfminer"] = f"{type(e).__name__}: {e}"

    if len(text2.strip()) >= min_chars_ok or not nougat_base:
        return {"engine": "pdfminer", "meta": meta, "text": text2.strip()}

    # --- 3) Nougat ---
    try:
        headers = {}
        if nougat_token:
            headers["Authorization"] = f"Bearer {nougat_token}"
        files = {"file": ("doc.pdf", pdf_bytes, "application/pdf")}
        resp = requests.post(
            f"{nougat_base}/infer_sync",
            headers=headers,
            files=files,
            params={"profile": nougat_profile},
            timeout=600,
        )
        resp.raise_for_status()
        data = resp.json()
        text3 = (data.get("raw_markdown") or "").strip()
        meta["nougat_meta"] = data.get("meta", {})
        return {"engine": "nougat", "meta": meta, "text": text3}
    except Exception as e:
        meta["error_nougat"] = f"{type(e).__name__}: {e}"

    best = text1 if len(text1) >= len(text2) else text2
    return {"engine": "fallback", "meta": meta, "text": best.strip()}