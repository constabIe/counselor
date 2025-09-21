const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000';

async function parseError(response) {
  let body = null;
  try {
    body = await response.json();
  } catch (e) {
    // ignore
  }
  const message = (body && (body.detail || body.message || body.error)) || response.statusText || 'Ошибка сервера';
  const err = new Error(message);
  err.status = response.status;
  throw err;
}

// WebSocket Chat Manager
class ChatManager {
  constructor() {
    this.socket = null;
    this.userId = null;
    this.token = null;
    this.onMessage = null;
    this.onError = null;
    this.onConnect = null;
    this.onDisconnect = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 3000;
  }

  connect(userId, token, callbacks = {}) {
    this.userId = userId;
    this.token = token;
    this.onMessage = callbacks.onMessage || (() => {});
    this.onError = callbacks.onError || (() => {});
    this.onConnect = callbacks.onConnect || (() => {});
    this.onDisconnect = callbacks.onDisconnect || (() => {});

    this._connect();
  }

  _connect() {
    try {
      // Добавляем токен как query параметр
      const wsUrl = `${WS_URL}/chat/ws/chat/${this.userId}?token=${encodeURIComponent(this.token)}`;
      this.socket = new WebSocket(wsUrl);
      
      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.onConnect();
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
          this.onError('Ошибка обработки сообщения');
        }
      };

      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        this.onDisconnect();
        
        // Автоматическое переподключение
        if (this.reconnectAttempts < this.maxReconnectAttempts && event.code !== 1000) {
          this.reconnectAttempts++;
          console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          setTimeout(() => this._connect(), this.reconnectInterval);
        }
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.onError('Ошибка подключения к чату');
      };

    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.onError('Не удалось подключиться к чату');
    }
  }

  sendMessage(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const data = {
        message: message,
        timestamp: new Date().toISOString()
      };
      this.socket.send(JSON.stringify(data));
      return true;
    } else {
      this.onError('Соединение с чатом потеряно');
      return false;
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close(1000, 'User disconnected');
      this.socket = null;
    }
  }

  isConnected() {
    return this.socket && this.socket.readyState === WebSocket.OPEN;
  }
}

// Создаем единственный экземпляр менеджера чата
const chatManager = new ChatManager();

export const api = {
  async register(data) {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async login(data) {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getUserProfile(token) {
    const response = await fetch(`${API_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async uploadCv(token, file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_URL}/cv/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getMyCvs(token) {
    const response = await fetch(`${API_URL}/cv/my`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async downloadCv(token, cvId) {
    const response = await fetch(`${API_URL}/cv/${cvId}/download`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.blob();
  },

  async getCourses(token) {
    const response = await fetch(`${API_URL}/courses/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getCourseById(token, courseId) {
    const response = await fetch(`${API_URL}/courses/${courseId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async enrollInCourse(token, courseId) {
    const response = await fetch(`${API_URL}/courses/enroll/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ course_id: courseId }),
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getMyEnrollments(token) {
    const response = await fetch(`${API_URL}/courses/my-enrollments/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async updateCv(token, cvId, data) {
    const response = await fetch(`${API_URL}/cv/${cvId}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getJobs(token) {
    const response = await fetch(`${API_URL}/jobs/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async createJob(token, jobData) {
    const response = await fetch(`${API_URL}/jobs/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobData),
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getMyFolders(token, page = 1, per_page = 50) {
    const response = await fetch(`${API_URL}/folders/my?page=${page}&per_page=${per_page}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async createFolder(token, folderData) {
    const response = await fetch(`${API_URL}/folders/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(folderData),
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getFolderById(token, folderId) {
    const response = await fetch(`${API_URL}/folders/${folderId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async deleteFolder(token, folderId) {
    const response = await fetch(`${API_URL}/folders/${folderId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    
    // Возвращаем success для пустых ответов
    return { success: true };
  },

  async getJobById(token, jobId) {
    const response = await fetch(`${API_URL}/jobs/${jobId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async deleteJob(token, jobId) {
    const response = await fetch(`${API_URL}/jobs/${jobId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.ok;
  },

  async searchEmployees(token, searchData) {
    const response = await fetch(`${API_URL}/generation/employees/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(searchData),
    });
    if (!response.ok) {
      await parseError(response);
    }
    return response.json();
  },

  async getMyBadges(token) {
    const response = await fetch(`${API_URL}/badges/my`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      await parseError(response);
    }
    const data = await response.json();
    
    // Извлекаем названия бейджей из структуры и берём только 3 последних
    const badges = Array.isArray(data.badges) 
      ? data.badges
          .sort((a, b) => new Date(b.earned_at) - new Date(a.earned_at)) // Сортируем по дате получения (новые сначала)
          .slice(0, 3) // Берём 3 последних
          .map(item => item.badge.name) // Извлекаем название бейджа
      : [];
    
    return badges;
  },

  // Chat methods
  chat: {
    connect(userId, token, callbacks) {
      return chatManager.connect(userId, token, callbacks);
    },

    sendMessage(message) {
      return chatManager.sendMessage(message);
    },

    disconnect() {
      return chatManager.disconnect();
    },

    isConnected() {
      return chatManager.isConnected();
    }
  }
};