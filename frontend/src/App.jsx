import React, { useState } from 'react'
import './App.css'

const makeEmployeeData = () => ({
  fullName: 'Файзуллина Дилия',
  rating: 4.5,
  xp: 1200,
  history: [
    { id: 1, title: 'Место работы/учёбы', value: 'Университет Иннополис' },
    { id: 2, title: 'Место работы/учёбы', value: 'Университет Иннополис' },
    { id: 3, title: 'Стаж/опыт', value: '2 года' },
    { id: 4, title: 'Место работы/учёбы', value: 'Университет Иннополис' },
    { id: 5, title: 'Место работы/учёбы', value: 'Университет Иннополис' },
  ],
  badges: ['Уникальность', 'CRE', 'Важность', 'Командность', 'Крутость'],
  cvFileName: '',
  uploadedAt: '',
})

const taskSuggestions = [
  {
    id: 'skills',
    title: 'Обновить раздел «Навыки»',
    details: 'Оставьте только релевантные навыки и сгруппируйте их по категориям.',
  },
  {
    id: 'results',
    title: 'Добавить измеримые результаты',
    details: 'Укажите цифры: процент роста, размер команды, бюджеты, KPI.',
  },
  {
    id: 'summary',
    title: 'Переписать резюме в шапке',
    details: 'Сформулируйте короткий summary на 2-3 предложения с уникальным преимуществом.',
  },
  {
    id: 'formatting',
    title: 'Привести форматирование к единому стилю',
    details: 'Проверьте интервалы, выравнивание и используйте один шрифт.',
  },
  {
    id: 'proofread',
    title: 'Проверить текст на ошибки',
    details: 'Прочитайте вслух или воспользуйтесь сервисом проверки орфографии.',
  },
]

const cvRecommendations = [
  'Добавьте ссылку на портфолио и актуальные профили в соцсетях.',
  'Сгруппируйте опыт по проектам: название, роль, результат.',
  'Уточните уровень владения инструментами и технологиями.',
  'Используйте PDF формат и название файла в формате Фамилия_Роль.pdf.',
]

const hrFolders = [
  {
    id: 'marketing',
    name: 'Маркетинг',
    count: 18,
    updated: '5 минут назад',
    accent: '#5eead4',
    files: [
      { id: 'marketing-1', name: 'Иванова Мария - Growth Manager.pdf', uploaded: '15 минут назад' },
      { id: 'marketing-2', name: 'Смирнов Павел - Brand Lead.pdf', uploaded: 'вчера' },
      { id: 'marketing-3', name: 'Петрова Анна - Performance Marketer.pdf', uploaded: '2 дня назад' },
    ],
  },
  {
    id: 'frontend',
    name: 'Frontend Junior',
    count: 24,
    updated: '12 минут назад',
    accent: '#a855f7',
    files: [
      { id: 'frontend-1', name: 'Ким Алексей - React Developer.pdf', uploaded: '10 минут назад' },
      { id: 'frontend-2', name: 'Гаврилов Илья - Vue Developer.pdf', uploaded: '30 минут назад' },
      { id: 'frontend-3', name: 'Романова Ольга - Frontend Intern.pdf', uploaded: 'сегодня' },
    ],
  },
  {
    id: 'data',
    name: 'Data Science',
    count: 13,
    updated: 'час назад',
    accent: '#f97316',
    files: [
      { id: 'data-1', name: 'Алиев Тимур - Data Scientist.pdf', uploaded: '40 минут назад' },
      { id: 'data-2', name: 'Соколова Дарья - ML Engineer.pdf', uploaded: 'сегодня' },
      { id: 'data-3', name: 'Миронов Константин - Analyst.pdf', uploaded: '2 часа назад' },
    ],
  },
  {
    id: 'design',
    name: 'Дизайн',
    count: 9,
    updated: 'вчера',
    accent: '#38bdf8',
    files: [
      { id: 'design-1', name: 'Кузнецова Мария - Product Designer.pdf', uploaded: '3 часа назад' },
      { id: 'design-2', name: 'Сафина Дина - UI Designer.pdf', uploaded: 'вчера' },
      { id: 'design-3', name: 'Новиков Андрей - UX Researcher.pdf', uploaded: '2 дня назад' },
    ],
  },
  {
    id: 'product',
    name: 'Product / PM',
    count: 11,
    updated: '2 часа назад',
    accent: '#bef264',
    files: [
      { id: 'product-1', name: 'Леонов Артём - Product Manager.pdf', uploaded: '25 минут назад' },
      { id: 'product-2', name: 'Алексеева Кира - Product Analyst.pdf', uploaded: 'час назад' },
      { id: 'product-3', name: 'Яковлев Степан - Associate PM.pdf', uploaded: 'вчера' },
    ],
  },
  {
    id: 'interns',
    name: 'Стажёры',
    count: 32,
    updated: '10 минут назад',
    accent: '#facc15',
    files: [
      { id: 'interns-1', name: 'Захарова Вера - HR Intern.pdf', uploaded: '5 минут назад' },
      { id: 'interns-2', name: 'Сергеев Никита - Marketing Intern.pdf', uploaded: '25 минут назад' },
      { id: 'interns-3', name: 'Федорова Лена - Product Intern.pdf', uploaded: 'сегодня' },
    ],
  },
]

export default function App() {
  const [view, setView] = useState('landing')
  const [onboardingSlide, setOnboardingSlide] = useState(0)
  const [employeeData, setEmployeeData] = useState(() => makeEmployeeData())
  const [showTaskModal, setShowTaskModal] = useState(false)

  const goLanding = () => {
    setView('landing')
    setOnboardingSlide(0)
    setShowTaskModal(false)
  }

  const handleEmployeeRegistration = () => {
    setEmployeeData(makeEmployeeData())
    setOnboardingSlide(0)
    setShowTaskModal(false)
    setView('employeeOnboarding')
  }

  const handleCvUploaded = (fileName) => {
    if (!fileName) {
      return
    }

    setEmployeeData((prev) => ({
      ...prev,
      cvFileName: fileName,
      uploadedAt: new Date().toLocaleString('ru-RU', {
        day: '2-digit',
        month: 'long',
        hour: '2-digit',
        minute: '2-digit',
      }),
    }))
    setShowTaskModal(false)
    setView('employeeDashboard')
  }

  const handleLogin = (role) => {
    setShowTaskModal(false)
    if (role === 'employee') {
      setView('employeeDashboard')
      return
    }

    setView('hrDashboard')
  }

  return (
    <div className={`app app--${view}`}>
      {view === 'landing' && <LandingPage onStart={() => setView('auth')} />}

      {view === 'auth' && (
        <AuthPage
          onBack={goLanding}
          onRegisterEmployee={handleEmployeeRegistration}
          onRegisterHr={() => setView('hrDashboard')}
          onLogin={handleLogin}
        />
      )}

      {view === 'employeeOnboarding' && (
        <EmployeeOnboarding
          currentSlide={onboardingSlide}
          onChangeSlide={setOnboardingSlide}
          onComplete={handleCvUploaded}
          onClose={goLanding}
          existingFileName={employeeData.cvFileName}
        />
      )}

      {view === 'employeeDashboard' && (
        <EmployeeDashboard
          data={employeeData}
          onLogout={goLanding}
          onReupload={() => {
            setOnboardingSlide(2)
            setView('employeeOnboarding')
          }}
          onOpenTasks={() => setShowTaskModal(true)}
        />
      )}

      {view === 'hrDashboard' && <HrDashboard onLogout={goLanding} />}

      {showTaskModal && <TaskModal onClose={() => setShowTaskModal(false)} />}
    </div>
  )
}

function LandingPage({ onStart }) {
  return (
    <div className="landing">
      <header className="landing__header">
        <span className="brand brand--accent">HR-АССИСТЕНТ</span>
        <button
          className="icon-button"
          type="button"
          onClick={onStart}
          aria-label="Войти в личный кабинет"
        >
          <UserIcon className="icon" />
        </button>
      </header>

      <div className="landing__body">
        <div className="landing__copy">
          <p className="landing__eyebrow">HR-Ассистент</p>
          <h1 className="landing__title">
            <span className="landing__title-highlight">AI-powered</span>
            <span>HR assistant</span>
          </h1>
          <p className="landing__subtitle">
            Оптимизируйте процесс найма с нашим интеллектуальным HR-ассистентом.
          </p>
          <button className="btn btn-green" type="button" onClick={onStart}>
            Начать
          </button>
        </div>

        <div className="landing__art">
          <div className="landing__illustration">
            <div className="landing__glow" />
            <div className="landing__person">
              <div className="landing__person-face" />
              <div className="landing__person-body" />
            </div>
            <span className="landing__label">AI</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function AuthPage({ onBack, onRegisterEmployee, onRegisterHr, onLogin }) {
  const [loginRole, setLoginRole] = React.useState('employee')

  return (
    <div className="auth">
      <header className="dashboard-header">
        <span className="brand">HR-АССИСТЕНТ</span>
        <button className="btn btn-ghost btn-small" type="button" onClick={onBack}>
          ← На главную
        </button>
      </header>

      <div className="auth__content">
        <div className="auth__cards">
          <article className="auth-card auth-card--employee">
            <h2>Я сотрудник</h2>
            <p>Создайте профиль, пройдите краткий onboarding и загрузите своё CV.</p>
            <button className="btn btn-purple btn-full" type="button" onClick={onRegisterEmployee}>
              Зарегистрироваться
            </button>
          </article>

          <article className="auth-card auth-card--hr">
            <h2>Я HR</h2>
            <p>Подключитесь к панели управления и управляйте папками с CV кандидатов.</p>
            <button className="btn btn-outline btn-full" type="button" onClick={onRegisterHr}>
              Зарегистрироваться
            </button>
          </article>
        </div>

        <div className="auth__login">
          <h3>Уже есть аккаунт?</h3>
          <p className="auth__hint">Выберите роль, чтобы продолжить.</p>
          <div className="auth__role">
            <label className={`auth__pill ${loginRole === 'employee' ? 'is-active' : ''}`}>
              <input
                type="radio"
                name="login-role"
                value="employee"
                checked={loginRole === 'employee'}
                onChange={() => setLoginRole('employee')}
              />
              Сотрудник
            </label>
            <label className={`auth__pill ${loginRole === 'hr' ? 'is-active' : ''}`}>
              <input
                type="radio"
                name="login-role"
                value="hr"
                checked={loginRole === 'hr'}
                onChange={() => setLoginRole('hr')}
              />
              HR
            </label>
          </div>
          <button className="btn btn-green btn-full" type="button" onClick={() => onLogin(loginRole)}>
            Войти
          </button>
        </div>
      </div>
    </div>
  )
}

function EmployeeOnboarding({
  currentSlide,
  onChangeSlide,
  onComplete,
  onClose,
  existingFileName,
}) {
  const [selectedFileName, setSelectedFileName] = React.useState(existingFileName ?? '')

  React.useEffect(() => {
    setSelectedFileName(existingFileName ?? '')
  }, [existingFileName])

  const goNext = () => onChangeSlide(Math.min(2, currentSlide + 1))
  const goPrev = () => onChangeSlide(Math.max(0, currentSlide - 1))

  const handleUploadChange = (event) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFileName(file.name)
    }
  }

  const handleComplete = () => {
    if (!selectedFileName) {
      return
    }

    onComplete(selectedFileName)
  }

  return (
    <div className="onboarding">
      <div className="onboarding__card">
        <button className="icon-button icon-button--ghost onboarding__close" type="button" onClick={onClose}>
          <CloseIcon className="icon icon--small" />
        </button>

        {currentSlide === 0 && (
          <div className="onboarding__content">
            <div className="onboarding__badge">Шаг 1</div>
            <h2>Привет! Тебе предстоит загрузить своё CV.</h2>
            <p>Вот несколько шагов, чтобы сделать это правильно и рассказать о себе актуальную информацию.</p>
          </div>
        )}

        {currentSlide === 1 && (
          <div className="onboarding__content">
            <div className="onboarding__badge">Шаг 2</div>
            <h2>Критерии идеального CV</h2>
            <ul className="onboarding__list">
              <li>Добавьте актуальный опыт, образование и ключевые проекты.</li>
              <li>Отметьте навыки и инструменты, с которыми вы работаете.</li>
              <li>Используйте PDF или DOCX для корректного отображения.</li>
            </ul>
          </div>
        )}

        {currentSlide === 2 && (
          <div className="onboarding__content">
            <div className="onboarding__badge">Шаг 3</div>
            <h2>Загрузите своё CV</h2>
            <p>Мы проанализируем документ и подготовим ваш личный кабинет.</p>
            <label className="onboarding__upload">
              <input type="file" accept=".pdf,.doc,.docx" onChange={handleUploadChange} />
              <span>{selectedFileName ? selectedFileName : 'Перетащите файл или выберите его'}</span>
            </label>
            <p className="onboarding__note">Поддерживаем файлы до 15 МБ.</p>
          </div>
        )}

        <footer className="onboarding__footer">
          <div className="onboarding__dots">
            {[0, 1, 2].map((dot) => (
              <span key={dot} className={`onboarding__dot ${currentSlide === dot ? 'is-active' : ''}`} />
            ))}
          </div>
          <div className="onboarding__actions">
            {currentSlide > 0 && (
              <button className="btn btn-ghost" type="button" onClick={goPrev}>
                Назад
              </button>
            )}
            {currentSlide < 2 && (
              <button className="btn btn-purple" type="button" onClick={goNext}>
                Далее
              </button>
            )}
            {currentSlide === 2 && (
              <button className="btn btn-green" type="button" disabled={!selectedFileName} onClick={handleComplete}>
                Перейти в кабинет
              </button>
            )}
          </div>
        </footer>
      </div>
    </div>
  )
}

function EmployeeDashboard({ data, onLogout, onReupload, onOpenTasks }) {
  return (
    <div className="employee-dashboard">
      <header className="dashboard-header">
        <span className="brand">HR-АССИСТЕНТ</span>
        <button className="icon-button" type="button" onClick={onLogout} aria-label="Выйти из профиля">
          <LogoutIcon className="icon" />
        </button>
      </header>

      <div className="employee-dashboard__top">
        <div className="profile-card">
          <div className="profile-card__avatar">{data.fullName.slice(0, 1)}</div>
          <div>
            <h2 className="profile-card__name">{data.fullName}</h2>
            <div className="profile-card__metrics">
              <div className="profile-card__metric">
                <span className="profile-card__metric-label">Рейтинг:</span>
                <RatingStars value={data.rating} />
                <span className="profile-card__metric-value">{data.rating.toFixed(1)}</span>
              </div>
              <div className="profile-card__metric">
                <span className="profile-card__metric-label">XP:</span>
                <span className="profile-card__metric-value">{data.xp}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="badge-panel">
          <h3>Бейджи</h3>
          <div className="badge-panel__list">
            {data.badges.map((badge) => (
              <span key={badge} className="badge-panel__badge">
                {badge}
              </span>
            ))}
          </div>
        </div>
      </div>

      <section className="employee-dashboard__grid">
        {data.history.map((item) => (
          <article key={item.id} className="info-card">
            <span className="info-card__label">{item.title}</span>
            <span className="info-card__value">{item.value}</span>
          </article>
        ))}
      </section>

      <section className="cv-card">
        <div>
          <h3>Загруженное CV</h3>
          {data.cvFileName ? (
            <>
              <p className="cv-card__file">{data.cvFileName}</p>
              {data.uploadedAt && <p className="cv-card__time">Загружено: {data.uploadedAt}</p>}
            </>
          ) : (
            <p className="cv-card__placeholder">Загрузите CV, чтобы мы показали данные профиля.</p>
          )}
        </div>
        <div className="cv-card__actions">
          <button className="btn btn-green" type="button" onClick={onReupload}>
            Загрузить CV
          </button>
          <button className="btn btn-purple" type="button" onClick={onOpenTasks}>
            Посмотреть задачи
          </button>
        </div>
      </section>
    </div>
  )
}

function HrDashboard({ onLogout }) {
  const [expandedFolders, setExpandedFolders] = React.useState({})

  const toggleFolder = (folderId) => {
    setExpandedFolders((prev) => ({
      ...prev,
      [folderId]: !prev[folderId],
    }))
  }

  return (
    <div className="hr-dashboard">
      <header className="dashboard-header">
        <span className="brand">HR-АССИСТЕНТ</span>
        <button className="btn btn-ghost btn-small" type="button" onClick={onLogout}>
          ← Выйти
        </button>
      </header>

      <div className="hr-dashboard__intro">
        <h1>Папки с CV кандидатов</h1>
        <p>Доступны подборки резюме по направлениям. Открывайте папку, чтобы просмотреть список кандидатов.</p>
      </div>

      <div className="hr-dashboard__grid">
        {hrFolders.map((folder) => {
          const isOpen = Boolean(expandedFolders[folder.id])

          return (
            <article key={folder.id} className="folder-card" style={{ '--accent': folder.accent }}>
              <div className="folder-card__icon">
                <FolderIcon className="icon" />
              </div>
              <div className="folder-card__body">
                <h2>{folder.name}</h2>
                <p>{folder.count} CV</p>
                <span>Обновлено {folder.updated}</span>
              </div>
              <button
                className="folder-card__action"
                type="button"
                onClick={() => toggleFolder(folder.id)}
                aria-expanded={isOpen}
              >
                {isOpen ? 'Скрыть список' : 'Открыть папку'}
              </button>

              {isOpen && (
                <ul className="folder-card__list">
                  {folder.files.map((file) => (
                    <li key={file.id} className="folder-card__item">
                      <div className="folder-card__file">
                        <span className="folder-card__file-icon">
                          <PdfIcon className="icon icon--small" />
                        </span>
                        <div className="folder-card__file-info">
                          <p className="folder-card__file-name">{file.name}</p>
                          <span className="folder-card__file-meta">Загружено {file.uploaded}</span>
                        </div>
                      </div>
                      <span className="folder-card__badge">PDF</span>
                    </li>
                  ))}
                </ul>
              )}
            </article>
          )
        })}
      </div>
    </div>
  )
}

function TaskModal({ onClose }) {
  return (
    <div className="modal" role="dialog" aria-modal="true">
      <div className="modal__backdrop" onClick={onClose} />
      <div className="modal__dialog" role="document">
        <header className="modal__header">
          <div>
            <h2>To-do для улучшения CV</h2>
            <p className="modal__subtitle">Отметьте, что уже сделали, и вернитесь к редактированию документа.</p>
          </div>
          <button className="icon-button icon-button--ghost modal__close" type="button" onClick={onClose}>
            <CloseIcon className="icon icon--small" />
          </button>
        </header>

        <ul className="todo-list">
          {taskSuggestions.map((task) => (
            <li key={task.id} className="todo-item">
              <label className="todo-item__label">
                <input className="todo-item__checkbox" type="checkbox" />
                <span className="todo-item__content">
                  <span className="todo-item__title">{task.title}</span>
                  <span className="todo-item__details">{task.details}</span>
                </span>
              </label>
            </li>
          ))}
        </ul>

        <footer className="modal__footer">
          <h3>Рекомендации по CV</h3>
          <ul className="modal__recommendations">
            {cvRecommendations.map((tip, index) => (
              <li key={index}>{tip}</li>
            ))}
          </ul>
          <button className="btn btn-purple btn-full" type="button" onClick={onClose}>
            Готово
          </button>
        </footer>
      </div>
    </div>
  )
}

function RatingStars({ value }) {
  return (
    <span className="stars">
      {Array.from({ length: 5 }).map((_, index) => {
        const position = index + 1
        const diff = value - index
        const isFull = diff >= 1 || (value >= position && diff > 0.75)
        const isHalf = !isFull && diff >= 0.25

        return (
          <span
            key={position}
            className={`stars__item ${isFull ? 'stars__item--full' : ''} ${isHalf ? 'stars__item--half' : ''}`}
          >
            ★
          </span>
        )
      })}
    </span>
  )
}

function UserIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="8" r="4" />
      <path d="M5 20c0-3.5 3.1-5.5 7-5.5s7 2 7 5.5" />
    </svg>
  )
}

function LogoutIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M15 3h-6a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h6" />
      <path d="M10 12h10" />
      <path d="m17 9 3 3-3 3" />
    </svg>
  )
}

function CloseIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m7 7 10 10" />
      <path d="m17 7-10 10" />
    </svg>
  )
}

function FolderIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z" />
      <path d="M3 9h18" />
    </svg>
  )
}

function PdfIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M7 3h7l5 5v11a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z" />
      <path d="M14 3v5h5" />
      <path d="M8 13h1.8a1 1 0 0 1 0 2H8v-2Z" />
      <path d="M8 15h1.4" />
      <path d="M12 13h2.2a1 1 0 0 1 1 1v1.5a1 1 0 0 1-1 1H12V13Z" />
      <path d="M12 16.5h2" />
      <path d="M17 13h2" />
      <path d="M18 13v3.5" />
    </svg>
  )
}

