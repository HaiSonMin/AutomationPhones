import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { ConfigProvider, theme } from 'antd';
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import { MonitoringPage } from './pages/devices/monitoring';
import { authService } from './services/authService';
import { useThemeStore } from './stores/themeStore';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const [isChecking, setIsChecking] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const themeMode = useThemeStore((state) => state.mode);

  useEffect(() => {
    authService.checkAuth().then((isAuth) => {
      setIsAuthenticated(isAuth);
      setIsChecking(false);
    });
  }, []);

  if (isChecking) {
    return (
      <div
        className='min-h-screen flex items-center justify-center'
        style={{
          background: themeMode === 'dark' ? '#141414' : '#f5f5f5',
        }}
      >
        <div className='text-center'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600'></div>
          <p className='mt-4' style={{ color: themeMode === 'dark' ? '#ffffff' : '#666666' }}>
            Loading...
          </p>
        </div>
      </div>
    );
  }

  return isAuthenticated ? <>{children}</> : <Navigate to='/login' replace />;
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const [isChecking, setIsChecking] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const themeMode = useThemeStore((state) => state.mode);

  useEffect(() => {
    authService.checkAuth().then((isAuth) => {
      setIsAuthenticated(isAuth);
      setIsChecking(false);
    });
  }, []);

  if (isChecking) {
    return (
      <div
        className='min-h-screen flex items-center justify-center'
        style={{
          background: themeMode === 'dark' ? '#141414' : '#f5f5f5',
        }}
      >
        <div className='text-center'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600'></div>
        </div>
      </div>
    );
  }

  return !isAuthenticated ? <>{children}</> : <Navigate to='/dashboard' replace />;
}

function App() {
  const themeMode = useThemeStore((state) => state.mode);

  return (
    <ConfigProvider
      theme={{
        algorithm: themeMode === 'dark' ? theme.darkAlgorithm : theme.defaultAlgorithm,
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
      }}
    >
      <BrowserRouter>
        <Routes>
          <Route
            path='/login'
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path='/dashboard'
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/devices/monitor'
            element={
              <ProtectedRoute>
                <MonitoringPage />
              </ProtectedRoute>
            }
          />
          <Route path='/' element={<Navigate to='/dashboard' replace />} />
          <Route path='*' element={<Navigate to='/dashboard' replace />} />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
