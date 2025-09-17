#!/usr/bin/env python3
"""
Точка входа для запуска FastAPI приложения через модуль
"""

import uvicorn
from pathlib import Path
import sys
import os

if __name__ == "__main__":
    # Запуск сервера с настройками
    uvicorn.run(
        "src.api.app:app",  # модуль:переменная
        host="0.0.0.0",
        port=8000,
        reload=True,  # автоперезагрузка при изменениях
        log_level="info"
    )
