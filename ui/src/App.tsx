import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { ConfigProvider, theme } from 'antd';
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import MonitoringPage from './pages/devices/monitoring/MonitoringPage';
import { authService } from './services/authService';
import { useThemeStore } from './stores/themeStore';

// Phone Tasks
import PhoneSetupPage from './pages/tasks/phone/setup/SetupPage';
import PhoneAppClonePage from './pages/tasks/phone/appclone/AppClonePage';

// Threads Tasks
import ThreadsNewsPage from './pages/tasks/threads/posts/news/NewsPage';
import ThreadsReelsPage from './pages/tasks/threads/posts/reels/ReelsPage';
import ThreadsSquarePage from './pages/tasks/threads/posts/square/SquarePage';
import ThreadsStoriesPage from './pages/tasks/threads/posts/stories/StoriesPage';
import ThreadsDynamicPage from './pages/tasks/threads/interacts/dynamic/DynamicPage';

// Instagram Tasks
import InstagramStoriesPage from './pages/tasks/instagrams/posts/stories/StoriesPage';
import InstagramSquarePage from './pages/tasks/instagrams/posts/square/SquarePage';
import InstagramReelsPage from './pages/tasks/instagrams/posts/reels/ReelsPage';
import InstagramNewsPage from './pages/tasks/instagrams/posts/news/NewsPage';
import InstagramDynamicPage from './pages/tasks/instagrams/interacts/dynamic/DynamicPage';

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
          {/* Phone Tasks */}
          <Route
            path='/tasks/phone/setup'
            element={
              <ProtectedRoute>
                <PhoneSetupPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/phone/appclone'
            element={
              <ProtectedRoute>
                <PhoneAppClonePage />
              </ProtectedRoute>
            }
          />
          {/* Threads Tasks */}
          <Route
            path='/tasks/threads/posts/news'
            element={
              <ProtectedRoute>
                <ThreadsNewsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/threads/posts/reels'
            element={
              <ProtectedRoute>
                <ThreadsReelsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/threads/posts/square'
            element={
              <ProtectedRoute>
                <ThreadsSquarePage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/threads/posts/stories'
            element={
              <ProtectedRoute>
                <ThreadsStoriesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/threads/interacts/dynamic'
            element={
              <ProtectedRoute>
                <ThreadsDynamicPage />
              </ProtectedRoute>
            }
          />
          {/* Instagram Tasks */}
          <Route
            path='/tasks/instagrams/posts/stories'
            element={
              <ProtectedRoute>
                <InstagramStoriesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/instagrams/posts/square'
            element={
              <ProtectedRoute>
                <InstagramSquarePage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/instagrams/posts/reels'
            element={
              <ProtectedRoute>
                <InstagramReelsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/instagrams/posts/news'
            element={
              <ProtectedRoute>
                <InstagramNewsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/tasks/instagrams/interacts/dynamic'
            element={
              <ProtectedRoute>
                <InstagramDynamicPage />
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
