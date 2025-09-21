# LLM Service — Инструкция (RU)

Этот документ описывает, как пользоваться модулем `llm_service` для обработки резюме: извлечение текста, структуризация, генерация тегов и векторизация.

---

## 🚀 Установка

```bash
# Клонируем репозиторий
git clone https://github.com/constabIe/hrcounselor.git
cd hrcounselor/backend

# Создаём и активируем виртуальное окружение
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate    # Windows PowerShell

# Устанавливаем зависимости
pip install -r requirements.txt
```

---

## ⚙️ Настройка окружения

Создайте файл `.env` в папке `backend/llm_service`:

```env
SCIBOX_API_KEY=ваш_api_ключ
SCIBOX_BASE_URL=https://llm.t1v.scibox.tech/v1
SCIBOX_MODEL=Qwen2.5-72B-Instruct-AWQ
SCIBOX_EMBED_MODEL=bge-m3
```

---

## 📄 Извлечение текста из PDF

```python
from pathlib import Path
from aihr.ingest.extractors import extract_auto

pdf_bytes = Path("cv.pdf").read_bytes()
result = extract_auto(pdf_bytes)
print(result.text)  # исходный текст
```

Результат сохраняется в JSON с полями:
```json
{
  "engine": "pymupdf",
  "meta": {"pages": 2},
  "text": "...."
}
```

---

## 🏗 Структуризация резюме

```python
from aihr.struct.pipeline import structure_from_extract_json

structured = structure_from_extract_json(result)
print(structured)
```

Пример JSON:
```json
{
  "name": "Ivan",
  "surname": "Petrov",
  "gender": "Male",
  "age": 28,
  "date_of_birth": "1997-01-05",
  "summary": "Опытный backend разработчик с фокусом на Python и Go.",
  "contacts": {"emails": ["ivan@mail.com"], "phones": ["+79998887766"], "urls": []},
  "education": [...],
  "experience": [...],
  "skills": {"hard": ["Python","FastAPI"], "soft": ["Time Management"]},
  "languages": [...],
  "projects": [],
  "awards": [],
  "hobbies": [],
  "request": {"type":"resume","format":"json","model":"Qwen2.5-72B-Instruct-AWQ"}
}
```

---

## 🏷 Генерация тегов

### Из резюме
```python
from aihr.struct.tags import generate_tags

tags = generate_tags(structured)
print(tags)
```

### Из HR-запроса
```python
from aihr.struct.tags import generate_hr_query_tags_llm

prefs = {
  "query": "Нужен backend разработчик с Python и английским C1+",
  "filters": {
    "department": "Engineering",
    "experience_years_min": 2,
    "experience_years_max": 5,
    "skills": ["Python","FastAPI","PostgreSQL"],
    "level": "Middle",
    "languages": ["English C1","Russian native"],
    "education_level": "Bachelor+",
    "age_min": 26,
    "age_max": 35
  }
}

tags = generate_hr_query_tags_llm(prefs)
print(tags)
```

Все теги возвращаются в ВЕРХНЕМ РЕГИСТРЕ и включают возрастную категорию.

---

## 🔢 Векторизация тегов

```python
from aihr.struct.embed import embed_tags
tags = ["PYTHON","FASTAPI","26-30"]

vectors = embed_tags({"tags": tags})
print(len(vectors), "vectors")
```

---

## 🧪 Тесты

Запуск всех тестов:
```bash
pytest backend/llm_service/tests -v
```

Пример теста извлечения:
```bash
python backend/llm_service/tests/test_extract_smoke.py
```

Пример теста тегов:
```bash
python backend/llm_service/tests/test_tags_smoke.py
```

Все тесты выводят результат в консоль в JSON.

---

## 🌐 Работа с GitHub

Создать ветку:
```bash
git checkout -b feature/llm-service
```

Закоммитить:
```bash
git add .
git commit -m "LLM сервис: структуризация резюме, теги, эмбеддинги"
git push origin feature/llm-service
```

---

## 📌 Итог

Модуль поддерживает:
- Извлечение текста из PDF
- Структуризацию резюме
- Генерацию тегов (резюме и HR-запрос)
- Векторизацию тегов
- Удобные тесты
- Настройки через `.env`

