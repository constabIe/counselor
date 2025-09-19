import os
import uuid
from pathlib import Path
from typing import BinaryIO

from fastapi import UploadFile, HTTPException


# Директория для хранения загруженных файлов
UPLOAD_DIR = Path("uploads")
CV_DIR = UPLOAD_DIR / "cvs"

# Создаем директории если их нет
CV_DIR.mkdir(parents=True, exist_ok=True)

# Разрешенные типы файлов
ALLOWED_CV_TYPES = {
    "application/pdf",
    "application/x-pdf",
}

# Максимальный размер файла (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_cv_file(file: UploadFile) -> None:
    """Валидирует загружаемый CV файл"""
    
    # Проверяем тип файла
    if file.content_type not in ALLOWED_CV_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый тип файла. Разрешены только PDF файлы."
        )
    
    # Проверяем расширение файла
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Файл должен иметь расширение .pdf"
        )


def generate_unique_filename(original_filename: str) -> str:
    """Генерирует уникальное имя файла"""
    file_extension = Path(original_filename).suffix
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{file_extension}"


async def save_cv_file(file: UploadFile) -> tuple[str, str, int]:
    """
    Сохраняет CV файл на диск
    
    Returns:
        tuple: (filename, file_path, file_size)
    """
    validate_cv_file(file)
    
    # Генерируем уникальное имя файла
    filename = generate_unique_filename(file.filename or "cv.pdf")
    file_path = CV_DIR / filename
    
    # Читаем содержимое файла
    content = await file.read()
    file_size = len(content)
    
    # Проверяем размер файла
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE // (1024*1024)} MB"
        )
    
    # Сохраняем файл
    with open(file_path, "wb") as f:
        f.write(content)
    
    return filename, str(file_path), file_size


def delete_cv_file(file_path: str) -> bool:
    """Удаляет файл CV с диска"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def get_file_size_mb(file_size: int) -> float:
    """Конвертирует размер файла в мегабайты"""
    return round(file_size / (1024 * 1024), 2)
