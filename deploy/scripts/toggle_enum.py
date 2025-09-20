#!/usr/bin/env python3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FILE = BASE_DIR.parent / "backend" / "alembic" / "versions" / "2413bdff9a4a_init.py"

if len(sys.argv) != 2 or sys.argv[1].lower() not in {"true", "false"}:
    print("Usage: toggle_enum.py true|false")
    sys.exit(1)

value = sys.argv[1].lower().capitalize()  # True / False

text = FILE.read_text(encoding="utf-8")
text = text.replace("create_type=True", f"create_type={value}")
text = text.replace("create_type=False", f"create_type={value}")
FILE.write_text(text, encoding="utf-8")

print(f"Change to create_type={value}")