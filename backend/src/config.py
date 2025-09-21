import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

from src.config_schema import Settings

BASE_DIR = Path(__file__).resolve().parent.parent

settings_path = os.getenv("SETTINGS_PATH", BASE_DIR / ".env")

settings_path = os.getenv("SETTINGS_PATH", ".env")
settings: Settings = Settings.from_env(Path(settings_path)) if Path(settings_path).exists() else Settings() # type: ignore


def get_settings() -> Settings:
    """Получить настройки приложения"""
    return settings
