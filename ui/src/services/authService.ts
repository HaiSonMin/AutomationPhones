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
const isPyWebView = (): boolean => {
  return typeof window !== 'undefined' && 'pywebview' in window && window.pywebview !== undefined;
};

// Helper function to safely access pywebview API
const getPyWebViewAPI = () => {
  if (!isPyWebView()) return null;
  return window.pywebview?.api || null;
};

// Wait for pywebview API to be ready (listens for pywebviewready event)
const waitForPyWebView = (): Promise<boolean> => {
  return new Promise((resolve) => {
    const api = getPyWebViewAPI();

    // Check if already ready
    if (api && typeof api.auth_get_token === 'function') {
      resolve(true);
      return;
    }

    // Listen for pywebviewready event
    const onReady = () => {
      window.removeEventListener('pywebviewready', onReady);
      resolve(true);
    };

    window.addEventListener('pywebviewready', onReady);

    // Timeout after 5 seconds
    setTimeout(() => {
      window.removeEventListener('pywebviewready', onReady);
      const apiAfterTimeout = getPyWebViewAPI();
      if (apiAfterTimeout && typeof apiAfterTimeout.auth_get_token === 'function') {
        resolve(true);
      } else {
        resolve(false);
      }
    }, 5000);
  });
};

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

      console.log('user:::', user);

      // 2. Notify Python to save token (if running in PyWebView)
      const api = getPyWebViewAPI();
      if (api) {
        await api.auth_on_login_success(token, user);
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
      const api = getPyWebViewAPI();
      if (api) {
        await api.auth_on_logout();
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
      const api = getPyWebViewAPI();
      if (api) {
        // Wait for pywebview API to be ready
        const isReady = await waitForPyWebView();
        if (!isReady) {
          console.warn('PyWebView API not ready');
          return false;
        }

        const result = (await api.auth_is_authenticated()) as { authenticated: boolean };
        if (result.authenticated) {
          const userResult = (await api.auth_get_current_user()) as { success: boolean; user: any };
          const tokenResult = (await api.auth_get_token()) as { success: boolean; token: string };
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
    } catch (error) {
      console.error('checkAuth error:', error);
      return false;
    }
  }

  /**
   * Get token (for Axios interceptor)
   */
  async getToken(): Promise<string | null> {
    const api = getPyWebViewAPI();
    if (api) {
      const result = (await api.auth_get_token()) as { success: boolean; token: string | null };
      return result.success ? result.token : null;
    }
    return localStorage.getItem('auth_token');
  }
}

export const authService = new AuthService();
