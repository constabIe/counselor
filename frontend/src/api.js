const API_URL = 'http://localhost:8000';

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
  }
};