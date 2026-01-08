import apiClient from '../lib/axios';
import { useAuthStore } from '../stores/authStore';

export interface LoginCredentials {
  user_email: string;
  user_password: string;
}

export interface LoginResponse {
  message: string;
  metadata: {
    token: string;
    user: {
      id: string;
      user_fullName: string;
      user_email: string;
      user_userName: string;
      [key: string]: any;
    };
  };
}

// Check if running in PyWebView
const isPyWebView = () => typeof window !== 'undefined' && window.pywebview?.auth;

/**
 * Auth Service - React handles API calls, Python stores token
 */
class AuthService {
  /**
   * Login user via API, then notify Python to save token
   */
  async login(credentials: LoginCredentials) {
    try {
      // 1. Call API via Axios
      const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
      const { token, user } = response.data.metadata;

      // 2. Notify Python to save token (if running in PyWebView)
      if (isPyWebView()) {
        await window.pywebview.auth.on_login_success(token, user);
      } else {
        // Fallback to localStorage for browser testing
        localStorage.setItem('auth_token', token);
        localStorage.setItem('auth_user', JSON.stringify(user));
      }

      // 3. Update React state
      useAuthStore.getState().setAuth(user, token);

      return { success: true, data: { token, user } };
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || error.message || 'Login failed';
      return { success: false, error: errorMessage };
    }
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      await apiClient.post('/auth/logout');
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      // Notify Python to clear token
      if (isPyWebView()) {
        await window.pywebview.auth.on_logout();
      } else {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }

      // Clear React state
      useAuthStore.getState().logout();
      return { success: true };
    }
  }

  /**
   * Check authentication status
   */
  async checkAuth(): Promise<boolean> {
    try {
      if (isPyWebView()) {
        const result = await window.pywebview.auth.is_authenticated();
        if (result.authenticated) {
          const userResult = await window.pywebview.auth.get_current_user();
          const tokenResult = await window.pywebview.auth.get_token();
          if (userResult.user && tokenResult.token) {
            useAuthStore.getState().setAuth(userResult.user, tokenResult.token);
            return true;
          }
        }
        return false;
      } else {
        // Fallback for browser testing
        const token = localStorage.getItem('auth_token');
        const userJson = localStorage.getItem('auth_user');
        if (token && userJson) {
          useAuthStore.getState().setAuth(JSON.parse(userJson), token);
          return true;
        }
        return false;
      }
    } catch {
      return false;
    }
  }

  /**
   * Get token (for Axios interceptor)
   */
  async getToken(): Promise<string | null> {
    if (isPyWebView()) {
      const result = await window.pywebview.auth.get_token();
      return result.success ? result.token : null;
    }
    return localStorage.getItem('auth_token');
  }
}

export const authService = new AuthService();
