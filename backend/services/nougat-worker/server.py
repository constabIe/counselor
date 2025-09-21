import os
import tempfile
import pathlib
import datetime
import subprocess
import time
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import JSONResponse, PlainTextResponse

# === Конфиг ===
API_TOKEN = os.getenv("API_TOKEN", "changeme")
MAX_FILE_MB = int(os.getenv("MAX_FILE_MB", "25"))
NOUGAT_BIN = os.getenv("NOUGAT_BIN", "nougat")

# профили: fast = быстрее, accurate = точнее
PROFILES = {"fast": [], "accurate": ["--no-skipping", "--full-precision"]}

log = logging.getLogger("nougat-worker")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# === App ===
app = FastAPI(title="Nougat API", version="1.0")


# Авторизация по токену
def _auth(h: str | None):
    if not h or not h.startswith("Bearer ") or h.split(" ", 1)[1] != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


# Запуск Nougat
def _run_nougat(pdf_path: pathlib.Path, profile: str) -> str:
    with tempfile.TemporaryDirectory() as outdir:
        cmd = [NOUGAT_BIN, "--out", outdir, "--markdown"]
        cmd += PROFILES.get(profile, [])
        cmd.append(str(pdf_path))

        t0 = time.perf_counter()
        res = subprocess.run(cmd, capture_output=True, text=True)
        dur_ms = (time.perf_counter() - t0) * 1000.0
        log.info("nougat cmd=%s status=%s dur_ms=%.1f", " ".join(cmd), res.returncode, dur_ms)

        if res.returncode != 0:
            raise RuntimeError(res.stderr.strip() or "nougat failed")

        # ищем первый markdown файл в папке
        out = None
        for ext in (".md", ".mmd", ".markdown"):
            cand = list(pathlib.Path(outdir).glob(f"*{ext}"))
            if cand:
                out = cand[0]
                break
        if not out:
            raise RuntimeError("nougat produced no markdown files")

        return out.read_text(encoding="utf-8", errors="ignore")


# === Эндпоинты ===
@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "OK"


@app.get("/readyz", response_class=PlainTextResponse)
def readyz():
    return "READY"


@app.post("/infer_sync")
async def infer_sync(
    file: UploadFile = File(...),
    profile: str = "fast",
    authorization: str | None = Header(default=None),
):
    _auth(authorization)

    if profile not in PROFILES:
        raise HTTPException(status_code=400, detail="Unknown profile")

    allowed_types = {"application/pdf", "application/octet-stream", "binary/octet-stream"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=415, detail=f"Bad content type: {file.content_type}")

    tmp = None
    try:
        pdf = await file.read()
        if len(pdf) > MAX_FILE_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"File too large: {MAX_FILE_MB}MB maximum")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(pdf)
            tmp = pathlib.Path(f.name)

        md = _run_nougat(tmp, profile)
        pages = md.count("\f") + (1 if md else 0)

        resp = {
            "meta": {
                "pages": pages,
                "ts": datetime.datetime.utcnow().isoformat(),
                "profile": profile,
                "source": "nougat",
                "ocr_used": True,
            },
            "raw_markdown": md,
        }
        return JSONResponse(content=resp)

    except HTTPException:
        raise
    except Exception as e:
        log.exception("processing failed")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
    finally:
        if tmp and tmp.exists():
            tmp.unlink()