import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios';
import { authService } from '../services/authService';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:9000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

// Request interceptor - Add token from Python keyring
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const token = await authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - Handle 401
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      await authService.logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
