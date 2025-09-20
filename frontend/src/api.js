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
  }
};