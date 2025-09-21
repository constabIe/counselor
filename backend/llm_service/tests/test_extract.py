import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aihr.ingest.extractors import extract_auto

PDF = pathlib.Path(r"C:\Users\Iudin\Downloads\cv.pdf")

def main() -> None:
    pdf_bytes = PDF.read_bytes()
    res = extract_auto(
        pdf_bytes,
        nougat_base="http://localhost:8080",
        nougat_token="supersecret-long-random",
        nougat_profile="accurate",
        min_chars_ok=400,
    )

    print(json.dumps(res, ensure_ascii=False, indent=2))

    out_dir = PDF.parent / "extract_out"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{PDF.stem}.json"
    out_path.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nSaved JSON to:", out_path)

if __name__ == "__main__":
    main()