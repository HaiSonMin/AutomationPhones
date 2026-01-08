import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { authService } from '../services/authService';

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, logout: logoutStore } = useAuthStore();

  useEffect(() => {
    // Verify authentication on mount
    authService.checkAuth().then((isAuth) => {
      if (!isAuth) {
        navigate('/login');
      }
    });
  }, [navigate]);

  const handleLogout = async () => {
    await authService.logout();
    navigate('/login');
  };

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <header className='bg-white shadow-sm border-b border-gray-200'>
        <div className='mx-auto px-4 sm:px-6 lg:px-8 py-4'>
          <div className='flex items-center justify-between'>
            <div className='flex items-center gap-3'>
              <div className='w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center'>
                <svg
                  className='w-6 h-6 text-white'
                  fill='none'
                  stroke='currentColor'
                  viewBox='0 0 24 24'
                >
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth={2}
                    d='M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z'
                  />
                </svg>
              </div>
              <div>
                <h1 className='text-xl font-bold text-gray-900'>Phone Manager</h1>
                <p className='text-sm text-gray-500'>Automation Tool</p>
              </div>
            </div>

            <div className='flex items-center gap-4'>
              {/* User Info */}
              <div className='flex items-center gap-3'>
                <div className='text-right'>
                  <p className='text-sm font-medium text-gray-900'>
                    {user?.user_fullName || 'User'}
                  </p>
                  <p className='text-xs text-gray-500'>{user?.user_email || ''}</p>
                </div>
                <div className='w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center'>
                  <span className='text-white font-semibold text-sm'>
                    {user?.user_fullName?.charAt(0).toUpperCase() || 'U'}
                  </span>
                </div>
              </div>

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className='px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2'
              >
                <svg className='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth={2}
                    d='M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1'
                  />
                </svg>
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className='mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {/* Welcome Card */}
        <div className='bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl shadow-xl p-8 text-white mb-8'>
          <h2 className='text-3xl font-bold mb-2'>
            Welcome back, {user?.user_fullName?.split(' ')[0] || 'User'}! 👋
          </h2>
          <p className='text-blue-100'>Your automation tool is ready to use</p>
        </div>

        {/* Stats Grid */}
        <div className='grid grid-cols-1 md:grid-cols-3 gap-6 mb-8'>
          <div className='bg-white rounded-xl shadow-sm p-6 border border-gray-200'>
            <div className='flex items-center justify-between mb-4'>
              <div className='w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center'>
                <svg
                  className='w-6 h-6 text-blue-600'
                  fill='none'
                  stroke='currentColor'
                  viewBox='0 0 24 24'
                >
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth={2}
                    d='M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z'
                  />
                </svg>
              </div>
            </div>
            <h3 className='text-2xl font-bold text-gray-900 mb-1'>0</h3>
            <p className='text-sm text-gray-600'>Connected Devices</p>
          </div>

          <div className='bg-white rounded-xl shadow-sm p-6 border border-gray-200'>
            <div className='flex items-center justify-between mb-4'>
              <div className='w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center'>
                <svg
                  className='w-6 h-6 text-green-600'
                  fill='none'
                  stroke='currentColor'
                  viewBox='0 0 24 24'
                >
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth={2}
                    d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
                  />
                </svg>
              </div>
            </div>
            <h3 className='text-2xl font-bold text-gray-900 mb-1'>0</h3>
            <p className='text-sm text-gray-600'>Active Tasks</p>
          </div>

          <div className='bg-white rounded-xl shadow-sm p-6 border border-gray-200'>
            <div className='flex items-center justify-between mb-4'>
              <div className='w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center'>
                <svg
                  className='w-6 h-6 text-purple-600'
                  fill='none'
                  stroke='currentColor'
                  viewBox='0 0 24 24'
                >
                  <path
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth={2}
                    d='M13 10V3L4 14h7v7l9-11h-7z'
                  />
                </svg>
              </div>
            </div>
            <h3 className='text-2xl font-bold text-gray-900 mb-1'>Ready</h3>
            <p className='text-sm text-gray-600'>System Status</p>
          </div>
        </div>

        {/* Info Card */}
        <div className='bg-white rounded-xl shadow-sm p-6 border border-gray-200'>
          <h3 className='text-lg font-semibold text-gray-900 mb-4'>
            🎉 Authentication Successful!
          </h3>
          <div className='space-y-3'>
            <div className='flex items-center gap-2 text-sm'>
              <svg className='w-5 h-5 text-green-600' fill='currentColor' viewBox='0 0 20 20'>
                <path
                  fillRule='evenodd'
                  d='M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z'
                  clipRule='evenodd'
                />
              </svg>
              <span className='text-gray-700'>Token securely stored in Python Keyring</span>
            </div>
            <div className='flex items-center gap-2 text-sm'>
              <svg className='w-5 h-5 text-green-600' fill='currentColor' viewBox='0 0 20 20'>
                <path
                  fillRule='evenodd'
                  d='M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z'
                  clipRule='evenodd'
                />
              </svg>
              <span className='text-gray-700'>Connected to API server (localhost:9000)</span>
            </div>
            <div className='flex items-center gap-2 text-sm'>
              <svg className='w-5 h-5 text-green-600' fill='currentColor' viewBox='0 0 20 20'>
                <path
                  fillRule='evenodd'
                  d='M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z'
                  clipRule='evenodd'
                />
              </svg>
              <span className='text-gray-700'>PyWebView bridge active</span>
            </div>
          </div>

          <div className='mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg'>
            <p className='text-sm text-blue-800'>
              <strong>Next steps:</strong> You can now add your automation features here. The
              authentication system is fully functional with secure token storage.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
