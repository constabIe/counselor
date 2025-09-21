# 📦 AIHR Resume Processing Package

Этот пакет помогает backend-разработчикам работать с резюме кандидатов:  
- 📄 Извлекать текст из PDF (сканы и текстовые файлы)  
- 🧾 Структурировать его в JSON по фиксированной схеме  
- 🏷 Генерировать теги (для HR или поиска)  
- 🔢 Векторизовать теги для семантического поиска  

---

## 🚀 Установка и подготовка

1. **Создать виртуальное окружение**
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

2. **Установить зависимости**
```bash
pip install -r requirements.txt
```

3. **Создать `.env` в корне проекта**
```env
SCIBOX_API_KEY=<API_KEY>              # ключ доступа к SciBox
SCIBOX_BASE_URL=https://llm.t1v.scibox.tech/v1
SCIBOX_MODEL=Qwen2.5-72B-Instruct-AWQ # модель чата
SCIBOX_EMBED_MODEL=bge-m3             # модель эмбеддингов
```

4. **Запустить сервис Nougat (опционально, для сканов PDF)**
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

---

## 📄 1. Извлечение текста из PDF

```python
import pathlib
from aihr.ingest.extractors import extract_auto

pdf = pathlib.Path("cv.pdf").read_bytes()
extracted = extract_auto(
    pdf,
    nougat_base="http://localhost:8080",   # если нужен OCR
    nougat_token="supersecret-long-random",
    nougat_profile="accurate",
)

print("Engine:", extracted.engine)  # pymupdf / nougat
print("Text snippet:", extracted.text[:300])
```

---

## 🧾 2. Структуризация в JSON-резюме

```python
from aihr.llm.scibox_client import SciBoxConfig
from aihr.llm.tasks import task_structure_resume
import json

cfg = SciBoxConfig()
structured = task_structure_resume(extracted.text, cfg=cfg)

print(json.dumps(structured.payload, ensure_ascii=False, indent=2))
```

### 📋 Схема JSON-резюме

```json
{
  "name": "string",
  "surname": "string",
  "gender": "Male|Female|''",
  "age": "int|null",
  "date_of_birth": "string",
  "summary": "string",
  "contacts": {
    "emails": ["string"],
    "phones": ["string"],
    "urls": ["string"]
  },
  "education": [],
  "experience": [],
  "skills": {"hard": [], "soft": []},
  "languages": [],
  "projects": [],
  "awards": [],
  "hobbies": [],
  "request": {"type": "resume", "format": "json", "model": "string"}
}
```

---

## 🏷 3. Генерация тегов

### a) Теги из резюме

```python
from aihr.struct.tags import generate_tags

tags = generate_tags(structured.payload, k=15, cfg=cfg, prefer_llm=True)
print(tags)
```

Пример результата:

```json
{
  "tags": ["PYTHON", "FASTAPI", "POSTGRESQL", "BACKEND", "18-25"],
  "request": {"type": "tags", "format": "json", "model": "Qwen2.5-72B-Instruct-AWQ"}
}
```

### b) Теги по HR-запросу

```python
from aihr.struct.tags import generate_hr_query_tags_llm

prefs = {
  "query": "Нужен бэкенд, ownership, английский C1+",
  "filters": {
    "department": "Engineering",
    "experience_years_min": 2,
    "experience_years_max": 5,
    "skills": ["Python","FastAPI","PostgreSQL","Docker"],
    "level": "Middle",
    "languages": ["English C1"],
    "education_level": "Bachelor+",
    "age_min": 26,
    "age_max": 35
  }
}

tags = generate_hr_query_tags_llm(prefs, k=20, cfg=cfg)
print(tags)
```

---

## 🔢 4. Векторизация тегов

```python
from aihr.struct.embeddings import embed_tags

tags = ["PYTHON", "FASTAPI", "POSTGRESQL", "18-25"]
vecs = embed_tags(tags, cfg=cfg)

print("Vectors:", len(vecs))
print(vecs[0][:8])  # первые 8 чисел первого вектора
```

---

## 🔗 5. Полный пайплайн "PDF → JSON резюме → Теги → Вектора"

```python
import pathlib, json
from aihr.ingest.extractors import extract_auto
from aihr.llm.tasks import task_structure_resume
from aihr.llm.scibox_client import SciBoxConfig
from aihr.struct.tags import generate_tags
from aihr.struct.embeddings import embed_tags

cfg = SciBoxConfig()
pdf = pathlib.Path("cv.pdf").read_bytes()

extracted = extract_auto(pdf)
structured = task_structure_resume(extracted.text, cfg=cfg)
tags = generate_tags(structured.payload, k=15, cfg=cfg, prefer_llm=True)
vecs = embed_tags(tags["tags"], cfg=cfg)

result = {"resume": structured.payload, "tags": tags, "vectors": vecs}
print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

## 🛠 Отладка и тестирование

```bash
pytest -v
python llm_service/tests/test_tags_smoke.py
```

---

## 📌 Итог

Этот пакет позволяет:  
✅ Автоматически обрабатывать резюме из PDF  
✅ Приводить данные в **единый JSON-формат**  
✅ Генерировать HR-теги и возрастные диапазоны  
✅ Строить эмбеддинги для поиска и подбора  

Используется единый конфиг `SciBoxConfig`, который берёт параметры из `.env`.
