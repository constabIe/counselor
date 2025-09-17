#!/usr/bin/env python3
"""
Точка входа для запуска FastAPI приложения
"""

import uvicorn
from pathlib import Path
import sys
import os

# Добавляем текущую директорию в PYTHONPATH
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

if __name__ == "__main__":
    # Запуск сервера с настройками
    uvicorn.run(
        "app:app",  # модуль:переменная
        host="0.0.0.0",
        port=8000,
        reload=True,  # автоперезагрузка при изменениях
        log_level="info"
    )
