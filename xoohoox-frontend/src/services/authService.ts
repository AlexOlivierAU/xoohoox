import api from './api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user?: User;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me');
    return response.data;
  }

  async logout(): Promise<void> {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    return !!token;
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  setAuthData(token: string, user?: User): void {
    localStorage.setItem('token', token);
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    }
  }
}

export default new AuthService(); 