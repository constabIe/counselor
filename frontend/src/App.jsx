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
  const [token, setToken] = React.useState(localStorage.getItem('token'));
  const [userData, setUserData] = React.useState(null);
  const [isFirstLogin, setIsFirstLogin] = React.useState(false);
  const [showCvManager, setShowCvManager] = React.useState(false);
  const [dashboardKey, setDashboardKey] = React.useState(0); // Для принудительного обновления EmployeeDashboard

  React.useEffect(() => {
    if (token) {
      api.getUserProfile(token)
        .then(async data => {
          // map backend profile to the shape EmployeeDashboard expects
          const mapped = {
            fullName: data.full_name || data.fullName || data.name || data.email || 'Пользователь',
            rating: (data.rating !== undefined && data.rating !== null) ? data.rating : 0,
            xp: (data.xp !== undefined && data.xp !== null) ? data.xp : 0,
            badges: Array.isArray(data.badges) ? data.badges : [],
            cvFileName: data.cv_file_name || data.cvFileName || data.cv || '',
            uploadedAt: data.uploaded_at || data.uploadedAt || '',
            // keep raw profile in case other components need it
            __raw: data,
          };

          setUserData(mapped);

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

  const handleOldCvUploaded = (fileName) => {
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

  const handleCvUploaded = () => {
    setIsFirstLogin(false);
    setShowCvManager(false);
    setView('employeeDashboard');
    setDashboardKey(prev => prev + 1); // Принудительно обновляем EmployeeDashboard
    
    // Загружаем обновленную информацию о пользователе
    if (token) {
      api.getUserProfile(token)
        .then(data => {
          const mapped = {
            fullName: data.full_name || data.fullName || data.name || data.email || 'Пользователь',
            rating: (data.rating !== undefined && data.rating !== null) ? data.rating : 0,
            xp: (data.xp !== undefined && data.xp !== null) ? data.xp : 0,
            badges: Array.isArray(data.badges) ? data.badges : [],
            cvFileName: data.cv_file_name || data.cvFileName || data.cv || '',
            uploadedAt: data.uploaded_at || data.uploadedAt || '',
            __raw: data,
          };
          setUserData(mapped);
        })
        .catch(console.error);
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
              <h3>У вас уже аккаунт?</h3>
              <p className="auth__hint">Выберите роль, затем авторизуйтесь.</p>
            </div>

            <div className="auth__role">
              <label className={`auth__pill ${loginRole === 'employee' ? 'is-active' : ''}`}>
                <input type="radio" name="login-role" value="employee" checked={loginRole === 'employee'} onChange={() => setLoginRole('employee')} />
                Сотрудник
              </label>
              <label className={`auth__pill ${loginRole === 'hr' ? 'is-active' : ''}`}>
                <input type="radio" name="login-role" value="hr" checked={loginRole === 'hr'} onChange={() => setLoginRole('hr')} />
                HR
              </label>
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
              <label className="auth__field">
                <span>Повтор пароля</span>
                <input type="password" value={registerConfirm} onChange={(event) => setRegisterConfirm(event.target.value)} placeholder="Повторите пароль" />
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
                  Загружено: {new Date(currentCv.uploaded_at).toLocaleString('ru-RU', {
                    day: '2-digit',
                    month: 'long',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
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


function EmployeeDashboard({ data, onLogout, onReupload, onOpenTasks }) {
  const [activeTab, setActiveTab] = React.useState('opportunities')
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
  
  // Состояния для личного помощника
  const [assistantMessages, setAssistantMessages] = React.useState([
    { from: 'bot', text: 'Привет! Я ваш личный помощник. Помогу с карьерными вопросами, анализом резюме и планированием развития. Что вас интересует?' }
  ])
  const [assistantInput, setAssistantInput] = React.useState('')
  const [completedTasks, setCompletedTasks] = React.useState([])

  // Загружаем информацию о CV и профиле при монтировании компонента
  React.useEffect(() => {
    if (token) {
      loadCvInfo();
      loadUserProfile();
      loadCourses();
      loadMyEnrollments();
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
      const enrollments = await api.getMyEnrollments(token);
      setMyEnrollments(enrollments || []);
    } catch (error) {
      console.error('Ошибка загрузки записей на курсы:', error);
      setMyEnrollments([]);
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

  const jobs = [
    { id: 'j1', title: 'Frontend Junior', company: 'TechNova', tags: ['React', 'JS', 'HTML/CSS'] },
    { id: 'j2', title: 'Data Analyst', company: 'DataWise', tags: ['SQL', 'Python', 'BI'] },
    { id: 'j3', title: 'QA Engineer', company: 'QualityLab', tags: ['Manual', 'API', 'Postman'] },
  ]

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
                  <>
                    <RatingStars value={parseFloat(currentCv.rating)} />
                    <span className="profile-card__metric-value">{parseFloat(currentCv.rating).toFixed(1)}</span>
                  </>
                ) : (
                  <span className="profile-card__metric-value">Нет данных</span>
                )}
              </div>
              <div className="profile-card__metric">
                <span className="profile-card__metric-label">XP:</span>
                {isLoadingProfile ? (
                  <span className="profile-card__metric-value">Загрузка...</span>
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
                Загружено: {new Date(currentCv.uploaded_at).toLocaleString('ru-RU', {
                  day: '2-digit',
                  month: 'long',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
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
          <button className="btn btn-purple" type="button" onClick={onOpenTasks}>
            Посмотреть задачи
          </button>
        </div>
      </section>

      <nav className="tabs">
        <button type="button" className={`tabs__btn ${activeTab === 'personal_assistant' ? 'is-active' : ''}`} onClick={() => setActiveTab('personal_assistant')}>Личный помощник</button>
        <button type="button" className={`tabs__btn ${activeTab === 'data' ? 'is-active' : ''}`} onClick={() => setActiveTab('data')}>Данные</button>
        <button type="button" className={`tabs__btn ${activeTab === 'opportunities' ? 'is-active' : ''}`} onClick={() => setActiveTab('opportunities')}>Карьерные возможности</button>
        <button type="button" className={`tabs__btn ${activeTab === 'courses' ? 'is-active' : ''}`} onClick={() => setActiveTab('courses')}>Курсы</button>
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
                    className="field__input" 
                    type="text" 
                    placeholder="Задайте вопрос помощнику..." 
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
          <div className="jobs">
            {jobs.map((j) => (
              <article key={j.id} className="job-card">
                <h4 className="job-card__title">{j.title}</h4>
                <p className="job-card__company">{j.company}</p>
                <div className="job-card__tags">
                  {j.tags.map((t) => (
                    <span key={t} className="tag">{t}</span>
                  ))}
                </div>
                <button className="btn btn-outline job-card__action" type="button">Откликнуться</button>
              </article>
            ))}
          </div>
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
              <SubCard title="Личная информация" render={(edit) => (
                <div className="form-grid">
                  <EditableField label="Возраст" value={getCvValue('age', 'Не указан')} onChange={() => {}} edit={false} />
                  <EditableField label="Опыт работы" value={getCvValue('experience_years') ? `${getCvValue('experience_years')} лет` : 'Не указан'} onChange={() => {}} edit={false} />
                  <EditableField label="Подразделение" value={getCvValue('department')} onChange={() => {}} edit={false} />
                  <EditableField label="Грейд" value={getCvValue('grade')} onChange={() => {}} edit={false} />
                  <EditableField label="Специализация" value={getCvValue('specialization')} onChange={() => {}} edit={false} />
                </div>
              )} />

              <SubCard title="Образование" render={(edit) => (
                <div className="form-grid">
                  <EditableField label="Образование" value={parseJsonField('education')} onChange={() => {}} edit={false} />
                  <EditableField label="Дополнительное образование" value={parseJsonField('additional_education')} onChange={() => {}} edit={false} />
                </div>
              )} />

              <SubCard title="Текущая роль" render={(edit) => (
                <div className="form-grid">
                  <EditableField label="Текущая должность" value={parseJsonField('current_role')} onChange={() => {}} edit={false} />
                  <EditableField label="Обязанности" value={parseJsonField('responsibilities')} onChange={() => {}} edit={false} />
                </div>
              )} />

              <SubCard title="Навыки и компетенции" render={(edit) => (
                <div className="form-grid">
                  <EditableField label="Навыки" value={parseJsonField('skills')} onChange={() => {}} edit={false} />
                  <EditableField label="Компетенции" value={parseJsonField('competencies')} onChange={() => {}} edit={false} />
                  <EditableField label="Языки" value={parseJsonField('languages')} onChange={() => {}} edit={false} />
                </div>
              )} />

              <SubCard title="Опыт работы" render={(edit) => (
                <div className="form-grid">
                  <EditableField label="Предыдущие места работы" value={parseJsonField('jobs')} onChange={() => {}} edit={false} />
                </div>
              )} />

              <SubCard title="Дополнительная информация" render={(edit) => (
                <div className="form-grid">
                  <EditableField label="Комментарии" value={getCvValue('comments')} onChange={() => {}} edit={false} />
                  <EditableField label="Рейтинг" value={getCvValue('rating') ? `${getCvValue('rating')}/10` : 'Не оценен'} onChange={() => {}} edit={false} />
                  <EditableField label="Теги" value={parseJsonField('tags')} onChange={() => {}} edit={false} />
                  <EditableField label="Карьерный путь" value={parseJsonField('career_path')} onChange={() => {}} edit={false} />
                </div>
              )} />

              <SubCard title="Статус анализа" render={(edit) => (
                <div className="form-grid">
                  <EditableField label="Статус обработки" value={getCvValue('analysis_status', 'Ожидает анализа')} onChange={() => {}} edit={false} />
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
                      {isEnrolledInCourse(c.id) && (
                        <div className="course-enrolled-badge">
                          ✅ Вы записаны
                        </div>
                      )}
                    </div>
                    <button 
                      className="folder-card__action" 
                      type="button" 
                      onClick={() => handleCourseClick(c)}
                    >
                      {isEnrolledInCourse(c.id) ? 'Посмотреть курс' : 'Выбрать курс'}
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
                          {new Date(selectedCourse.created_at).toLocaleDateString('ru-RU')}
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
  const hrName = 'Садыков Хасан Альбертович'
  const [activeTab, setActiveTab] = React.useState('search')
  const [expandedFolders, setExpandedFolders] = React.useState({})
  const [activeFolder, setActiveFolder] = React.useState(null)

  const [filters, setFilters] = React.useState({
    ageMin: 21,
    ageMax: 45,
    gender: '',
    expMin: 0,
    expMax: 10,
    languages: '',
    education: '',
    specialty: '',
    format: '',
    uploaded: '',
    ratingMin: 0,
  })

  const [messages, setMessages] = React.useState([
    { from: 'bot', text: 'Привет! Опишите кандидата или выберите фильтры слева.' },
  ])
  const [chatInput, setChatInput] = React.useState('')
  const [showCvModal, setShowCvModal] = React.useState(false)

  const allCvs = React.useMemo(
    () => hrFolders.flatMap((f) => (f.files || []).map((file) => ({ ...file, folder: f.name }))),
    []
  )

  const sendQuery = () => {
    const text = chatInput.trim()
    if (!text) return
    setMessages((prev) => [...prev, { from: 'user', text }])
    setChatInput('')
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { from: 'bot', text: 'Нашлось несколько подходящих резюме. Открыть список?', action: 'open' },
      ])
    }, 200)
  }

  const onBotAction = (msg) => {
    if (msg.action === 'open') setShowCvModal(true)
  }

  const update = (key) => (e) => setFilters((p) => ({ ...p, [key]: e.target.value }))
  // Открытие модального окна с файлами папки
  const openFolderModal = (folder) => setActiveFolder(folder)
  const closeFolderModal = () => setActiveFolder(null)

  return (
    <div className="hr-dashboard">
      <header className="dashboard-header">
        <span className="brand">HR-Counselor</span>
        <button className="btn btn-ghost btn-small" type="button" onClick={onLogout}>Выйти</button>
      </header>

      <div className="employee-dashboard__top">
        <div className="profile-card">
          <div className="profile-card__avatar">{hrName.slice(0, 1)}</div>
          <div>
            <h2 className="profile-card__name">{hrName}</h2>
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
              <label className="field"><span className="field__label">Формат работы</span><input className="field__input" type="text" placeholder="офис/гибрид/удалёнка" value={filters.format} onChange={update('format')} /></label>
              <label className="field"><span className="field__label">Дата загрузки</span><input className="field__input" type="date" value={filters.uploaded} onChange={update('uploaded')} /></label>
              <label className="field"><span className="field__label">Мин. рейтинг</span><input className="field__input" type="number" value={filters.ratingMin} onChange={update('ratingMin')} /></label>
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
              <input className="field__input" type="text" placeholder="Опишите требования..." value={chatInput} onChange={(e) => setChatInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && sendQuery()} />
              <button className="btn btn-green" type="button" onClick={sendQuery}>Отправить</button>
            </div>
          </section>
        </section>
      )}

      {activeTab === 'vacancies' && <VacanciesTab />}

      {activeTab === 'folders' && (
        <section className="panel">
          <div className="hr-dashboard__grid">
            {hrFolders.map((folder) => (
              <article key={folder.id} className="folder-card" style={{ '--accent': folder.accent }}>
                <div className="folder-card__icon"><FolderIcon className="icon" /></div>
                <div className="folder-card__body">
                  <h2>{folder.name}</h2>
                  <p>{folder.count} CV</p>
                  <span>Обновлено {folder.updated}</span>
                </div>
                <button className="folder-card__action" type="button" onClick={() => openFolderModal(folder)}>
                  Открыть папку
                </button>
              </article>
            ))}
          </div>
          {activeFolder && (
            <FolderFilesModal folder={activeFolder} onClose={closeFolderModal} />
          )}
        </section>
      )}



      {showCvModal && (
        <CvResultsModal list={allCvs} onClose={() => setShowCvModal(false)} />
      )}
    </div>
  )
}

function VacanciesTab() {
  const [vacancies, setVacancies] = React.useState([{ id: 'v1', title: 'Frontend Junior', location: 'Казань', format: 'гибрид' }])
  const [title, setTitle] = React.useState('')
  const [location, setLocation] = React.useState('')
  const [format, setFormat] = React.useState('')
  const add = () => {
    if (!title.trim()) return
    setVacancies((prev) => [...prev, { id: String(Date.now()), title, location, format }])
    setTitle(''); setLocation(''); setFormat('')
  }
  return (
    <section className="panel">
      <div className="panel__header"><h3>Свободные вакансии</h3></div>
      <div className="form-grid">
        <label className="field"><span className="field__label">Название</span><input className="field__input" value={title} onChange={(e) => setTitle(e.target.value)} /></label>
        <label className="field"><span className="field__label">Локация</span><input className="field__input" value={location} onChange={(e) => setLocation(e.target.value)} /></label>
        <label className="field"><span className="field__label">Формат</span><input className="field__input" placeholder="офис/гибрид/удалёнка" value={format} onChange={(e) => setFormat(e.target.value)} /></label>
        <div><button className="btn btn-purple" type="button" onClick={add}>Добавить</button></div>
      </div>
      <div className="jobs" style={{ marginTop: 16 }}>
        {vacancies.map((v) => (
          <article key={v.id} className="job-card">
            <h4 className="job-card__title">{v.title}</h4>
            <p className="job-card__company">{(v.location || '-') + ' - ' + (v.format || '-')}</p>
          </article>
        ))}
      </div>
    </section>
  )
}

function CvResultsModal({ list, onClose }) {
  const [folderName, setFolderName] = React.useState('')
  const [selected, setSelected] = React.useState(null)
  const addToFolder = () => { onClose() }
  return (
    <div className="modal" role="dialog" aria-modal="true">
      <div className="modal__backdrop" onClick={onClose} />
      <div className="modal__dialog" role="document">
        <header className="modal__header">
          <h2>Подходящие резюме</h2>
          <button className="icon-button icon-button--ghost modal__close" type="button" onClick={onClose}>
            <CloseIcon className="icon icon--small" />
          </button>
        </header>
        <div className="modal__content" style={{ display: 'grid', gridTemplateColumns: '1fr 260px', gap: 16 }}>
          <ul className="list" style={{ maxHeight: 360, overflow: 'auto' }}>
            {list.map((cv) => (
              <li key={cv.id} className="list__item" onClick={() => setSelected(cv)} style={{ cursor: 'pointer' }}>
                <span className="list__title">{cv.name}</span>
                <span className="list__meta">{cv.folder + ' - ' + cv.uploaded}</span>
              </li>
            ))}
          </ul>
          <div className="form-grid">
            <label className="field"><span className="field__label">Папка</span><input className="field__input" placeholder="Новая или существующая" value={folderName} onChange={(e) => setFolderName(e.target.value)} /></label>
            <button className="btn btn-purple" type="button" disabled={!selected || !folderName} onClick={addToFolder}>Добавить выбранное</button>
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
        <button className="btn btn-ghost btn-small" type="button" onClick={() => setEdit((v) => !v)}>
          {edit ? 'Сохранить' : 'Редактировать'}
        </button>
      </div>
      <div className="subcard__body">{render(edit)}</div>
    </div>
  )
}

// Модальное окно для файлов папки
function FolderFilesModal({ folder, onClose }) {
  return (
    <div className="modal" role="dialog" aria-modal="true" style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div className="modal__backdrop" onClick={onClose} />
      <div className="modal__dialog" role="document" style={{width: '90%', maxWidth: '800px', margin: '0 auto'}}>
        <header className="modal__header">
          <h2 style={{fontSize: '1.5rem', marginBottom: '1rem'}}>Файлы папки: {folder.name}</h2>
          <button className="icon-button icon-button--ghost modal__close" type="button" onClick={onClose}>
            <CloseIcon className="icon icon--small" />
          </button>
        </header>
        <div className="modal__content" style={{maxHeight: '70vh', overflowY: 'auto', padding: '1.5rem'}}>
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
        </div>
      </div>
    </div>
  )
}

