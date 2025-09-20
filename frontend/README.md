# 🎨 HR Counselor Frontend

> Современный веб-интерфейс для системы анализа резюме и автоматизации HR-процессов с поддержкой ИИ.

## ✨ Возможности

- **Аутентификация** - безопасный вход и управление пользователями
- **Интерактивная работа с резюме** - загрузка, просмотр и анализ CV
- **Управление вакансиями** - создание, редактирование и публикация job positions
- **Образовательная платформа** - просмотр курсов и отслеживание прогресса
- **Система достижений** - badges и визуализация опыта
- **Аналитика** - дашборды и отчеты по эффективности
- **Адаптивный дизайн** - работа на всех устройствах

## 🔧 Технологический стек

![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat&logo=javascript&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)

## 🚀 Быстрый старт

### Требования

- **Node.js** 18+ 
- **npm** 9+ или **yarn** 3+

### Установка и запуск

1. **Клонирование и навигация**:
   ```bash
   cd frontend
   ```

2. **Установка зависимостей**:
   ```bash
   npm install
   # или
   yarn install
   ```

3. **Настройка переменных окружения**:
   ```bash
   cp .env.example .env.local
   # Отредактируйте .env.local
   ```

4. **Запуск dev-сервера**:
   ```bash
   npm run dev
   # или
   yarn dev
   ```

5. **Открытие в браузере**:
   ```
   http://localhost:5173
   ```

## 📁 Структура проекта

```
frontend/
├── public/                     # Статические файлы
│   ├── favicon.ico
│   └── assets/
├── src/                        # Исходный код
│   ├── components/             # React компоненты
│   │   ├── common/             # Общие компоненты
│   │   ├── auth/               # Компоненты аутентификации
│   │   ├── cv/                 # Управление резюме
│   │   ├── jobs/               # Управление вакансиями
│   │   ├── courses/            # Образовательная платформа
│   │   └── badges/             # Система достижений
│   ├── pages/                  # Страницы приложения
│   ├── hooks/                  # Кастомные React хуки
│   ├── services/               # API сервисы
│   ├── utils/                  # Утилиты
│   ├── styles/                 # Стили
│   │   ├── globals.css
│   │   └── components/
│   ├── api.js                  # API конфигурация
│   ├── App.jsx                 # Главный компонент
│   ├── main.jsx                # Точка входа
│   └── index.css               # Глобальные стили
├── package.json                # Зависимости и скрипты
└── vite.config.js              # Конфигурация Vite
```

## 🛠️ Доступные скрипты

```bash
# Запуск dev-сервера
npm run dev

# Сборка для продакшна
npm run build

# Предпросмотр production сборки
npm run preview

# Линтинг кода
npm run lint

# Форматирование кода
npm run format

# Запуск тестов
npm run test
```

## 🎨 Стилизация

Проект использует:
- **CSS Modules** для изоляции стилей
- **CSS Custom Properties** для темизации
- **Flexbox/Grid** для адаптивных макетов
- **Mobile-first** подход

### Цветовая схема

```css
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --warning-color: #ffc107;
  --danger-color: #dc3545;
  --background-color: #f8f9fa;
  --text-color: #212529;
}
```

## 🔌 API Интеграция

Конфигурация API в `src/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Автоматическое добавление JWT токенов
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```