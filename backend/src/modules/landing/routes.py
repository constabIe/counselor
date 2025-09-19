from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["landing"],
)


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Landing страница",
    description="Главная страница HR помощника с информацией о сервисе"
)
async def landing_page() -> str:
    """Возвращает главную страницу"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HR Counselor - Ваш ИИ помощник в HR</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                padding: 60px 0;
                color: white;
            }
            
            .header h1 {
                font-size: 3rem;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
                max-width: 600px;
                margin: 0 auto;
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin: 50px 0;
            }
            
            .feature-card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 20px;
            }
            
            .feature-card h3 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.5rem;
            }
            
            .cta-section {
                text-align: center;
                padding: 50px 0;
                color: white;
            }
            
            .cta-button {
                display: inline-block;
                background: #ff6b6b;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 50px;
                font-size: 1.1rem;
                font-weight: bold;
                transition: background 0.3s ease;
                margin: 0 10px;
            }
            
            .cta-button:hover {
                background: #ff5252;
            }
            
            .api-info {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                margin: 30px 0;
                color: white;
            }
            
            .api-info h3 {
                margin-bottom: 15px;
            }
            
            .endpoint {
                background: rgba(255,255,255,0.1);
                padding: 10px 15px;
                border-radius: 8px;
                margin: 10px 0;
                font-family: 'Courier New', monospace;
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2rem;
                }
                
                .features {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 HR Counselor</h1>
                <p>Ваш умный помощник в сфере управления персоналом с поддержкой искусственного интеллекта</p>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <div class="feature-icon">📄</div>
                    <h3>Загрузка CV</h3>
                    <p>Простая загрузка резюме в формате PDF с автоматическим сохранением и организацией файлов</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3>Умный подбор</h3>
                    <p>ИИ поможет найти идеальных кандидатов на основе требований к позиции и анализа резюме</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Аналитика</h3>
                    <p>Глубокая аналитика HR-процессов с использованием машинного обучения для оптимизации найма</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🤝</div>
                    <h3>Автоматизация</h3>
                    <p>Автоматизируйте рутинные задачи: скрининг резюме, планирование интервью, отправка уведомлений</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">💡</div>
                    <h3>Рекомендации</h3>
                    <p>Получайте персонализированные рекомендации по улучшению HR-процессов на основе ИИ</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Безопасность</h3>
                    <p>Надежная защита данных с современными методами шифрования и контроля доступа</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🚀</div>
                    <h3>Быстрый старт</h3>
                    <p>Простая интеграция с существующими системами и быстрое развертывание за один день</p>
                </div>
            </div>
            
            <div class="api-info">
                <h3>🔌 API Endpoints</h3>
                <p>Наш сервис предоставляет RESTful API для интеграции с вашими системами:</p>
                
                <div class="endpoint">
                    <strong>POST /auth/register</strong> - Регистрация нового пользователя
                </div>
                <div class="endpoint">
                    <strong>POST /auth/login</strong> - Вход в систему
                </div>
                <div class="endpoint">
                    <strong>GET /auth/me</strong> - Получение информации о текущем пользователе
                </div>
                <div class="endpoint">
                    <strong>POST /cv/upload</strong> - Загрузка CV в формате PDF
                </div>
                <div class="endpoint">
                    <strong>GET /cv/my</strong> - Список загруженных CV
                </div>
                <div class="endpoint">
                    <strong>GET /docs</strong> - Интерактивная документация API
                </div>
            </div>
            
            <div class="cta-section">
                <h2>Готовы начать?</h2>
                <p style="margin: 20px 0;">Присоединяйтесь к революции в HR-технологиях уже сегодня!</p>
                <a href="/docs" class="cta-button">📚 API Документация</a>
                <a href="/auth/register" class="cta-button">🚀 Начать сейчас</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content
