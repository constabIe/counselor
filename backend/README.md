# HR Counselor Backend

Backend API для HR помощника с поддержкой искусственного интеллекта.

## Быстрый старт

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Настройте конфигурацию:**
   Отредактируйте файл `settings.yaml` под ваши нужды.

3. **Инициализируйте базу данных:**
   ```bash
   python init_db.py
   ```

4. **Запустите сервер:**
   ```bash
   uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Откройте в браузере:**
   - Главная страница: http://localhost:8000
   - API документация: http://localhost:8000/docs

## Структура проекта

```
backend/
├── src/
│   ├── api/                 # FastAPI приложение
│   ├── config.py           # Конфигурация
│   ├── config_schema.py    # Схема конфигурации
│   ├── modules/            # Модули бизнес-логики
│   │   ├── users/          # Пользователи и аутентификация
│   │   └── landing/        # Главная страница
│   ├── storages/           # Работа с данными
│   │   └── sql/            # SQL модели и зависимости
│   └── utils/              # Утилиты
│       └── security.py     # JWT и безопасность
├── settings.yaml           # Настройки приложения
├── requirements.txt        # Python зависимости
└── init_db.py             # Инициализация БД
```

## API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Вход в систему
- `GET /auth/me` - Информация о текущем пользователе

### Системные
- `GET /` - Главная страница (HTML)
- `GET /health` - Проверка состояния API
- `GET /docs` - Swagger документация

## Фичи

✅ **Реализовано:**
- Красивая landing страница с описанием сервиса
- Регистрация и аутентификация пользователей с JWT токенами
- SQLite база данных (легко переключить на PostgreSQL)
- CORS поддержка
- Автоматическая документация API
- Валидация данных с Pydantic
- Хеширование паролей с bcrypt

🚧 **В планах:**
- Интеграция с ИИ для анализа резюме
- Система ролей (HR, Admin, User)
- API для работы с вакансиями
- Файловое хранилище для резюме
- Уведомления и email интеграция

## Разработка

Для разработки рекомендуется использовать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

Для тестирования:
```bash
pytest
```

2. Запустите сервер:
```bash
python __main__.py
```

Или:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Главная страница с приветствием
- `GET /health` - Проверка здоровья сервиса  
- `GET /api/hello` - Приветствие на API роуте

## Доступ

После запуска API будет доступно по адресу:
- http://localhost:8000
- Документация: http://localhost:8000/docs
