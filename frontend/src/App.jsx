import React, { useState } from 'react'
import './App.css'

// Компонент для показа уведомлений о начислении XP
const XPNotification = ({ show, xpAmount, message, onClose }) => {
  console.log('XPNotification render:', { show, xpAmount, message }); // Отладка
  
  React.useEffect(() => {
    if (show) {
      console.log('XPNotification showing, setting timer'); // Отладка
      const timer = setTimeout(() => {
        onClose();
      }, 3000); // Автоматически скрываем через 3 секунды
      return () => clearTimeout(timer);
    }
  }, [show, onClose]);

  if (!show) return null;

  return (
    <div className="xp-notification" style={{
      position: 'fixed',
      top: '40%',
      right: '20px',
      zIndex: 1000,
      backgroundColor: 'linear-gradient(135deg, #10b981, #059669)',
      background: 'linear-gradient(135deg, #10b981, #059669)',
      padding: '16px 20px',
      borderRadius: '12px',
      boxShadow: '0 8px 32px rgba(16, 185, 129, 0.3)',
      color: 'white',
      minWidth: '300px',
      maxWidth: '400px'
    }}>
      <div className="xp-notification__content" style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <div className="xp-notification__icon" style={{fontSize: '24px'}}>🎉</div>
        <div className="xp-notification__text" style={{flex: 1}}>
          <div className="xp-notification__title" style={{
            fontWeight: '700',
            fontSize: '16px',
            marginBottom: '4px'
          }}>Поздравляем!</div>
          <div className="xp-notification__message" style={{
            fontSize: '14px',
            opacity: '0.9',
            marginBottom: '4px'
          }}>{message}</div>
          <div className="xp-notification__xp" style={{
            fontWeight: '700',
            fontSize: '18px',
            color: '#fbbf24'
          }}>+{xpAmount} XP</div>
        </div>
        <button 
          className="xp-notification__close" 
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            fontSize: '20px',
            cursor: 'pointer',
            padding: '4px',
            borderRadius: '4px'
          }}
        >×</button>
      </div>
    </div>
  );
};

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
  const [token, setToken] = React.useState(localStorage.getItem('token'));
  const [userData, setUserData] = React.useState(null);
  const [isFirstLogin, setIsFirstLogin] = React.useState(false);
  const [showCvManager, setShowCvManager] = React.useState(false);
  const [dashboardKey, setDashboardKey] = React.useState(0); // Для принудительного обновления EmployeeDashboard
  
  // Состояние для XP уведомлений
  const [xpNotification, setXpNotification] = React.useState({
    show: false,
    xpAmount: 0,
    message: ''
  });

  // Функция для показа XP уведомления
  const showXPNotification = React.useCallback((xpAmount, message) => {
    console.log('showXPNotification called:', { xpAmount, message }); // Отладка
    
    // Показываем уведомление
    setXpNotification({
      show: true,
      xpAmount,
      message
    });
    
    // Обновляем XP в userData
    setUserData(prev => {
      if (!prev) return prev;
      return {
        ...prev,
        xp: (prev.xp || 0) + xpAmount
      };
    });
  }, []);

  // Функция для скрытия XP уведомления
  const hideXPNotification = React.useCallback(() => {
    setXpNotification(prev => ({ ...prev, show: false }));
  }, []);

  // Функция для загрузки данных пользователя с бейджами
  const loadUserDataWithBadges = React.useCallback(async (token) => {
    try {
      // Загружаем профиль пользователя
      const data = await api.getUserProfile(token);
      
      // Загружаем бейджи отдельно
      const badges = await api.getMyBadges(token);
      
      // Маппим данные в нужный формат
      const mapped = {
        fullName: data.full_name || data.fullName || data.name || data.email || 'Пользователь',
        rating: (data.rating !== undefined && data.rating !== null) ? data.rating : 0,
        xp: (data.xp !== undefined && data.xp !== null) ? data.xp : 0,
        badges: badges, // Используем бейджи из отдельного эндпоинта (уже ограничены 3 последними)
        cvFileName: data.cv_file_name || data.cvFileName || data.cv || '',
        uploadedAt: data.uploaded_at || data.uploadedAt || '',
        // keep raw profile in case other components need it
        __raw: data,
      };

      setUserData(mapped);
      return { mapped, data };
    } catch (error) {
      console.error('Error loading user data:', error);
      throw error;
    }
  }, []);

  React.useEffect(() => {
    if (token) {
      loadUserDataWithBadges(token)
        .then(async ({ mapped, data }) => {

          const role = (data.role || data.user_role || '').toString().toLowerCase();
          
          if (role === 'hr') {
            setView('hrDashboard');
          } else {
            // Для сотрудников проверяем наличие CV через API
            try {
              const cvs = await api.getMyCvs(token);
              const hasCV = cvs && cvs.length > 0;
              
              if (!hasCV) {
                // Если CV нет - показываем CvManager как первый вход
                setIsFirstLogin(true);
                setShowCvManager(true);
                setView('cvManager');
              } else {
                // Если CV есть - переходим в дашборд
                setView('employeeDashboard');
              }
            } catch (error) {
              // Если ошибка при получении CV - считаем что CV нет
              console.error('Error checking CV:', error);
              setIsFirstLogin(true);
              setShowCvManager(true);
              setView('cvManager');
            }
          }
        })
        .catch(() => {
          localStorage.removeItem('token');
          setToken(null);
          setView('landing');
        });
    }
  }, [token]);
  
  const [view, setView] = useState('landing')
  const [onboardingSlide, setOnboardingSlide] = useState(0)
  const [employeeData, setEmployeeData] = useState(() => makeEmployeeData())
  const [showTaskModal, setShowTaskModal] = useState(false)

  const goLanding = () => {
    // Очищаем токен при выходе
    localStorage.removeItem('token')
    setToken(null)
    setUserData(null)
    
    // Сбрасываем состояние приложения
    setView('landing')
    setOnboardingSlide(0)
    setShowTaskModal(false)
    setIsFirstLogin(false)
    setShowCvManager(false)
    setDashboardKey(0)
  }

  const handleEmployeeRegistration = () => {
    setEmployeeData(makeEmployeeData())
    setOnboardingSlide(0)
    setShowTaskModal(false)
    setView('employeeOnboarding')
  }

  const handleOldCvUploaded = (fileName) => {
    if (!fileName) {
      return
    }

    setEmployeeData((prev) => ({
      ...prev,
      cvFileName: fileName,
      uploadedAt: new Date().toLocaleString('ru-RU', {
        timeZone: 'Europe/Moscow',
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

  const handleCvUploaded = () => {
    setIsFirstLogin(false);
    setShowCvManager(false);
    setView('employeeDashboard');
    setDashboardKey(prev => prev + 1); // Принудительно обновляем EmployeeDashboard
    
    // Показываем уведомление о начислении XP
    showXPNotification(40, 'Вы успешно загрузили CV!');
    
    // Загружаем обновленную информацию о пользователе с небольшой задержкой
    if (token) {
      setTimeout(() => {
        loadUserDataWithBadges(token)
          .catch(console.error);
      }, 500); // Даем время показать локальное обновление XP
    }
  };

  const handleShowCvManager = () => {
    setIsFirstLogin(false);
    setShowCvManager(true);
    setView('cvManager');
  };

  const handleCloseCvManager = () => {
    setShowCvManager(false);
    setDashboardKey(prev => prev + 1); // Обновляем dashboard при закрытии CvManager
    
    // При первом входе всё равно переходим в личный кабинет, даже если CV не загружено
    if (isFirstLogin) {
      setIsFirstLogin(false);
      setView('employeeDashboard');
    } else {
      setView('employeeDashboard');
    }
  };

  return (
    <div className={`app app--${view}`}>
      {view === 'landing' && <LandingPage onStart={() => setView('auth')} />}

      {view === 'auth' && (
        <AuthPage
          onBack={goLanding}
          onRegisterEmployee={handleEmployeeRegistration}
          onRegisterHr={() => setView('hrDashboard')}
          onLogin={handleLogin}
          onSetToken={setToken}
        />
      )}

      {view === 'employeeOnboarding' && (
        <EmployeeOnboarding
          currentSlide={onboardingSlide}
          onChangeSlide={setOnboardingSlide}
          onComplete={handleOldCvUploaded}
          onClose={goLanding}
          existingFileName={employeeData.cvFileName}
        />
      )}

      {(view === 'cvManager' || showCvManager) && (
        <CvManager
          isFirstLogin={isFirstLogin}
          token={token}
          onCvUploaded={handleCvUploaded}
          onClose={handleCloseCvManager}
          userData={userData}
        />
      )}

      {view === 'employeeDashboard' && (
        <EmployeeDashboard
          key={dashboardKey}
          data={userData || employeeData}
          onLogout={goLanding}
          onReupload={handleShowCvManager}
          onOpenTasks={() => setShowTaskModal(true)}
          showXPNotification={showXPNotification}
        />
      )}

      {view === 'hrDashboard' && <HrDashboard onLogout={goLanding} />}

      {showTaskModal && <TaskModal onClose={() => setShowTaskModal(false)} />}
      
      {/* XP Notification */}
      <XPNotification 
        show={xpNotification.show}
        xpAmount={xpNotification.xpAmount}
        message={xpNotification.message}
        onClose={hideXPNotification}
      />
    </div>
  )
}

function LandingPage({ onStart }) {
  return (
    <div className="landing">
      <header className="landing__header">
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
            <span>HR-counselor</span>
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

import { api } from './api';

// Утилита для форматирования времени в московском часовом поясе
const formatMoscowTime = (dateString) => {
  if (!dateString) return 'Не указано';
  
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    timeZone: 'Europe/Moscow',
    day: '2-digit',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  });
};

// Утилита для форматирования даты в московском часовом поясе
const formatMoscowDate = (dateString) => {
  if (!dateString) return 'Не указано';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    timeZone: 'Europe/Moscow'
  });
};

function AuthPage({ onBack, onRegisterEmployee, onRegisterHr, onLogin, onSetToken }) {
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [mode, setMode] = React.useState('login')
  const [loginRole, setLoginRole] = React.useState('employee')
  const [loginEmail, setLoginEmail] = React.useState('')
  const [loginPassword, setLoginPassword] = React.useState('')
  const [registerRole, setRegisterRole] = React.useState('employee')
  const [registerEmail, setRegisterEmail] = React.useState('')
  const [registerName, setRegisterName] = React.useState('')
  const [registerPassword, setRegisterPassword] = React.useState('')
  const [registerConfirm, setRegisterConfirm] = React.useState('')
  const [loginError, setLoginError] = React.useState('')
  const [registerError, setRegisterError] = React.useState('')

  const openRegister = () => {
    setRegisterRole(loginRole)
    setMode('register')
  }

  const backToLogin = () => {
    setMode('login')
    setRegisterEmail('')
    setRegisterName('')
    setRegisterPassword('')
    setRegisterConfirm('')
  }

  const handleRegister = async () => {
    try {
      setIsLoading(true);
      setError(null);
      setRegisterError('');

      // Проверяем формат email
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailRegex.test(registerEmail)) {
        setRegisterError('Некорректный формат email адреса');
        return;
      }

      // Проверяем длину пароля
      if (registerPassword.length < 6) {
        setRegisterError('Пароль должен содержать минимум 6 символов');
        return;
      }
      
      // Преобразуем роль в нужный формат
      const roleMap = {
        'employee': 'user',
        'hr': 'hr'
      };
      
      const data = {
        email: registerEmail,
        password: registerPassword,
        full_name: registerName,
        role: roleMap[registerRole] || 'user'
      };

      const response = await api.register(data);
      localStorage.setItem('token', response.access_token);
      
      // notify parent about token and navigate
      if (typeof onSetToken === 'function') onSetToken(response.access_token);
      if (registerRole === 'employee') {
        onRegisterEmployee();
      } else {
        onRegisterHr();
      }
    } catch (error) {
      // if user already exists, show friendly message
      if (error && error.status === 409) {
        setRegisterError('Пользователь с таким email уже существует. Попробуйте войти.');
        setMode('login');
        setLoginEmail(registerEmail);
      } else {
        setRegisterError(error.message || 'Ошибка при регистрации');
      }
    } finally {
      setIsLoading(false);
    }
  }

  const handleLogin = async () => {
    try {
      setIsLoading(true);
      setLoginError('');
      const data = {
        email: loginEmail,
        password: loginPassword,
      };

      const response = await api.login(data);
      localStorage.setItem('token', response.access_token);
      if (typeof onSetToken === 'function') onSetToken(response.access_token);

      // fetch profile to determine role
      try {
        const profile = await api.getUserProfile(response.access_token);
        onLogin(profile.role.toLowerCase());
      } catch (e) {
        // if profile fetch failed, still call onLogin with chosen role
        onLogin(loginRole);
      }
    } catch (error) {
      // if backend returns 404 or specific 'user not found' message, switch to register
      if (error && (error.status === 404 || /not found|does not exist|no user/i.test(error.message))) {
        setLoginError('Пользователь не найден. Пожалуйста, зарегистрируйтесь.');
        setRegisterEmail(loginEmail);
        setRegisterRole(loginRole);
        setMode('register');
      } else if (error && error.status === 401) {
        setLoginError('Неверный пароль.');
      } else {
        setLoginError(error.message || 'Ошибка при входе');
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="auth">
      <header className="dashboard-header">
        <span className="brand">HR-Counselor</span>
        <button className="btn btn-ghost btn-small" type="button" onClick={onBack}>
          Назад к началу
        </button>
      </header>

      <div className="auth__content">
        {mode === 'login' && (
          <section className="auth__login auth__panel">
            <div className="auth__login-header">
              <h3>У вас уже есть аккаунт?</h3>
            </div>

            <div className="auth__fields">
              <label className="auth__field">
                <span>Электронная почта</span>
                <input type="email" value={loginEmail} onChange={(event) => setLoginEmail(event.target.value)} placeholder="name@email.com" />
              </label>
              <label className="auth__field">
                <span>Пароль</span>
                <input type="password" value={loginPassword} onChange={(event) => setLoginPassword(event.target.value)} placeholder="Введите пароль" />
              </label>
            </div>

            {loginError && <div className="auth__error">{loginError}</div>}
            <div className="auth__actions">
              <button className="btn btn-green btn-full" type="button" onClick={handleLogin} disabled={isLoading}>
                {isLoading ? 'Загрузка...' : 'Войти'}
              </button>
              <button className="auth__switch" type="button" onClick={openRegister}>
                Зарегистрироваться
              </button>
            </div>
          </section>
        )}

        {mode === 'register' && (
          <section className="auth__panel auth__register">
            <div className="auth__register-header">
              <h3>Регистрация</h3>
              <p className="auth__hint">Выберите роль, затем пройдите онбординг и загрузите CV.</p>
            </div>

            <div className="auth__role">
              <label className={`auth__pill ${registerRole === 'employee' ? 'is-active' : ''}`}>
                <input type="radio" name="register-role" value="employee" checked={registerRole === 'employee'} onChange={() => setRegisterRole('employee')} />
                Сотрудник
              </label>
              <label className={`auth__pill ${registerRole === 'hr' ? 'is-active' : ''}`}>
                <input type="radio" name="register-role" value="hr" checked={registerRole === 'hr'} onChange={() => setRegisterRole('hr')} />
                HR
              </label>
            </div>

            <div className="auth__fields">
              <label className="auth__field">
                <span>Электронная почта</span>
                <input type="email" value={registerEmail} onChange={(event) => setRegisterEmail(event.target.value)} placeholder="name@email.com" />
              </label>
              <label className="auth__field">
                <span>ФИО</span>
                <input type="text" value={registerName} onChange={(event) => setRegisterName(event.target.value)} placeholder="Иванов Иван Иванович" />
              </label>
              <label className="auth__field">
                <span>Пароль</span>
                <input type="password" value={registerPassword} onChange={(event) => setRegisterPassword(event.target.value)} placeholder="Придумайте пароль" />
              </label>
            </div>

            {registerError && <div className="auth__error">{registerError}</div>}
            <div className="auth__actions">
              <button className="btn btn-purple btn-full" type="button" onClick={handleRegister} disabled={isLoading}>
                {isLoading ? 'Загрузка...' : 'Зарегистрироваться'}
              </button>
              <button className="auth__switch" type="button" onClick={backToLogin}>
                У меня уже есть аккаунт
              </button>
            </div>
          </section>
        )}
      </div>
    </div>
  )
}

function CvManager({ 
  isFirstLogin, 
  token, 
  onCvUploaded, 
  onClose, 
  userData 
}) {
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [selectedFile, setSelectedFile] = React.useState(null);
  const [currentCv, setCurrentCv] = React.useState(null);
  const [showUploadForm, setShowUploadForm] = React.useState(isFirstLogin);

  // Загружаем информацию о текущем CV при монтировании (если не первый вход)
  React.useEffect(() => {
    if (!isFirstLogin && token) {
      loadCurrentCv();
    }
  }, [isFirstLogin, token]);

  const loadCurrentCv = async () => {
    try {
      setIsLoading(true);
      const cvs = await api.getMyCvs(token);
      if (cvs && cvs.length > 0) {
        setCurrentCv(cvs[0]); // Берем последнее загруженное CV
      }
    } catch (err) {
      console.error('Ошибка загрузки CV:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setError('Пожалуйста, выберите PDF файл');
        return;
      }
      if (file.size > 15 * 1024 * 1024) { // 15MB
        setError('Размер файла не должен превышать 15 МБ');
        return;
      }
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Пожалуйста, выберите файл');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      const response = await api.uploadCv(token, selectedFile);
      
      if (isFirstLogin) {
        // При первом входе - переходим в личный кабинет
        onCvUploaded();
      } else {
        // При замене CV - обновляем данные
        await loadCurrentCv();
        setShowUploadForm(false);
        setSelectedFile(null);
      }
    } catch (err) {
      setError(err.message || 'Ошибка при загрузке файла');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!currentCv) return;

    try {
      setIsLoading(true);
      const blob = await api.downloadCv(token, currentCv.id);
      
      // Создаем ссылку для скачивания
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = currentCv.original_filename || 'cv.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message || 'Ошибка при скачивании файла');
    } finally {
      setIsLoading(false);
    }
  };

  if (isFirstLogin) {
    return (
      <div className="onboarding">
        <div className="onboarding__card">
          <button className="icon-button icon-button--ghost onboarding__close" type="button" onClick={onClose}>
            <CloseIcon className="icon icon--small" />
          </button>

          <div className="onboarding__content">
            <div className="onboarding__badge">Добро пожаловать!</div>
            <h2>Загрузите ваше резюме (CV)</h2>
            <p>Это поможет нам лучше подобрать для вас вакансии и курсы. Вы можете сделать это сейчас или позже в личном кабинете.</p>
            
            <div className="cv-recommendations">
              <h3>Рекомендации для идеального CV:</h3>
              <ul className="onboarding__list">
                {cvRecommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>

            <label className="onboarding__upload">
              <input 
                type="file" 
                accept=".pdf" 
                onChange={handleFileSelect}
                disabled={isLoading}
              />
              <span>
                {selectedFile ? selectedFile.name : 'Перетащите PDF файл или выберите его'}
              </span>
            </label>
            
            <p className="onboarding__note">Поддерживаются PDF файлы до 15 МБ.</p>
            
            {error && <div className="auth__error">{error}</div>}
          </div>

          <footer className="onboarding__footer">
            <div className="onboarding__actions">
              <button 
                className="btn btn-ghost" 
                type="button" 
                onClick={onClose}
              >
                Пропустить
              </button>
              <button 
                className="btn btn-green" 
                type="button" 
                onClick={handleUpload}
                disabled={!selectedFile || isLoading}
              >
                {isLoading ? 'Загрузка...' : 'Загрузить и перейти в кабинет'}
              </button>
            </div>
          </footer>
        </div>
      </div>
    );
  }

  // Повторный вход - показываем информацию о текущем CV
  return (
    <div className="cv-manager">
      <div className="cv-manager__header">
        <h2>Управление CV</h2>
        <button className="icon-button icon-button--ghost" type="button" onClick={onClose}>
          <CloseIcon className="icon icon--small" />
        </button>
      </div>
      <div className="cv-manager__content">
        {isLoading && !currentCv ? (
          <div className="cv-manager__loading">Загрузка...</div>
        ) : currentCv ? (
          <div className="cv-manager__current">
            <h3>Ваше CV</h3>
            <div className="cv-card">
              <div className="cv-card__info">
                <p className="cv-card__file">{currentCv.original_filename}</p>
                <p className="cv-card__time">
                  Загружено: {formatMoscowTime(currentCv.uploaded_at)}
                </p>
              </div>
              <div className="cv-card__actions">
                <button 
                  className="btn btn-green" 
                  type="button" 
                  onClick={handleDownload}
                  disabled={isLoading}
                >
                  {isLoading ? 'Загрузка...' : 'Скачать CV'}
                </button>
                <button 
                  className="btn btn-purple" 
                  type="button" 
                  onClick={() => setShowUploadForm(true)}
                >
                  Обновить CV
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="cv-manager__empty">
            <p>CV не найдено</p>
            <div className="cv-manager__empty-actions">
              <button 
                className="btn btn-green" 
                type="button" 
                onClick={() => setShowUploadForm(true)}
              >
                Загрузить CV
              </button>
              <button 
                className="btn btn-outline" 
                type="button" 
                onClick={onClose}
              >
                Выйти
              </button>
            </div>
          </div>
        )}

        {showUploadForm && !isFirstLogin && (
          <div className="cv-manager__upload">
            <h4>{currentCv ? 'Обновить CV' : 'Загрузить новое CV'}</h4>
            <label className="onboarding__upload">
              <input 
                type="file" 
                accept=".pdf" 
                onChange={handleFileSelect}
                disabled={isLoading}
              />
              <span>
                {selectedFile ? selectedFile.name : 'Выберите PDF файл'}
              </span>
            </label>
            
            {error && <div className="auth__error">{error}</div>}
            
            <div className="cv-manager__upload-actions">
              <button 
                className="btn btn-green" 
                type="button" 
                onClick={handleUpload}
                disabled={!selectedFile || isLoading}
              >
                {isLoading ? 'Загрузка...' : (currentCv ? 'Обновить CV' : 'Загрузить CV')}
              </button>
              <button 
                className="btn btn-ghost" 
                type="button" 
                onClick={() => {
                  setShowUploadForm(false);
                  setSelectedFile(null);
                  setError(null);
                }}
              >
                Отмена
              </button>
              <button 
                className="btn btn-outline" 
                type="button" 
                onClick={onClose}
              >
                Выйти
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
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


function EmployeeDashboard({ data, onLogout, onReupload, onOpenTasks, showXPNotification }) {
  // Функция для перевода уровней
  const getJobLevelLabel = (level) => {
    const levelLabels = {
      'intern': 'Стажер',
      'junior': 'Junior',
      'middle': 'Middle',
      'senior': 'Senior',
      'lead': 'Lead',
      'manager': 'Менеджер'
    };
    return levelLabels[level] || level;
  };

  const [activeTab, setActiveTab] = React.useState('personal_assistant')
  const [editMode, setEditMode] = React.useState(false)
  const [currentCv, setCurrentCv] = React.useState(null)
  const [isLoadingCv, setIsLoadingCv] = React.useState(true)
  const [courses, setCourses] = React.useState([])
  const [isLoadingCourses, setIsLoadingCourses] = React.useState(false)
  const [selectedCourse, setSelectedCourse] = React.useState(null)
  const [isLoadingCourseDetails, setIsLoadingCourseDetails] = React.useState(false)
  const [isEnrolling, setIsEnrolling] = React.useState(false)
  const [enrollmentMessage, setEnrollmentMessage] = React.useState('')
  const [myEnrollments, setMyEnrollments] = React.useState([])
  const [token] = React.useState(localStorage.getItem('token'))
  
  // Состояния для профиля пользователя
  const [userProfile, setUserProfile] = React.useState(null)
  const [isLoadingProfile, setIsLoadingProfile] = React.useState(true)
  
  // Состояния для редактирования CV данных
  const [editedCvData, setEditedCvData] = React.useState({})
  const [isSaving, setIsSaving] = React.useState(false)
  const [saveMessage, setSaveMessage] = React.useState('')
  
  // Обернутая версия showXPNotification, которая также обновляет локальный userProfile
  const showXPNotificationWithLocalUpdate = React.useCallback((xpAmount, message) => {
    // Вызываем оригинальную функцию
    showXPNotification(xpAmount, message);
    
    // Обновляем локальный userProfile
    setUserProfile(prev => {
      if (!prev) return prev;
      return {
        ...prev,
        xp: (prev.xp || 0) + xpAmount
      };
    });
  }, [showXPNotification]);
  
  // Состояния для личного помощника
  const [assistantMessages, setAssistantMessages] = React.useState([
    { from: 'bot', text: 'Привет! Я ваш личный помощник. Помогу с карьерными вопросами, анализом резюме и планированием развития. Что вас интересует?' }
  ])
  const [assistantInput, setAssistantInput] = React.useState('')
  const [completedTasks, setCompletedTasks] = React.useState([])
  
  // Состояния для вакансий
  const [jobs, setJobs] = React.useState([])
  const [isLoadingJobs, setIsLoadingJobs] = React.useState(false)

  // Загружаем информацию о CV и профиле при монтировании компонента
  React.useEffect(() => {
    if (token) {
      loadCvInfo();
      loadUserProfile();
      loadCourses();
      loadMyEnrollments();
      loadJobs();
    }
  }, [token]);

  const loadCvInfo = async () => {
    try {
      setIsLoadingCv(true);
      const cvs = await api.getMyCvs(token);
      if (cvs && cvs.length > 0) {
        setCurrentCv(cvs[0]); // Берем последнее загруженное CV
      } else {
        setCurrentCv(null);
      }
    } catch (error) {
      console.error('Ошибка загрузки CV:', error);
      setCurrentCv(null);
    } finally {
      setIsLoadingCv(false);
    }
  };

  const loadUserProfile = async () => {
    try {
      setIsLoadingProfile(true);
      const profile = await api.getUserProfile(token);
      setUserProfile(profile);
    } catch (error) {
      console.error('Ошибка загрузки профиля пользователя:', error);
      setUserProfile(null);
    } finally {
      setIsLoadingProfile(false);
    }
  };

  // Функции для редактирования CV
  const handleFieldChange = (field, value) => {
    setEditedCvData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const saveChanges = async () => {
    if (!currentCv || Object.keys(editedCvData).length === 0) {
      setSaveMessage('Нет изменений для сохранения');
      return;
    }

    try {
      setIsSaving(true);
      setSaveMessage('');
      
      await api.updateCv(token, currentCv.id, editedCvData);
      
      // Показываем уведомление о начислении XP
      showXPNotificationWithLocalUpdate(10, 'Вы обновили информацию в CV!');
      
      // Обновляем локальное состояние
      setCurrentCv(prev => ({
        ...prev,
        ...editedCvData
      }));
      
      // Очищаем изменения
      setEditedCvData({});
      setEditMode(false);
      setSaveMessage('Данные успешно сохранены!');
      
      // Убираем сообщение через 3 секунды
      setTimeout(() => setSaveMessage(''), 3000);
      
    } catch (error) {
      console.error('Ошибка сохранения данных:', error);
      setSaveMessage(error.message || 'Ошибка при сохранении данных');
    } finally {
      setIsSaving(false);
    }
  };

  const cancelEdit = () => {
    setEditMode(false);
    setEditedCvData({});
    setSaveMessage('');
  };

  // Функция для получения значения поля (с учетом редактирования)
  const getFieldValue = (field, defaultValue = 'Не указано') => {
    if (editedCvData.hasOwnProperty(field)) {
      return editedCvData[field];
    }
    return getCvValue(field, defaultValue);
  };

  // Функция для безопасного парсинга JSON полей
  const parseJsonField = (field, defaultValue = 'Не указано') => {
    if (!currentCv || !currentCv[field]) return defaultValue;
    
    const value = currentCv[field];
    if (typeof value === 'string' && (value.startsWith('[') || value.startsWith('{'))) {
      try {
        const parsed = JSON.parse(value);
        if (Array.isArray(parsed)) {
          return parsed.map(item => {
            if (typeof item === 'object') {
              return Object.entries(item)
                .filter(([key, val]) => val && val !== '')
                .map(([key, val]) => `${key}: ${val}`)
                .join(', ');
            }
            return String(item);
          }).join('; ');
        } else if (typeof parsed === 'object') {
          return Object.entries(parsed)
            .filter(([key, val]) => val && val !== '')
            .map(([key, val]) => `${key}: ${val}`)
            .join(', ');
        }
        return String(parsed);
      } catch (e) {
        return value;
      }
    }
    return value || defaultValue;
  };

  // Функция для получения простых полей
  const getCvValue = (field, defaultValue = 'Не указано') => {
    if (!currentCv) return defaultValue;
    return currentCv[field] || defaultValue;
  };

  // Функция для загрузки курсов
  const loadCourses = async () => {
    try {
      setIsLoadingCourses(true);
      const coursesData = await api.getCourses(token);
      setCourses(coursesData || []);
    } catch (error) {
      console.error('Ошибка загрузки курсов:', error);
      setCourses([]);
    } finally {
      setIsLoadingCourses(false);
    }
  };

  // Функция для загрузки моих записей на курсы
  const loadMyEnrollments = async () => {
    try {
      const response = await api.getMyEnrollments(token);
      // API возвращает объект UserEnrollmentsSummary с полем enrollments
      setMyEnrollments(response?.enrollments || []);
    } catch (error) {
      console.error('Ошибка загрузки записей на курсы:', error);
      setMyEnrollments([]);
    }
  };

  // Функция для загрузки вакансий
  const loadJobs = async () => {
    try {
      setIsLoadingJobs(true);
      const jobsResponse = await api.getJobs(token);
      // jobsResponse возвращает объект с полями: jobs, total, page, per_page
      setJobs(jobsResponse.jobs || []);
    } catch (error) {
      console.error('Ошибка загрузки вакансий:', error);
      // В случае ошибки используем статические данные как fallback
      setJobs([
        { id: 'j1', title: 'Frontend Junior', company: 'TechNova', tags: ['React', 'JS', 'HTML/CSS'] },
        { id: 'j2', title: 'Data Analyst', company: 'DataWise', tags: ['SQL', 'Python', 'BI'] },
        { id: 'j3', title: 'QA Engineer', company: 'QualityLab', tags: ['Manual', 'API', 'Postman'] },
      ]);
    } finally {
      setIsLoadingJobs(false);
    }
  };

  // Функция для проверки записи на курс
  const isEnrolledInCourse = (courseId) => {
    return myEnrollments.some(enrollment => enrollment.course_id === courseId);
  };

  // Функция для обработки клика по курсу
  const handleCourseClick = async (course) => {
    try {
      setIsLoadingCourseDetails(true);
      setEnrollmentMessage('');
      const courseDetails = await api.getCourseById(token, course.id);
      setSelectedCourse(courseDetails);
    } catch (error) {
      console.error('Ошибка загрузки деталей курса:', error);
      setEnrollmentMessage('Ошибка при загрузке информации о курсе');
    } finally {
      setIsLoadingCourseDetails(false);
    }
  };

  // Функция для записи на курс
  const handleEnrollInCourse = async () => {
    if (!selectedCourse) return;
    
    try {
      setIsEnrolling(true);
      setEnrollmentMessage('');
      await api.enrollInCourse(token, selectedCourse.id);
      await loadMyEnrollments(); // Перезагружаем список записей
      
      // Показываем уведомление о начислении XP
      showXPNotificationWithLocalUpdate(20, 'Вы записались на курс!');
      
      setEnrollmentMessage('Вы успешно записались на курс!');
      setTimeout(() => {
        setSelectedCourse(null);
        setEnrollmentMessage('');
      }, 2000);
    } catch (error) {
      console.error('Ошибка записи на курс:', error);
      setEnrollmentMessage(error.message || 'Ошибка при записи на курс');
    } finally {
      setIsEnrolling(false);
    }
  };

  // Функция для закрытия модального окна курса
  const handleCloseCourseModal = () => {
    setSelectedCourse(null);
    setEnrollmentMessage('');
  };

  // Функция для отклика на вакансию
  const handleJobApply = (jobTitle) => {
    showXPNotificationWithLocalUpdate(10, `Вы откликнулись на вакансию "${jobTitle}"!`);
  };

  // Состояния для модального окна покупки
  const [purchaseModalOpen, setPurchaseModalOpen] = React.useState(false);
  const [purchaseDetails, setPurchaseDetails] = React.useState(null);

  // Функция для покупки товара в магазине
  const handleStorePurchase = (itemName, priceStr) => {
    // Извлекаем числовое значение из строки цены (например, "500 XP" -> 500)
    const price = parseInt(priceStr);
    if (isNaN(price)) return;

    setPurchaseDetails({ itemName, price });
    setPurchaseModalOpen(true);
  };

  // Проверка достаточности XP
  const hasEnoughXP = (requiredXP) => {
    const currentXP = userProfile?.xp || 0;
    return currentXP >= parseInt(requiredXP);
  };

  const [form, setForm] = React.useState({
    institution: 'Университет Иннополис',
    educationLevel: 'Высшее',
    specialty: 'Специальность не указана',
    graduationYear: '2023',
    addEduName: '',
    addEduCompany: '',
    addEduDate: '',
    addEduHours: '',
    currentPosition: 'Руководитель-направления',
    experienceText: '1 год, 3 месяца',
    functionalRole: '',
    teamRole: '',
    functionDesc: '',
    extraRole: 'Аналитик',
    extraRoleSpec: '',
    languages: 'Русский — родной; Английский — B2',
    otherSkills: 'Agile, Active Directory',
    programming: 'Python, JavaScript',
    prevRole: '',
    prevCompany: '',
    prevPeriod: '',
    prevDuties: '',
    portfolio: '',
    about: '',
    testResults: 'Отсутствуют',
  })

  const roadmap = [
    '3 мес: закрепить основы и закрыть пробелы',
    '6 мес: взять pet‑проект/внутреннюю задачу',
    '12 мес: мидл‑уровень по целевой роли',
  ]

  const set = (key) => (e) => setForm((prev) => ({ ...prev, [key]: e.target.value }))

  // Функции для личного помощника
  const sendAssistantMessage = () => {
    const text = assistantInput.trim()
    if (!text) return
    
    setAssistantMessages(prev => [...prev, { from: 'user', text }])
    setAssistantInput('')
    
    // Имитация ответа бота (заглушка)
    setTimeout(() => {
      const botResponses = [
        'Интересный вопрос! Давайте разберем это подробнее.',
        'Я анализирую ваш запрос. Вот что я могу предложить...',
        'Основываясь на вашем профиле, рекомендую следующее:',
        'Хороший вопрос! Это поможет в вашем карьерном развитии.',
        'Давайте составим план действий по вашему запросу.'
      ]
      const randomResponse = botResponses[Math.floor(Math.random() * botResponses.length)]
      setAssistantMessages(prev => [...prev, { from: 'bot', text: randomResponse }])
    }, 1000)
  }

  const toggleTaskCompletion = (taskId) => {
    setCompletedTasks(prev => 
      prev.includes(taskId) 
        ? prev.filter(id => id !== taskId)
        : [...prev, taskId]
    )
  }

  return (
    <div className="employee-dashboard">
      <header className="dashboard-header">
        <span className="brand">HR-Counselor</span>
        <button className="icon-button" type="button" onClick={onLogout} aria-label="Выйти из аккаунта">
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
                {isLoadingCv ? (
                  <span className="profile-card__metric-value">Загрузка...</span>
                ) : currentCv && currentCv.rating ? (
                  <span className="profile-card__metric-value">{parseFloat(currentCv.rating).toFixed(1)}</span>
                ) : (
                  <span className="profile-card__metric-value">Нет данных</span>
                )}
              </div>
              <div className="profile-card__metric">
                <span className="profile-card__metric-label">XP:</span>
                {isLoadingProfile ? (
                  <span className="profile-card__metric-value">Загрузка...</span>
                ) : data && data.xp !== undefined ? (
                  <span className="profile-card__metric-value">{data.xp}</span>
                ) : userProfile && userProfile.xp !== undefined ? (
                  <span className="profile-card__metric-value">{userProfile.xp}</span>
                ) : (
                  <span className="profile-card__metric-value">0</span>
                )}
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

      <section className="cv-card">
        <div>
          <h3>Загруженное CV</h3>
          {isLoadingCv ? (
            <p className="cv-card__placeholder">Загрузка информации о CV...</p>
          ) : currentCv ? (
            <>
              <p className="cv-card__file">{currentCv.original_filename}</p>
              <p className="cv-card__time">
                Загружено: {formatMoscowTime(currentCv.uploaded_at)}
              </p>
            </>
          ) : (
            <p className="cv-card__placeholder">Загрузите CV, чтобы мы показали данные профиля.</p>
          )}
        </div>
        <div className="cv-card__actions">
          <button className="btn btn-green" type="button" onClick={onReupload} disabled={isLoadingCv}>
            {currentCv ? 'Управление CV' : 'Загрузить CV'}
          </button>
        </div>
      </section>

      <nav className="tabs">
        <button type="button" className={`tabs__btn ${activeTab === 'personal_assistant' ? 'is-active' : ''}`} onClick={() => setActiveTab('personal_assistant')}>Личный помощник</button>
        <button type="button" className={`tabs__btn ${activeTab === 'data' ? 'is-active' : ''}`} onClick={() => setActiveTab('data')}>Данные</button>
        <button type="button" className={`tabs__btn ${activeTab === 'opportunities' ? 'is-active' : ''}`} onClick={() => setActiveTab('opportunities')}>Карьерные возможности</button>
        <button type="button" className={`tabs__btn ${activeTab === 'courses' ? 'is-active' : ''}`} onClick={() => setActiveTab('courses')}>Курсы</button>
        <button type="button" className={`tabs__btn ${activeTab === 'store' ? 'is-active' : ''}`} onClick={() => setActiveTab('store')}>Магазин</button>
      </nav>

      {activeTab === 'personal_assistant' && (
        <section className="panel">
          <div className="assistant-container">
            <div className="assistant-tasks">
              <h3>Рекомендации по улучшению CV</h3>
              <div className="task-list">
                {taskSuggestions.map((task) => (
                  <div key={task.id} className={`task-item ${completedTasks.includes(task.id) ? 'task-item--completed' : ''}`}>
                    <div className="task-item__header">
                      <label className="task-item__checkbox">
                        <input 
                          type="checkbox" 
                          checked={completedTasks.includes(task.id)}
                          onChange={() => toggleTaskCompletion(task.id)}
                        />
                        <span className="task-item__title">{task.title}</span>
                      </label>
                    </div>
                    <p className="task-item__details">{task.details}</p>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="assistant-chat">
              <h3>Чат с помощником</h3>
              <div className="chat">
                <div className="chat__messages">
                  {assistantMessages.map((message, index) => (
                    <div key={index} className={`msg ${message.from === 'bot' ? 'msg--bot' : 'msg--user'}`}>
                      {message.text}
                    </div>
                  ))}
                </div>
                <div className="chat__input">
                  <input 
                    className="field__input field__input--chat" 
                    type="text" 
                    placeholder="Задайте вопрос помощнику" 
                    value={assistantInput} 
                    onChange={(e) => setAssistantInput(e.target.value)} 
                    onKeyDown={(e) => e.key === 'Enter' && sendAssistantMessage()}
                  />
                  <button className="btn btn-green" type="button" onClick={sendAssistantMessage}>
                    Отправить
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {activeTab === 'opportunities' && (
        <section className="panel">
          {isLoadingJobs ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Загружаем вакансии...</p>
            </div>
          ) : (
            <div className="jobs">
              {jobs.length > 0 ? jobs.map((job) => (
                <article key={job.id} className="job-card">
                  <h4 className="job-card__title">{job.title}</h4>
                  <p className="job-card__company">{job.department}</p>
                  <div className="job-card__meta">
                    <span className="job-card__level">{getJobLevelLabel(job.level)}</span>
                  </div>
                  <button 
                    className="btn btn-outline job-card__action" 
                    type="button"
                    onClick={() => handleJobApply(job.title)}
                  >
                    Откликнуться
                  </button>
                </article>
              )) : (
                <div className="empty-state">
                  <p>Нет доступных вакансий</p>
                </div>
              )}
            </div>
          )}
        </section>
      )}

      {activeTab === 'data' && (
        <section className="panel">
          {isLoadingCv ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Загружаем данные из CV...</p>
            </div>
          ) : !currentCv ? (
            <div className="empty-state">
              <p>Нет загруженного CV. Загрузите резюме для просмотра данных.</p>
              <button className="btn btn-green" onClick={onReupload}>Загрузить CV</button>
            </div>
          ) : (
            <>
              <div className="data-section-header">
                <h3>Данные CV</h3>
                <div className="data-section-actions">
                  {!editMode ? (
                    <button 
                      className="btn btn-purple" 
                      type="button" 
                      onClick={() => setEditMode(true)}
                    >
                      Редактировать
                    </button>
                  ) : (
                    <div className="edit-actions">
                      <button 
                        className="btn btn-green" 
                        type="button" 
                        onClick={saveChanges}
                        disabled={isSaving}
                      >
                        {isSaving ? 'Сохранение...' : 'Сохранить'}
                      </button>
                      <button 
                        className="btn btn-ghost" 
                        type="button" 
                        onClick={cancelEdit}
                        disabled={isSaving}
                      >
                        Отмена
                      </button>
                    </div>
                  )}
                </div>
              </div>
              
              {saveMessage && (
                <div className={`save-message ${saveMessage.includes('успешно') ? 'save-message--success' : 'save-message--error'}`}>
                  {saveMessage}
                </div>
              )}

              <SubCard title="Личная информация" render={() => (
                <div className="form-grid">
                  <EditableField 
                    label="Возраст" 
                    value={getFieldValue('age', 'Не указан')} 
                    onChange={(e) => handleFieldChange('age', e.target.value)} 
                    edit={editMode} 
                  />
                  <EditableField 
                    label="Опыт работы (лет)" 
                    value={getFieldValue('experience_years', '')} 
                    onChange={(e) => handleFieldChange('experience_years', e.target.value)} 
                    edit={editMode} 
                  />
                  <EditableField 
                    label="Подразделение" 
                    value={getFieldValue('department')} 
                    onChange={(e) => handleFieldChange('department', e.target.value)} 
                    edit={editMode} 
                  />
                  <EditableField 
                    label="Грейд" 
                    value={getFieldValue('grade')} 
                    onChange={(e) => handleFieldChange('grade', e.target.value)} 
                    edit={editMode} 
                  />
                  <EditableField 
                    label="Специализация" 
                    value={getFieldValue('specialization')} 
                    onChange={(e) => handleFieldChange('specialization', e.target.value)} 
                    edit={editMode} 
                  />
                </div>
              )} />

              <SubCard title="Образование" render={() => (
                <div className="form-grid">
                  <EditableField 
                    label="Образование" 
                    value={getFieldValue('education')} 
                    onChange={(e) => handleFieldChange('education', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                  <EditableField 
                    label="Дополнительное образование" 
                    value={getFieldValue('additional_education')} 
                    onChange={(e) => handleFieldChange('additional_education', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                </div>
              )} />

              <SubCard title="Текущая роль" render={() => (
                <div className="form-grid">
                  <EditableField 
                    label="Текущая должность" 
                    value={getFieldValue('current_role')} 
                    onChange={(e) => handleFieldChange('current_role', e.target.value)} 
                    edit={editMode} 
                  />
                  <EditableField 
                    label="Обязанности" 
                    value={getFieldValue('responsibilities')} 
                    onChange={(e) => handleFieldChange('responsibilities', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                </div>
              )} />

              <SubCard title="Навыки и компетенции" render={() => (
                <div className="form-grid">
                  <EditableField 
                    label="Навыки" 
                    value={getFieldValue('skills')} 
                    onChange={(e) => handleFieldChange('skills', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                  <EditableField 
                    label="Компетенции" 
                    value={getFieldValue('competencies')} 
                    onChange={(e) => handleFieldChange('competencies', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                  <EditableField 
                    label="Языки" 
                    value={getFieldValue('languages')} 
                    onChange={(e) => handleFieldChange('languages', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                </div>
              )} />

              <SubCard title="Опыт работы" render={() => (
                <div className="form-grid">
                  <EditableField 
                    label="Предыдущие места работы" 
                    value={getFieldValue('jobs')} 
                    onChange={(e) => handleFieldChange('jobs', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                </div>
              )} />

              <SubCard title="Дополнительная информация" render={() => (
                <div className="form-grid">
                  <EditableField 
                    label="Комментарии" 
                    value={getFieldValue('comments')} 
                    onChange={(e) => handleFieldChange('comments', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                  <EditableField 
                    label="Рейтинг" 
                    value={getFieldValue('rating')} 
                    onChange={(e) => handleFieldChange('rating', e.target.value)} 
                    edit={editMode} 
                  />
                  <EditableField 
                    label="Теги" 
                    value={getFieldValue('tags')} 
                    onChange={(e) => handleFieldChange('tags', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                  <EditableField 
                    label="Карьерный путь" 
                    value={getFieldValue('career_path')} 
                    onChange={(e) => handleFieldChange('career_path', e.target.value)} 
                    edit={editMode} 
                    multiline
                  />
                </div>
              )} />

              <SubCard title="Статус анализа" render={() => (
                <div className="form-grid">
                  <EditableField 
                    label="Статус обработки" 
                    value={getFieldValue('analysis_status', 'Ожидает анализа')} 
                    onChange={(e) => handleFieldChange('analysis_status', e.target.value)} 
                    edit={editMode} 
                  />
                </div>
              )} />
            </>
          )}
        </section>
      )}

      {activeTab === 'courses' && (
        <section className="panel">
          <h3>Рекомендуемые курсы</h3>
          {isLoadingCourses ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Загружаем курсы...</p>
            </div>
          ) : courses.length === 0 ? (
            <div className="empty-state">
              <p>Курсы не найдены</p>
            </div>
          ) : (
            <div className="hr-dashboard__grid">
              {courses.map((c) => {
                const accent = {
                  'HR': '#5eead4',
                  'Frontend': '#a855f7',
                  'Data': '#f97316',
                  'IT': '#38bdf8',
                  'Marketing': '#f59e0b',
                  'Design': '#ec4899',
                }[c.direction] || '#bef264'

                const levelLabels = {
                  'beginner': 'Начальный',
                  'intermediate': 'Средний', 
                  'advanced': 'Продвинутый'
                }
                
                return (
                  <article key={c.id} className="folder-card course-card" style={{ '--accent': accent }}>
                    <div className="folder-card__icon">
                      <span className="folder-card__badge">{levelLabels[c.level] || c.level}</span>
                    </div>
                    <div className="folder-card__body">
                      <h2>{c.title}</h2>
                      <p>{c.direction}</p>
                      <span className="folder-card__meta">{c.duration_hours} академических часов</span>
                      {c.description && (
                        <div className="course-description">{c.description}</div>
                      )}
                      
                    </div>
                    <button 
                      className={`folder-card__action ${isEnrolledInCourse(c.id) ? 'folder-card__action--enrolled' : ''}`}
                      type="button" 
                      onClick={() => handleCourseClick(c)}
                    >
                      {isEnrolledInCourse(c.id) ? 'Записаны' : 'Выбрать курс'}
                    </button>
                  </article>
                )
              })}
            </div>
          )}
          <h3>Роадмап</h3>
          <ul className="list">
            {roadmap.map((r, i) => (
              <li key={i} className="list__item">{r}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Модальное окно с подробной информацией о курсе */}
      {selectedCourse && (
        <div className="modal-overlay" onClick={handleCloseCourseModal}>
          <div className="modal-content course-modal" onClick={(e) => e.stopPropagation()}>
            <button className="icon-button icon-button--ghost modal-close" onClick={handleCloseCourseModal}>
              <CloseIcon className="icon icon--small" />
            </button>
            
            {isLoadingCourseDetails ? (
              <div className="loading-state">
                <div className="loading-spinner"></div>
                <p>Загружаем информацию о курсе...</p>
              </div>
            ) : (
              <>
                <header className="course-modal__header">
                  <h2>{selectedCourse.title}</h2>
                  <div className="course-modal__meta">
                    <span className={`course-badge course-badge--${selectedCourse.level}`}>
                      {selectedCourse.level === 'beginner' && 'Начальный'}
                      {selectedCourse.level === 'intermediate' && 'Средний'}
                      {selectedCourse.level === 'advanced' && 'Продвинутый'}
                    </span>
                    <span className="course-direction">{selectedCourse.direction}</span>
                  </div>
                </header>

                <div className="course-modal__body">
                  <div className="course-info">
                    <div className="course-info__item">
                      <span className="course-info__label">Длительность:</span>
                      <span className="course-info__value">{selectedCourse.duration_hours} академических часов</span>
                    </div>
                    {selectedCourse.created_at && (
                      <div className="course-info__item">
                        <span className="course-info__label">Дата создания:</span>
                        <span className="course-info__value">
                          {formatMoscowDate(selectedCourse.created_at)}
                        </span>
                      </div>
                    )}
                  </div>

                  {selectedCourse.description && (
                    <div className="course-description-full">
                      <h3>Описание курса</h3>
                      <p>{selectedCourse.description}</p>
                    </div>
                  )}

                  {enrollmentMessage && (
                    <div className={`enrollment-message ${enrollmentMessage.includes('успешно') ? 'enrollment-message--success' : 'enrollment-message--error'}`}>
                      {enrollmentMessage}
                    </div>
                  )}
                </div>

                <footer className="course-modal__footer">
                  <button 
                    className="btn btn-ghost" 
                    onClick={handleCloseCourseModal}
                    disabled={isEnrolling}
                  >
                    Закрыть
                  </button>
                  {isEnrolledInCourse(selectedCourse.id) ? (
                    <button 
                      className="btn btn-green" 
                      disabled={true}
                    >
                      Вы уже записаны на курс
                    </button>
                  ) : (
                    <button 
                      className="btn btn-green" 
                      onClick={handleEnrollInCourse}
                      disabled={isEnrolling}
                    >
                      {isEnrolling ? 'Записываемся...' : 'Записаться на курс'}
                    </button>
                  )}
                </footer>
              </>
            )}
          </div>
        </div>
      )}

      {activeTab === 'store' && (
        <section className="panel">
          <h3>Корпоративный магазин</h3>
          <div className="store-grid">
            <div className="store-item">
              <h4>Носки с логотипом</h4>
              <p className="store-item-description">Удобные носки с корпоративным логотипом компании</p>
              <div className="store-item-price">500 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Носки с логотипом', '500 XP')}
                disabled={!hasEnoughXP(500)}
              >
                {hasEnoughXP(500) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
            
            <div className="store-item">
              <h4>Футболка компании</h4>
              <p className="store-item-description">Качественная футболка с фирменным дизайном</p>
              <div className="store-item-price">1200 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Футболка компании', '1200 XP')}
              disabled={!hasEnoughXP(1200)}
              >
                {hasEnoughXP(1200) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
            
            <div className="store-item">
              <h4>Кружка с логотипом</h4>
              <p className="store-item-description">Керамическая кружка для кофе и чая</p>
              <div className="store-item-price">800 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Кружка с логотипом', '800 XP')}
              disabled={!hasEnoughXP(800)}
              >
                {hasEnoughXP(800) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
            
            <div className="store-item">
              <h4>Оплата питания</h4>
              <p className="store-item-description">Пополнение баланса для оплаты в корпоративной столовой</p>
              <div className="store-item-price">от 1000 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Оплата питания', 'от 1000 XP')}
              disabled={!hasEnoughXP(1000)}
              >
                {hasEnoughXP(1000) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
            
            <div className="store-item">
              <h4>Сертификат Wildberries</h4>
              <p className="store-item-description">Подарочный сертификат на покупки в Wildberries</p>
              <div className="store-item-price">3000 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Сертификат Wildberries', '3000 XP')}
              disabled={!hasEnoughXP(3000)}
              >
                {hasEnoughXP(3000) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
            
            <div className="store-item">
              <h4>Сертификат Ozon</h4>
              <p className="store-item-description">Подарочный сертификат на покупки в Ozon</p>
              <div className="store-item-price">2500 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Сертификат Ozon', '2500 XP')}
              disabled={!hasEnoughXP(2500)}
              >
                {hasEnoughXP(2500) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
            
            <div className="store-item">
              <h4>Сертификат Пятёрочка</h4>
              <p className="store-item-description">Подарочная карта для покупок продуктов</p>
              <div className="store-item-price">2000 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Сертификат Пятёрочка', '2000 XP')}
              disabled={!hasEnoughXP(2000)}
              >
                {hasEnoughXP(2000) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
            
            <div className="store-item">
              <h4>Сертификат развлечений</h4>
              <p className="store-item-description">Сертификат на посещение кинотеатров и развлекательных центров</p>
              <div className="store-item-price">1500 XP</div>
              <button 
                className="btn btn-primary" 
                onClick={() => handleStorePurchase('Сертификат развлечений', '1500 XP')}
              disabled={!hasEnoughXP(1500)}
              >
                {hasEnoughXP(1500) ? 'Заказать' : 'Недостаточно XP'}
              </button>
            </div>
          </div>
        </section>
      )}

      {/* Модальное окно подтверждения покупки */}
      {purchaseModalOpen && (
        <div className="modal-overlay" onClick={() => setPurchaseModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button 
              className="icon-button icon-button--ghost modal-close" 
              onClick={() => setPurchaseModalOpen(false)}
            >
              <CloseIcon className="icon icon--small" />
            </button>
            <div className="modal-body">
              <h3>Покупка совершена!</h3>
              <p>Вы успешно приобрели товар "{purchaseDetails?.itemName}"</p>
              <p>Списано {purchaseDetails?.price} XP</p>
            </div>
            <div className="modal-footer">
              <button 
                className="btn btn-green" 
                onClick={() => setPurchaseModalOpen(false)}
              >
                Закрыть
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function EditableField({ label, value, onChange, edit, multiline }) {
  return (
    <label className="field">
      <span className="field__label">{label}</span>
      {edit ? (
        multiline ? (
          <textarea className="field__input" rows={4} value={value} onChange={onChange} />
        ) : (
          <input className="field__input" type="text" value={value} onChange={onChange} />
        )
      ) : (
        <span className="field__text">{value || '—'}</span>
      )}
    </label>
  )
}

function HrDashboard({ onLogout }) {
  const [hrName, setHrName] = React.useState('HR Пользователь')
  const [isLoadingProfile, setIsLoadingProfile] = React.useState(true)
  const [token] = React.useState(localStorage.getItem('token'))
  const [activeTab, setActiveTab] = React.useState('search')
  const [expandedFolders, setExpandedFolders] = React.useState({})
  const [activeFolder, setActiveFolder] = React.useState(null)
  const [folders, setFolders] = React.useState([])
  const [isLoadingFolders, setIsLoadingFolders] = React.useState(false)
  
  // Состояния для создания папки
  const [showCreateFolderModal, setShowCreateFolderModal] = React.useState(false)
  const [isCreatingFolder, setIsCreatingFolder] = React.useState(false)
  const [createFolderError, setCreateFolderError] = React.useState(null)
  const [newFolder, setNewFolder] = React.useState({
    name: '',
    description: '',
    job_id: ''
  })
  const [jobs, setJobs] = React.useState([])
  const [isLoadingJobs, setIsLoadingJobs] = React.useState(false)

  // Состояния для детальной информации о папке
  const [folderDetails, setFolderDetails] = React.useState(null)
  const [isLoadingFolderDetails, setIsLoadingFolderDetails] = React.useState(false)

  // Загружаем профиль HR при монтировании компонента
  React.useEffect(() => {
    if (token) {
      loadHrProfile();
      loadFolders();
      loadJobs();
    }
  }, [token]);

  const loadHrProfile = async () => {
    try {
      setIsLoadingProfile(true);
      const profile = await api.getUserProfile(token);
      setHrName(profile.full_name || profile.name || profile.email || 'HR Пользователь');
    } catch (error) {
      console.error('Ошибка загрузки профиля HR:', error);
      setHrName('HR Пользователь');
    } finally {
      setIsLoadingProfile(false);
    }
  };

  const loadFolders = async () => {
    try {
      setIsLoadingFolders(true);
      const response = await api.getMyFolders(token);
      setFolders(response.folders || []);
    } catch (error) {
      console.error('Ошибка загрузки папок:', error);
      // В случае ошибки используем статические данные
      setFolders(hrFolders);
    } finally {
      setIsLoadingFolders(false);
    }
  };

  const loadJobs = async () => {
    try {
      setIsLoadingJobs(true);
      const response = await api.getJobs(token);
      setJobs(response.jobs || []);
    } catch (error) {
      console.error('Ошибка загрузки вакансий:', error);
      setJobs([]);
    } finally {
      setIsLoadingJobs(false);
    }
  };

  // Функции для создания папки
  const openCreateFolderModal = () => {
    setShowCreateFolderModal(true);
    setCreateFolderError(null);
    setNewFolder({
      name: '',
      description: '',
      job_id: ''
    });
  };

  const closeCreateFolderModal = () => {
    setShowCreateFolderModal(false);
    setCreateFolderError(null);
    setNewFolder({
      name: '',
      description: '',
      job_id: ''
    });
  };

  const handleCreateFolder = async () => {
    try {
      setIsCreatingFolder(true);
      setCreateFolderError(null);

      // Валидация
      if (!newFolder.name.trim()) {
        setCreateFolderError('Название папки обязательно');
        return;
      }
      if (!newFolder.job_id) {
        setCreateFolderError('Выберите вакансию');
        return;
      }

      // Создаем папку
      const folder = await api.createFolder(token, newFolder);
      
      // Обновляем список папок
      await loadFolders();
      
      // Закрываем модальное окно
      closeCreateFolderModal();
      
    } catch (err) {
      console.error('Ошибка создания папки:', err);
      setCreateFolderError(err.message || 'Ошибка при создании папки');
    } finally {
      setIsCreatingFolder(false);
    }
  };

  const [filters, setFilters] = React.useState({
    ageMin: 21,
    ageMax: 45,
    gender: '',
    expMin: 0,
    expMax: 10,
    languages: '',
    education: '',
    specialty: '',
    department: '',
    level: '',
    skills: '',
    format: '',
    uploaded: '',
    ratingMin: 0,
  })

  const [messages, setMessages] = React.useState([
    { from: 'bot', text: 'Привет! Опишите кандидата или выберите фильтры слева.' },
  ])
  const [chatInput, setChatInput] = React.useState('')
  const [showCvModal, setShowCvModal] = React.useState(false)
  const [isSearching, setIsSearching] = React.useState(false)
  const [searchResults, setSearchResults] = React.useState([])

  const allCvs = React.useMemo(
    () => folders.flatMap((f) => (f.files || []).map((file) => ({ ...file, folder: f.name }))),
    [folders]
  )

  const sendQuery = async () => {
    const text = chatInput.trim()
    if (!text) return
    
    setMessages((prev) => [...prev, { from: 'user', text }])
    setChatInput('')
    setIsSearching(true)
    
    // Показываем сообщение о загрузке
    setMessages((prev) => [...prev, { from: 'bot', text: 'Ищу подходящих сотрудников...' }])
    
    try {
      // Подготавливаем данные для запроса
      const searchData = {
        query: text,
        filters: {
          department: filters.department || undefined,
          experience_years_min: filters.expMin,
          experience_years_max: filters.expMax,
          skills: filters.skills ? filters.skills.split(',').map(s => s.trim()).filter(s => s) : 
                  filters.specialty ? filters.specialty.split(',').map(s => s.trim()).filter(s => s) : [],
          level: filters.level || undefined,
          languages: filters.languages ? filters.languages.split(',').map(l => l.trim()).filter(l => l) : [],
          education_level: filters.education || undefined,
          age_min: filters.ageMin,
          age_max: filters.ageMax
        }
      }
      
      // Удаляем undefined значения из filters
      const cleanFilters = Object.fromEntries(
        Object.entries(searchData.filters).filter(([_, v]) => v !== undefined && v !== '' && (!Array.isArray(v) || v.length > 0))
      )
      searchData.filters = cleanFilters
      
      const results = await api.searchEmployees(token, searchData)
      setSearchResults(results.employees || [])
      
      // Обновляем сообщения с результатами
      setMessages((prev) => {
        const newMessages = [...prev]
        // Убираем сообщение о загрузке
        newMessages.pop()
        
        if (results.employees && results.employees.length > 0) {
          // Добавляем сообщение с тегами, если они есть
          if (results.generated_tags && results.generated_tags.length > 0) {
            newMessages.push({
              from: 'bot',
              text: `Определил ключевые навыки: ${results.generated_tags.join(', ')}`
            })
          }
          
          newMessages.push({
            from: 'bot',
            text: `Найдено ${results.employees.length} подходящих сотрудников${results.total_found && results.total_found !== results.employees.length ? ` из ${results.total_found} общего количества` : ''}. Открыть список?`,
            action: 'open'
          })
        } else {
          newMessages.push({
            from: 'bot',
            text: 'К сожалению, не удалось найти сотрудников по вашему запросу. Попробуйте изменить критерии поиска.'
          })
        }
        
        return newMessages
      })
      
    } catch (error) {
      console.error('Ошибка поиска сотрудников:', error)
      
      // Обновляем сообщения с ошибкой
      setMessages((prev) => {
        const newMessages = [...prev]
        // Убираем сообщение о загрузке
        newMessages.pop()
        newMessages.push({
          from: 'bot',
          text: `Произошла ошибка при поиске: ${error.message || 'Неизвестная ошибка'}. Попробуйте еще раз.`
        })
        return newMessages
      })
    } finally {
      setIsSearching(false)
    }
  }

  const searchByFilters = async () => {
    setIsSearching(true)
    
    // Добавляем сообщение о поиске по фильтрам
    setMessages((prev) => [...prev, 
      { from: 'user', text: 'Поиск по заданным фильтрам' },
      { from: 'bot', text: 'Ищу сотрудников по заданным фильтрам...' }
    ])
    
    try {
      // Подготавливаем данные для запроса
      const searchData = {
        query: "Поиск по фильтрам",
        filters: {
          department: filters.department || undefined,
          experience_years_min: filters.expMin,
          experience_years_max: filters.expMax,
          skills: filters.skills ? filters.skills.split(',').map(s => s.trim()).filter(s => s) : 
                  filters.specialty ? filters.specialty.split(',').map(s => s.trim()).filter(s => s) : [],
          level: filters.level || undefined,
          languages: filters.languages ? filters.languages.split(',').map(l => l.trim()).filter(l => l) : [],
          education_level: filters.education || undefined,
          age_min: filters.ageMin,
          age_max: filters.ageMax
        }
      }
      
      // Удаляем undefined значения из filters
      const cleanFilters = Object.fromEntries(
        Object.entries(searchData.filters).filter(([_, v]) => v !== undefined && v !== '' && (!Array.isArray(v) || v.length > 0))
      )
      searchData.filters = cleanFilters
      
      const results = await api.searchEmployees(token, searchData)
      setSearchResults(results.employees || [])
      
      // Обновляем сообщения с результатами
      setMessages((prev) => {
        const newMessages = [...prev]
        // Убираем сообщение о загрузке
        newMessages.pop()
        
        if (results.employees && results.employees.length > 0) {
          // Добавляем сообщение с тегами, если они есть
          if (results.generated_tags && results.generated_tags.length > 0) {
            newMessages.push({
              from: 'bot',
              text: `Определил ключевые навыки из фильтров: ${results.generated_tags.join(', ')}`
            })
          }
          
          newMessages.push({
            from: 'bot',
            text: `Найдено ${results.employees.length} подходящих сотрудников по заданным фильтрам${results.total_found && results.total_found !== results.employees.length ? ` из ${results.total_found} общего количества` : ''}. Открыть список?`,
            action: 'open'
          })
        } else {
          newMessages.push({
            from: 'bot',
            text: 'По заданным фильтрам сотрудники не найдены. Попробуйте изменить критерии поиска.'
          })
        }
        
        return newMessages
      })
      
    } catch (error) {
      console.error('Ошибка поиска сотрудников:', error)
      
      // Обновляем сообщения с ошибкой
      setMessages((prev) => {
        const newMessages = [...prev]
        // Убираем сообщение о загрузке
        newMessages.pop()
        newMessages.push({
          from: 'bot',
          text: `Произошла ошибка при поиске: ${error.message || 'Неизвестная ошибка'}. Попробуйте еще раз.`
        })
        return newMessages
      })
    } finally {
      setIsSearching(false)
    }
  }

  const onBotAction = (msg) => {
    if (msg.action === 'open') {
      setShowCvModal(true)
    }
  }

  const update = (key) => (e) => setFilters((p) => ({ ...p, [key]: e.target.value }))
  
  // Функции для работы с модальным окном папки
  const openFolderModal = async (folder) => {
    setActiveFolder(folder);
    setIsLoadingFolderDetails(true);
    try {
      const details = await api.getFolderById(token, folder.id);
      setFolderDetails(details);
    } catch (error) {
      console.error('Ошибка загрузки деталей папки:', error);
      setFolderDetails(folder); // Используем базовую информацию в случае ошибки
    } finally {
      setIsLoadingFolderDetails(false);
    }
  };
  
  const closeFolderModal = () => {
    setActiveFolder(null);
    setFolderDetails(null);
  };

  // Функция для удаления папки
  const handleDeleteFolder = async (folderId) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту папку? Все файлы в ней будут потеряны.')) {
      return;
    }
    
    try {
      await api.deleteFolder(token, folderId);
      
      // Сначала оптимистично удаляем из локального состояния
      setFolders(prev => prev.filter(folder => folder.id !== folderId));
      
      // Затем перезагружаем список папок с сервера для синхронизации
      await loadFolders();
      
      // Закрываем модальное окно
      closeFolderModal();
      
    } catch (error) {
      console.error('Ошибка удаления папки:', error);
      alert('Ошибка при удалении папки: ' + (error.message || 'Неизвестная ошибка'));
      
      // В случае ошибки перезагружаем список для восстановления состояния
      await loadFolders();
    }
  };

  return (
    <div className="hr-dashboard">
      <header className="dashboard-header">
        <span className="brand">HR-Counselor</span>
        <button className="btn btn-ghost btn-small" type="button" onClick={onLogout}>Выйти</button>
      </header>

      <div className="employee-dashboard__top">
        <div className="profile-card">
          <div className="profile-card__avatar">
            {isLoadingProfile ? '...' : hrName.slice(0, 1)}
          </div>
          <div>
            <h2 className="profile-card__name">
              {isLoadingProfile ? 'Загрузка...' : hrName}
            </h2>
            <div className="profile-card__metrics">
              <div className="profile-card__metric">
                <span className="profile-card__metric-label">Роль:</span>
                <span className="profile-card__metric-value">HR</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <nav className="tabs">
        <button type="button" className={`tabs__btn ${activeTab === 'search' ? 'is-active' : ''}`} onClick={() => setActiveTab('search')}>Поиск сотрудников</button>
        <button type="button" className={`tabs__btn ${activeTab === 'vacancies' ? 'is-active' : ''}`} onClick={() => setActiveTab('vacancies')}>Вакансии компании</button>
        <button type="button" className={`tabs__btn ${activeTab === 'folders' ? 'is-active' : ''}`} onClick={() => setActiveTab('folders')}>Папки с CV</button>
      </nav>

      {activeTab === 'search' && (
        <section className="panel">
          <div className="filters" style={{marginBottom: 24}}>
            <h3>Базовые фильтры</h3>
            <div className="form-grid">
              <label className="field"><span className="field__label">Возраст, от</span><input className="field__input" type="number" value={filters.ageMin} onChange={update('ageMin')} /></label>
              <label className="field"><span className="field__label">Возраст, до</span><input className="field__input" type="number" value={filters.ageMax} onChange={update('ageMax')} /></label>
              <label className="field"><span className="field__label">Пол</span><input className="field__input" type="text" placeholder="опционально" value={filters.gender} onChange={update('gender')} /></label>
              <label className="field"><span className="field__label">Опыт, от (лет)</span><input className="field__input" type="number" value={filters.expMin} onChange={update('expMin')} /></label>
              <label className="field"><span className="field__label">Опыт, до (лет)</span><input className="field__input" type="number" value={filters.expMax} onChange={update('expMax')} /></label>
              <label className="field"><span className="field__label">Языки</span><input className="field__input" type="text" placeholder="English B2+, ..." value={filters.languages} onChange={update('languages')} /></label>
              <label className="field"><span className="field__label">Образование</span><input className="field__input" type="text" placeholder="бакалавр/магистр/PhD" value={filters.education} onChange={update('education')} /></label>
              <label className="field"><span className="field__label">Специальность</span><input className="field__input" type="text" value={filters.specialty} onChange={update('specialty')} /></label>
              <label className="field"><span className="field__label">Департамент</span><input className="field__input" type="text" placeholder="IT, HR, Marketing..." value={filters.department} onChange={update('department')} /></label>
              <label className="field"><span className="field__label">Уровень</span><input className="field__input" type="text" placeholder="Junior, Middle, Senior..." value={filters.level} onChange={update('level')} /></label>
              <label className="field"><span className="field__label">Навыки</span><input className="field__input" type="text" placeholder="Python, React, SQL..." value={filters.skills} onChange={update('skills')} /></label>
              <label className="field"><span className="field__label">Формат работы</span><input className="field__input" type="text" placeholder="офис/гибрид/удалёнка" value={filters.format} onChange={update('format')} /></label>
              <label className="field"><span className="field__label">Дата загрузки</span><input className="field__input" type="date" value={filters.uploaded} onChange={update('uploaded')} /></label>
              <label className="field"><span className="field__label">Мин. рейтинг</span><input className="field__input" type="number" value={filters.ratingMin} onChange={update('ratingMin')} /></label>
            </div>
            <div style={{marginTop: '1rem'}}>
              <button 
                className="btn btn-green" 
                type="button" 
                onClick={() => searchByFilters()}
                disabled={isSearching}
              >
                {isSearching ? 'Поиск...' : 'Найти по фильтрам'}
              </button>
            </div>
          </div>
          <section className="chat">
            <div className="chat__messages">
              {messages.map((m, i) => (
                <div key={i} className={`msg ${m.from === 'bot' ? 'msg--bot' : 'msg--user'}`} onClick={() => onBotAction(m)}>
                  {m.text}
                </div>
              ))}
            </div>
            <div className="chat__input">
              <input className="field__input" type="text" placeholder="Опишите требования..." value={chatInput} onChange={(e) => setChatInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && !isSearching && sendQuery()} disabled={isSearching} />
              <button className="btn btn-green" type="button" onClick={sendQuery} disabled={isSearching || !chatInput.trim()}>
                {isSearching ? 'Поиск...' : 'Отправить'}
              </button>
            </div>
          </section>
        </section>
      )}

      {activeTab === 'vacancies' && <VacanciesTab />}

      {activeTab === 'folders' && (
        <section className="panel">
          <div className="panel__header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h3>Папки с CV</h3>
            <button className="btn btn-purple" type="button" onClick={openCreateFolderModal}>
              Создать папку
            </button>
          </div>
          
          {isLoadingFolders ? (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
              <p>Загрузка папок...</p>
            </div>
          ) : (
            <div 
              className="hr-dashboard__grid" 
              style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
                gap: '1.5rem',
                maxWidth: '900px',
                margin: '0 auto'
              }}
            >
              {folders.map((folder) => (
                <article key={folder.id} className="folder-card" style={{ '--accent': '#5eead4' }}>
                  <div className="folder-card__icon"><FolderIcon className="icon" /></div>
                  <div className="folder-card__body">
                    <h2>{folder.name}</h2>
                    <p>{folder.candidates_count || 0} кандидатов</p>
                    {folder.description && <p className="folder-description">{folder.description}</p>}
                    <span>Создано {formatMoscowDate(folder.created_at)}</span>
                  </div>
                  <button className="folder-card__action" type="button" onClick={() => openFolderModal(folder)}>
                    Открыть папку
                  </button>
                </article>
              ))}
              {folders.length === 0 && (
                <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '3rem' }}>
                  <FolderIcon className="icon" style={{ fontSize: '3rem', color: '#9ca3af', marginBottom: '1rem' }} />
                  <p style={{ fontSize: '1.125rem', color: '#6b7280', marginBottom: '1rem' }}>У вас пока нет папок с CV</p>
                </div>
              )}
            </div>
          )}
          
          {activeFolder && (
            <FolderFilesModal 
              folder={activeFolder} 
              folderDetails={folderDetails}
              isLoadingDetails={isLoadingFolderDetails}
              onClose={closeFolderModal}
              onDelete={handleDeleteFolder}
            />
          )}
          
          {showCreateFolderModal && (
            <CreateFolderModal 
              jobs={jobs}
              isLoadingJobs={isLoadingJobs}
              newFolder={newFolder}
              setNewFolder={setNewFolder}
              isCreating={isCreatingFolder}
              error={createFolderError}
              onSubmit={handleCreateFolder}
              onClose={closeCreateFolderModal}
            />
          )}
        </section>
      )}



      {showCvModal && (
        <CvResultsModal list={searchResults.length > 0 ? searchResults : allCvs} onClose={() => setShowCvModal(false)} />
      )}
    </div>
  )
}

function VacanciesTab() {
  const [vacancies, setVacancies] = React.useState([])
  const [isLoading, setIsLoading] = React.useState(true)
  const [error, setError] = React.useState(null)
  const [selectedJob, setSelectedJob] = React.useState(null)
  const [showJobModal, setShowJobModal] = React.useState(false)
  const [token] = React.useState(localStorage.getItem('token'))
  
  // Состояния для создания новой вакансии
  const [isCreating, setIsCreating] = React.useState(false)
  const [createError, setCreateError] = React.useState(null)
  const [createSuccess, setCreateSuccess] = React.useState('')
  const [isFormExpanded, setIsFormExpanded] = React.useState(false)
  const [newJob, setNewJob] = React.useState({
    title: '',
    department: '',
    level: 'intern',
    employment_type: 'full_time',
    location: '',
    remote_available: false,
    description: '',
    requirements: '',
    responsibilities: '',
    required_skills: [],
    min_experience_years: 0,
    max_experience_years: 0,
    average_salary: 0,
    salary_currency: 'RUB'
  })
  
  // Загружаем вакансии при монтировании компонента
  React.useEffect(() => {
    if (token) {
      loadJobs();
    }
  }, [token]);

  const loadJobs = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.getJobs(token);
      setVacancies(data.jobs || []);
    } catch (err) {
      console.error('Ошибка загрузки вакансий:', err);
      setError(err.message || 'Ошибка при загрузке вакансий');
    } finally {
      setIsLoading(false);
    }
  };

  const handleJobClick = (job) => {
    setSelectedJob(job);
    setShowJobModal(true);
  };

  const closeJobModal = () => {
    setShowJobModal(false);
    setSelectedJob(null);
  };

  // Функции для создания новой вакансии
  const handleInputChange = (field, value) => {
    setNewJob(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSkillsChange = (value) => {
    // Разбиваем строку навыков по запятым и убираем лишние пробелы
    const skillsArray = value.split(',').map(skill => skill.trim()).filter(skill => skill.length > 0);
    setNewJob(prev => ({
      ...prev,
      required_skills: skillsArray
    }));
  };

  const handleCreateJob = async () => {
    try {
      setIsCreating(true);
      setCreateError(null);
      setCreateSuccess('');

      // Валидация обязательных полей
      if (!newJob.title.trim()) {
        setCreateError('Название вакансии обязательно');
        return;
      }
      if (!newJob.department.trim()) {
        setCreateError('Отдел обязателен');
        return;
      }

      // Создаем вакансию
      await api.createJob(token, newJob);
      
      // Сбрасываем форму
      setNewJob({
        title: '',
        department: '',
        level: 'intern',
        employment_type: 'full_time',
        location: '',
        remote_available: false,
        description: '',
        requirements: '',
        responsibilities: '',
        required_skills: [],
        min_experience_years: 0,
        max_experience_years: 0,
        average_salary: 0,
        salary_currency: 'RUB'
      });

      setCreateSuccess('Вакансия успешно создана!');
      
      // Перезагружаем список вакансий
      await loadJobs();
      
      // Убираем сообщение об успехе через 3 секунды
      setTimeout(() => setCreateSuccess(''), 3000);
      
    } catch (err) {
      console.error('Ошибка создания вакансии:', err);
      setCreateError(err.message || 'Ошибка при создании вакансии');
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteJob = async (jobId) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту вакансию? Это действие нельзя отменить.')) {
      return;
    }

    try {
      await api.deleteJob(token, jobId);
      
      // Закрываем модальное окно
      closeJobModal();
      
      // Перезагружаем список вакансий
      await loadJobs();
      
    } catch (err) {
      console.error('Ошибка удаления вакансии:', err);
      alert(err.message || 'Ошибка при удалении вакансии');
    }
  };

  const formatSalary = (salary, currency) => {
    if (!salary) return 'Не указана';
    return `${salary.toLocaleString()} ${currency || 'руб.'}`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Не указана';
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: 'long',
      year: 'numeric'
    });
  };

  const getStatusText = (status) => {
    const statusMap = {
      'active': 'Активна',
      'paused': 'Приостановлена',
      'closed': 'Закрыта'
    };
    return statusMap[status] || status;
  };

  const getLevelText = (level) => {
    const levelMap = {
      'intern': 'Стажер',
      'junior': 'Junior',
      'middle': 'Middle',
      'senior': 'Senior',
      'lead': 'Lead'
    };
    return levelMap[level] || level;
  };

  const getEmploymentTypeText = (type) => {
    const typeMap = {
      'full_time': 'Полная занятость',
      'part_time': 'Частичная занятость',
      'contract': 'Контракт',
      'internship': 'Стажировка'
    };
    return typeMap[type] || type;
  };

  if (isLoading) {
    return (
      <section className="panel">
        <div className="panel__header"><h3>Свободные вакансии</h3></div>
        <div style={{ padding: 24, textAlign: 'center' }}>Загрузка вакансий...</div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="panel">
        <div className="panel__header"><h3>Свободные вакансии</h3></div>
        <div style={{ padding: 24, textAlign: 'center', color: '#ef4444' }}>
          Ошибка: {error}
          <br />
          <button 
            className="btn btn-ghost" 
            style={{ marginTop: 16 }} 
            onClick={loadJobs}
          >
            Попробовать снова
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="panel__header">
        <h3>Свободные вакансии</h3>
      </div>

      {/* Форма создания новой вакансии */}
      <div className={`job-create-form ${isFormExpanded ? 'job-create-form--expanded' : 'job-create-form--collapsed'}`}>
        <div 
          className="job-create-form__header"
          onClick={() => setIsFormExpanded(!isFormExpanded)}
        >
          <h4>Создать новую вакансию</h4>
          <span className={`job-create-form__icon ${isFormExpanded ? 'job-create-form__icon--expanded' : ''}`}>
            ▼
          </span>
        </div>
        
        {isFormExpanded && (
          <div className="job-create-form__content">
            <div className="form-grid form-grid--wide">
              <label className="field">
                <span className="field__label">Название вакансии *</span>
                <input 
                  className="field__input" 
                  type="text" 
                  value={newJob.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  placeholder="Frontend Developer"
                />
              </label>
              
              <label className="field">
                <span className="field__label">Отдел *</span>
                <input 
                  className="field__input" 
                  type="text" 
                  value={newJob.department}
                  onChange={(e) => handleInputChange('department', e.target.value)}
                  placeholder="IT"
                />
              </label>
              
              <label className="field">
                <span className="field__label">Уровень</span>
                <select 
                  className="field__input" 
                  value={newJob.level}
                  onChange={(e) => handleInputChange('level', e.target.value)}
                >
                  <option value="intern">Стажер</option>
                  <option value="junior">Junior</option>
                  <option value="middle">Middle</option>
                  <option value="senior">Senior</option>
                  <option value="lead">Lead</option>
                </select>
              </label>
              
              <label className="field">
                <span className="field__label">Тип занятости</span>
                <select 
                  className="field__input" 
                  value={newJob.employment_type}
                  onChange={(e) => handleInputChange('employment_type', e.target.value)}
                >
                  <option value="full_time">Полная занятость</option>
                  <option value="part_time">Частичная занятость</option>
                  <option value="contract">Контракт</option>
                  <option value="internship">Стажировка</option>
                </select>
              </label>
              
              <label className="field">
                <span className="field__label">Локация</span>
                <input 
                  className="field__input" 
                  type="text" 
                  value={newJob.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  placeholder="Казань"
                />
              </label>
              
              <label className="field field--checkbox">
                <input 
                  type="checkbox" 
                  checked={newJob.remote_available}
                  onChange={(e) => handleInputChange('remote_available', e.target.checked)}
                />
                <span className="field__label">Возможна удаленная работа</span>
              </label>
              
              <label className="field">
                <span className="field__label">Мин. опыт (лет)</span>
                <input 
                  className="field__input" 
                  type="number" 
                  min="0"
                  value={newJob.min_experience_years}
                  onChange={(e) => handleInputChange('min_experience_years', parseInt(e.target.value) || 0)}
                />
              </label>
              
              <label className="field">
                <span className="field__label">Макс. опыт (лет)</span>
                <input 
                  className="field__input" 
                  type="number" 
                  min="0"
                  value={newJob.max_experience_years}
                  onChange={(e) => handleInputChange('max_experience_years', parseInt(e.target.value) || 0)}
                />
              </label>
              
              <label className="field">
                <span className="field__label">Зарплата</span>
                <input 
                  className="field__input" 
                  type="number" 
                  min="0"
                  value={newJob.average_salary}
                  onChange={(e) => handleInputChange('average_salary', parseInt(e.target.value) || 0)}
                  placeholder="0"
                />
              </label>
              
              <label className="field">
                <span className="field__label">Валюта</span>
                <select 
                  className="field__input" 
                  value={newJob.salary_currency}
                  onChange={(e) => handleInputChange('salary_currency', e.target.value)}
                >
                  <option value="RUB">RUB</option>
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                </select>
              </label>
            </div>

            <div className="form-grid form-grid--full">
              <label className="field">
                <span className="field__label">Описание</span>
                <textarea 
                  className="field__input field__input--textarea" 
                  rows="3"
                  value={newJob.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  placeholder="Описание вакансии..."
                />
              </label>
              
              <label className="field">
                <span className="field__label">Требования</span>
                <textarea 
                  className="field__input field__input--textarea" 
                  rows="3"
                  value={newJob.requirements}
                  onChange={(e) => handleInputChange('requirements', e.target.value)}
                  placeholder="Требования к кандидату..."
                />
              </label>
              
              <label className="field">
                <span className="field__label">Обязанности</span>
                <textarea 
                  className="field__input field__input--textarea" 
                  rows="3"
                  value={newJob.responsibilities}
                  onChange={(e) => handleInputChange('responsibilities', e.target.value)}
                  placeholder="Обязанности..."
                />
              </label>
              
              <label className="field">
                <span className="field__label">Необходимые навыки</span>
                <input 
                  className="field__input" 
                  type="text" 
                  value={newJob.required_skills.join(', ')}
                  onChange={(e) => handleSkillsChange(e.target.value)}
                  placeholder="React, JavaScript, HTML, CSS (через запятую)"
                />
              </label>
            </div>

            {createError && (
              <div className="auth__error" style={{ marginTop: 16 }}>
                {createError}
              </div>
            )}
            
            {createSuccess && (
              <div className="create-success" style={{ marginTop: 16 }}>
                {createSuccess}
              </div>
            )}

            <div className="job-create-actions">
              <button 
                className="btn btn-purple" 
                type="button" 
                onClick={handleCreateJob}
                disabled={isCreating}
              >
                {isCreating ? 'Создание...' : 'Добавить вакансию'}
              </button>
            </div>
          </div>
        )}
      </div>
      
      {/* Список существующих вакансий */}
      {vacancies.length === 0 ? (
        <div style={{ padding: 24, textAlign: 'center' }}>
          Нет доступных вакансий
        </div>
      ) : (
        <div className="jobs" style={{ marginTop: 24 }}>
          {vacancies.map((job) => (
            <article 
              key={job.id} 
              className="job-card"
              onClick={() => handleJobClick(job)}
              style={{ cursor: 'pointer' }}
            >
              <h4 className="job-card__title">{job.title}</h4>
              <p className="job-card__company">
                {job.department} • {getLevelText(job.level)}
              </p>
              <p className="job-card__location">
                {job.location} {job.remote_available ? '(возможна удаленка)' : ''}
              </p>
              <p className="job-card__salary">
                {formatSalary(job.average_salary, job.salary_currency)}
              </p>
            </article>
          ))}
        </div>
      )}

      {showJobModal && selectedJob && (
        <JobDetailsModal 
          job={selectedJob} 
          onClose={closeJobModal}
          onDelete={handleDeleteJob}
          formatSalary={formatSalary}
          formatDate={formatDate}
          getStatusText={getStatusText}
          getLevelText={getLevelText}
          getEmploymentTypeText={getEmploymentTypeText}
        />
      )}
    </section>
  )
}

function JobDetailsModal({ 
  job, 
  onClose, 
  onDelete,
  formatSalary, 
  formatDate, 
  getStatusText, 
  getLevelText, 
  getEmploymentTypeText 
}) {
  return (
    <div className="modal" role="dialog" aria-modal="true">
      <div className="modal__backdrop" onClick={onClose} />
      <div className="modal__dialog modal__dialog--large" role="document">
        <header className="modal__header">
          <div>
            <h2>{job.title}</h2>
            <p className="modal__subtitle">{job.department}</p>
          </div>
          <button className="icon-button icon-button--ghost modal__close" type="button" onClick={onClose}>
            <CloseIcon className="icon icon--small" />
          </button>
        </header>

        <div className="modal__content">
          <div className="job-details">
            <div className="job-details__section">
              <h3>Основная информация</h3>
              <div className="job-details__grid">
                <div className="job-details__item">
                  <span className="job-details__label">Уровень:</span>
                  <span className="job-details__value">{getLevelText(job.level)}</span>
                </div>
                <div className="job-details__item">
                  <span className="job-details__label">Тип занятости:</span>
                  <span className="job-details__value">{getEmploymentTypeText(job.employment_type)}</span>
                </div>
                <div className="job-details__item">
                  <span className="job-details__label">Локация:</span>
                  <span className="job-details__value">{job.location || 'Не указана'}</span>
                </div>
                <div className="job-details__item">
                  <span className="job-details__label">Удаленная работа:</span>
                  <span className="job-details__value">{job.remote_available ? 'Возможна' : 'Нет'}</span>
                </div>
                <div className="job-details__item">
                  <span className="job-details__label">Опыт:</span>
                  <span className="job-details__value">
                    {job.min_experience_years !== undefined && job.max_experience_years !== undefined
                      ? `${job.min_experience_years}-${job.max_experience_years} лет`
                      : 'Не указан'
                    }
                  </span>
                </div>
                <div className="job-details__item">
                  <span className="job-details__label">Зарплата:</span>
                  <span className="job-details__value">{formatSalary(job.average_salary, job.salary_currency)}</span>
                </div>
                <div className="job-details__item">
                  <span className="job-details__label">Статус:</span>
                  <span className={`job-details__value job-details__value--status job-details__value--${job.status}`}>
                    {getStatusText(job.status)}
                  </span>
                </div>
              </div>
            </div>

            {job.description && (
              <div className="job-details__section">
                <h3>Описание</h3>
                <div className="job-details__text">
                  {job.description}
                </div>
              </div>
            )}

            {job.requirements && (
              <div className="job-details__section">
                <h3>Требования</h3>
                <div className="job-details__text">
                  {job.requirements}
                </div>
              </div>
            )}

            {job.responsibilities && (
              <div className="job-details__section">
                <h3>Обязанности</h3>
                <div className="job-details__text">
                  {job.responsibilities}
                </div>
              </div>
            )}

            {job.required_skills && job.required_skills.length > 0 && (
              <div className="job-details__section">
                <h3>Необходимые навыки</h3>
                <div className="job-details__skills">
                  {job.required_skills.map((skill, index) => (
                    <span key={index} className="job-details__skill">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="job-details__section">
              <h3>Даты</h3>
              <div className="job-details__grid">
                <div className="job-details__item">
                  <span className="job-details__label">Создана:</span>
                  <span className="job-details__value">{formatDate(job.created_at)}</span>
                </div>
                <div className="job-details__item">
                  <span className="job-details__label">Обновлена:</span>
                  <span className="job-details__value">{formatDate(job.updated_at)}</span>
                </div>
                {job.published_at && (
                  <div className="job-details__item">
                    <span className="job-details__label">Опубликована:</span>
                    <span className="job-details__value">{formatDate(job.published_at)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <footer className="modal__footer">
          <button 
            className="btn btn-ghost btn-danger" 
            type="button" 
            onClick={() => onDelete(job.id)}
            style={{ color: '#ef4444', marginRight: 'auto' }}
          >
            Удалить
          </button>
          <button className="btn btn-ghost" type="button" onClick={onClose}>
            Закрыть
          </button>
        </footer>
      </div>
    </div>
  );
}

function CvResultsModal({ list, onClose }) {
  const [folderName, setFolderName] = React.useState('')
  const [selected, setSelected] = React.useState(null)
  const addToFolder = () => { onClose() }
  
  // Функция для получения отображаемого имени
  const getDisplayName = (item) => {
    return item.name || item.full_name || item.title || 'Без названия'
  }
  
  // Функция для получения мета-информации
  const getMetaInfo = (item) => {
    if (item.folder && item.uploaded) {
      return `${item.folder} - ${item.uploaded}`
    }
    if (item.department) {
      const rating = item.rating ? ` • Рейтинг: ${item.rating}/5` : ''
      const matchScore = item.match_score ? ` • Соответствие: ${Math.round(item.match_score * 100)}%` : ''
      return `${item.department} - ${item.experience_years || 0} лет опыта${rating}${matchScore}`
    }
    return 'Информация недоступна'
  }
  
  // Функция для получения навыков сотрудника
  const getSkills = (item) => {
    if (item.skills && Array.isArray(item.skills) && item.skills.length > 0) {
      return item.skills.slice(0, 3).join(', ') + (item.skills.length > 3 ? '...' : '')
    }
    return null
  }
  
  return (
    <div className="modal" role="dialog" aria-modal="true">
      <div className="modal__backdrop" onClick={onClose} />
      <div className="modal__dialog" role="document">
        <header className="modal__header">
          <h2>Найденные сотрудники</h2>
          <button className="icon-button icon-button--ghost modal__close" type="button" onClick={onClose}>
            <CloseIcon className="icon icon--small" />
          </button>
        </header>
        <div className="modal__content" style={{ display: 'grid', gridTemplateColumns: '1fr 260px', gap: 16 }}>
          <ul className="list" style={{ maxHeight: 360, overflow: 'auto' }}>
            {list.length === 0 ? (
              <li className="list__item" style={{ textAlign: 'center', color: '#6b7280' }}>
                Результаты не найдены
              </li>
            ) : (
              list.map((cv, index) => (
                <li key={cv.id || index} className="list__item" onClick={() => setSelected(cv)} style={{ cursor: 'pointer' }}>
                  <div>
                    <span className="list__title">{getDisplayName(cv)}</span>
                    <span className="list__meta">{getMetaInfo(cv)}</span>
                    {getSkills(cv) && (
                      <div style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>
                        Навыки: {getSkills(cv)}
                      </div>
                    )}
                  </div>
                </li>
              ))
            )}
          </ul>
          <div className="form-grid">
            {selected && selected.department ? (
              // Показываем информацию о выбранном сотруднике
              <div>
                <h3 style={{ margin: '0 0 16px 0', fontSize: '16px' }}>Информация о сотруднике</h3>
                <div style={{ fontSize: '14px', lineHeight: '1.4' }}>
                  <p><strong>Имя:</strong> {getDisplayName(selected)}</p>
                  <p><strong>Департамент:</strong> {selected.department}</p>
                  <p><strong>Опыт:</strong> {selected.experience_years} лет</p>
                  {selected.rating && <p><strong>Рейтинг:</strong> {selected.rating}/5</p>}
                  {selected.match_score && <p><strong>Соответствие:</strong> {Math.round(selected.match_score * 100)}%</p>}
                  {selected.skills && selected.skills.length > 0 && (
                    <div>
                      <strong>Навыки:</strong>
                      <div style={{ marginTop: '8px' }}>
                        {selected.skills.map((skill, index) => (
                          <span key={index} style={{
                            display: 'inline-block',
                            padding: '4px 8px',
                            margin: '2px',
                            backgroundColor: '#f3f4f6',
                            borderRadius: '4px',
                            fontSize: '12px'
                          }}>
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              // Показываем форму добавления в папку для обычных CV
              <>
                <label className="field"><span className="field__label">Папка</span><input className="field__input" placeholder="Новая или существующая" value={folderName} onChange={(e) => setFolderName(e.target.value)} /></label>
                <button className="btn btn-purple" type="button" disabled={!selected || !folderName} onClick={addToFolder}>Добавить выбранное</button>
              </>
            )}
          </div>
        </div>
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



function SubCard({ title, render }) {
  const [edit, setEdit] = React.useState(false)
  return (
    <div className="subcard">
      <div className="subcard__header">
        <h4 className="subcard__title">{title}</h4>
      </div>
      <div className="subcard__body">{render(edit)}</div>
    </div>
  )
}

// Модальное окно для информации о папке
function FolderFilesModal({ folder, folderDetails, isLoadingDetails, onClose, onDelete }) {
  const [jobInfo, setJobInfo] = React.useState(null);
  const [isLoadingJob, setIsLoadingJob] = React.useState(false);
  const [token] = React.useState(localStorage.getItem('token'));

  // Сбрасываем состояние при открытии нового модального окна
  React.useEffect(() => {
    setJobInfo(null);
    setIsLoadingJob(false);
  }, [folder?.id]);

  const formatMoscowDate = (dateString) => {
    if (!dateString) return 'Неизвестно';
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const displayData = folderDetails || folder;

  // Загружаем информацию о вакансии когда получаем детали папки
  React.useEffect(() => {
    const loadJobInfo = async () => {
      if (displayData?.job_id && token && !isLoadingJob) {
        try {
          setIsLoadingJob(true);
          const job = await api.getJobById(token, displayData.job_id);
          setJobInfo(job);
        } catch (error) {
          console.error('Ошибка загрузки информации о вакансии:', error);
          setJobInfo(null);
        } finally {
          setIsLoadingJob(false);
        }
      }
    };

    loadJobInfo();
  }, [displayData?.job_id, token]);

  return (
    <div className="modal" role="dialog" aria-modal="true" style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div className="modal__backdrop" onClick={onClose} />
      <div className="modal__dialog" role="document" style={{
        width: '90%', 
        maxWidth: '800px', 
        margin: '0 auto',
        backgroundColor: '#1f2937',
        borderRadius: '12px',
        border: '1px solid #374151'
      }}>
        <header className="modal__header" >
          <h2 style={{fontSize: '1.5rem', marginBottom: '1rem', color: '#f3f4f6'}}>Информация о папке: {displayData.name}</h2>
          <button className="icon-button icon-button--ghost modal__close" type="button" onClick={onClose} style={{color: '#f3f4f6'}}>
            <CloseIcon className="icon icon--small" />
          </button>
        </header>
        <div className="modal__content" style={{
          maxHeight: '70vh', 
          overflowY: 'auto', 
          padding: '1.5rem',
          backgroundColor: '#1f2937'
        }}>
          {isLoadingDetails ? (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
              <p style={{color: '#d1d5db'}}>Загрузка деталей папки...</p>
            </div>
          ) : (
            <div>
              {/* Основная информация о папке */}
              <div style={{marginBottom: '2rem', padding: '1.5rem', backgroundColor: '#374151', borderRadius: '8px', border: '1px solid #4b5563'}}>
                <h3 style={{fontSize: '1.25rem', marginBottom: '1rem', color: '#f3f4f6'}}>Основная информация</h3>
                <div style={{display: 'grid', gap: '0.75rem'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{fontWeight: '500', color: '#9ca3af'}}>Название:</span>
                    <span style={{color: '#f3f4f6'}}>{displayData.name}</span>
                  </div>
                  {displayData.description && (
                    <div style={{display: 'flex', justifyContent: 'space-between'}}>
                      <span style={{fontWeight: '500', color: '#9ca3af'}}>Описание:</span>
                      <span style={{color: '#f3f4f6', textAlign: 'right', maxWidth: '60%'}}>{displayData.description}</span>
                    </div>
                  )}
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{fontWeight: '500', color: '#9ca3af'}}>Кандидатов:</span>
                    <span style={{color: '#f3f4f6'}}>{displayData.candidates_count || 0}</span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{fontWeight: '500', color: '#9ca3af'}}>Создано:</span>
                    <span style={{color: '#f3f4f6'}}>{formatMoscowDate(displayData.created_at)}</span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{fontWeight: '500', color: '#9ca3af'}}>Обновлено:</span>
                    <span style={{color: '#f3f4f6'}}>{formatMoscowDate(displayData.updated_at)}</span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{fontWeight: '500', color: '#9ca3af'}}>Вакансия:</span>
                    <span style={{color: '#f3f4f6', textAlign: 'right', maxWidth: '60%'}}>
                      {isLoadingJob ? (
                        <span style={{color: '#9ca3af'}}>Загрузка...</span>
                      ) : jobInfo ? (
                        <span>
                          {jobInfo.title}
                          {jobInfo.department && (
                            <span style={{color: '#9ca3af', fontSize: '0.875rem', display: 'block'}}>
                              {jobInfo.department}
                            </span>
                          )}
                        </span>
                      ) : (
                        <span style={{color: '#d1d5db', fontFamily: 'monospace', fontSize: '0.875rem'}}>
                          {displayData.job_id}
                        </span>
                      )}
                    </span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{fontWeight: '500', color: '#9ca3af'}}>Статус:</span>
                    <span style={{
                      color: displayData.is_active ? '#10b981' : '#f87171',
                      fontWeight: '500'
                    }}>
                      {displayData.is_active ? 'Активна' : 'Неактивна'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Список файлов (пока заглушка, так как в API нет информации о файлах) */}
              <div>
                <h3 style={{fontSize: '1.25rem', marginBottom: '1rem', color: '#f3f4f6'}}>Файлы кандидатов</h3>
                {(folder.files && folder.files.length > 0) ? (
                  <ul className="folder-card__list" style={{gap: '1rem'}}>
                    {folder.files.map((file) => (
                      <li key={file.id} className="folder-card__item" style={{padding: '1rem', borderRadius: '8px'}}>
                        <div className="folder-card__file">
                          <span className="folder-card__file-icon"><PdfIcon className="icon icon--small" /></span>
                          <div className="folder-card__file-info">
                            <p className="folder-card__file-name" style={{fontSize: '1.1rem', marginBottom: '0.5rem'}}>{file.name}</p>
                            <span className="folder-card__file-meta">Загружено {file.uploaded}</span>
                          </div>
                        </div>
                        <span className="folder-card__badge">PDF</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div style={{
                    padding: '2rem',
                    textAlign: 'center',
                    backgroundColor: '#374151',
                    borderRadius: '8px',
                    border: '2px dashed #6b7280'
                  }}>
                    <PdfIcon className="icon" style={{fontSize: '2rem', color: '#9ca3af', marginBottom: '1rem'}} />
                    <p style={{color: '#d1d5db', marginBottom: '0.5rem'}}>В папке пока нет файлов</p>
                    <p style={{color: '#9ca3af', fontSize: '0.875rem'}}>Кандидаты будут появляться здесь после добавления в папку</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        <footer className="modal__footer" style={{
          padding: '1rem 1.5rem',
          borderTop: '1px solid #374151',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#1f2937'
        }}>
          <button 
            className="btn btn-danger" 
            type="button" 
            onClick={() => onDelete(displayData.id)}
            style={{
              backgroundColor: '#dc2626',
              color: 'white',
              border: 'none',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            Удалить
          </button>
          <button 
            className="btn btn-ghost" 
            type="button" 
            onClick={onClose}
            style={{
              backgroundColor: 'transparent',
              color: '#d1d5db',
              border: '1px solid #4b5563',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            Закрыть
          </button>
        </footer>
      </div>
    </div>
  )
}

// Модальное окно для создания папки
function CreateFolderModal({ 
  jobs, 
  isLoadingJobs, 
  newFolder, 
  setNewFolder, 
  isCreating, 
  error, 
  onSubmit, 
  onClose 
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  const updateField = (field) => (e) => {
    setNewFolder(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  };

  return (
    <div className="modal" role="dialog" aria-modal="true" style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div className="modal__backdrop" onClick={onClose} />
      <div className="modal__dialog" role="document" style={{width: '90%', maxWidth: '500px', margin: '0 auto'}}>
        <header className="modal__header">
          <h2 style={{fontSize: '1.5rem', marginBottom: '1rem'}}>Создать новую папку</h2>
          <button className="icon-button icon-button--ghost modal__close" type="button" onClick={onClose}>
            <CloseIcon className="icon icon--small" />
          </button>
        </header>
        <div className="modal__content" style={{padding: '1.5rem'}}>
          <form onSubmit={handleSubmit}>
            <div className="form-grid" style={{gap: '1rem'}}>
              <label className="field">
                <span className="field__label">Название папки *</span>
                <input 
                  className="field__input" 
                  type="text" 
                  value={newFolder.name}
                  onChange={updateField('name')}
                  placeholder="Введите название папки"
                  required
                />
              </label>

              <label className="field">
                <span className="field__label">Описание</span>
                <textarea 
                  className="field__input" 
                  rows={3}
                  value={newFolder.description}
                  onChange={updateField('description')}
                  placeholder="Опишите папку (необязательно)"
                />
              </label>

              <label className="field">
                <span className="field__label">Вакансия *</span>
                {isLoadingJobs ? (
                  <div style={{padding: '0.5rem', color: '#6b7280'}}>Загрузка вакансий...</div>
                ) : (
                  <select 
                    className="field__input"
                    value={newFolder.job_id}
                    onChange={updateField('job_id')}
                    required
                  >
                    <option value="">Выберите вакансию</option>
                    {jobs.map(job => (
                      <option key={job.id} value={job.id}>
                        {job.title} ({job.department || 'Без отдела'})
                      </option>
                    ))}
                  </select>
                )}
              </label>

              {error && (
                <div style={{
                  padding: '0.75rem',
                  backgroundColor: '#fef2f2',
                  border: '1px solid #fecaca',
                  borderRadius: '6px',
                  color: '#dc2626',
                  fontSize: '0.875rem'
                }}>
                  {error}
                </div>
              )}

              <div style={{display: 'flex', gap: '1rem', marginTop: '1rem'}}>
                <button 
                  className="btn btn-purple" 
                  type="submit"
                  disabled={isCreating || !newFolder.name.trim() || !newFolder.job_id}
                >
                  {isCreating ? 'Создание...' : 'Создать папку'}
                </button>
                <button 
                  className="btn btn-ghost" 
                  type="button" 
                  onClick={onClose}
                  disabled={isCreating}
                >
                  Отмена
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

