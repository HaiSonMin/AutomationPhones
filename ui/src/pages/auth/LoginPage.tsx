import { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';
import { useAuthStore } from '../../stores/authStore';
import { useThemeStore } from '../../stores/themeStore';
import { Button, Input, PasswordInput } from '../../components';
import { LoadingOutlined, LoginOutlined } from '@ant-design/icons';

// Validation schema
const loginSchema = z.object({
  user_email: z.string().min(1, 'Email is required').email('Invalid email format'),
  user_password: z.string().min(1, 'Password is required'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const setAuthLoading = useAuthStore((state) => state.setLoading);
  const { mode: themeMode } = useThemeStore();
  const isDark = themeMode === 'dark';

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      user_email: 'hson22102000@gmail.com',
      user_password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setAuthLoading(true);
    setError('');

    try {
      const result = await authService.login({
        user_email: data.user_email,
        user_password: data.user_password,
      });

      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setIsLoading(false);
      setAuthLoading(false);
    }
  };

  return (
    <div
      className={`min-h-screen flex items-center justify-center p-4 ${
        isDark
          ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900'
          : 'bg-gradient-to-br from-blue-50 via-white to-purple-50'
      }`}
    >
      <div className='w-full max-w-md'>
        {/* Logo & Title */}
        <div className='text-center mb-8'>
          <div className='inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mb-4 shadow-lg'>
            <svg
              className='w-8 h-8 text-white'
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
          <h1 className={`text-3xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
            Phone Manager
          </h1>
          <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>
            Automation Tool - Desktop Application
          </p>
        </div>

        {/* Login Card */}
        <div
          className={`rounded-2xl shadow-xl p-8 border ${
            isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-100'
          }`}
        >
          <h2 className={`text-2xl font-semibold mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
            Sign In
          </h2>

          {/* Error Message */}
          {error && (
            <div
              className={`mb-6 p-4 border rounded-lg flex items-start gap-3 ${
                isDark ? 'bg-red-900/30 border-red-800' : 'bg-red-50 border-red-200'
              }`}
            >
              <svg
                className='w-5 h-5 text-red-500 mt-0.5 flex-shrink-0'
                fill='currentColor'
                viewBox='0 0 20 20'
              >
                <path
                  fillRule='evenodd'
                  d='M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z'
                  clipRule='evenodd'
                />
              </svg>
              <div className='flex-1'>
                <p className={`text-sm font-medium ${isDark ? 'text-red-400' : 'text-red-800'}`}>
                  {error}
                </p>
              </div>
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleSubmit(onSubmit)} className='space-y-5'>
            {/* Email Field */}
            <Controller
              name='user_email'
              control={control}
              render={({ field }) => (
                <Input
                  {...field}
                  label='Email'
                  placeholder='Enter your email'
                  error={errors.user_email?.message}
                  disabled={isLoading}
                  type='email'
                />
              )}
            />

            {/* Password Field */}
            <Controller
              name='user_password'
              control={control}
              render={({ field }) => (
                <PasswordInput
                  {...field}
                  label='Password'
                  placeholder='Enter your password'
                  error={errors.user_password?.message}
                  disabled={isLoading}
                />
              )}
            />

            {/* Submit Button */}
            <Button
              variant='primary'
              htmlType='submit'
              loading={isLoading}
              disabled={isLoading}
              fullWidth
              icon={isLoading ? <LoadingOutlined /> : <LoginOutlined />}
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>

          {/* Footer */}
          <div className={`mt-6 pt-6 border-t ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
            <p className={`text-center text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              API Server: <span className='font-mono text-blue-500'>localhost:9000</span>
            </p>
          </div>
        </div>

        {/* Additional Info */}
        <div className='mt-6 text-center'>
          <p className={`text-sm ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>
            Secure authentication powered by Python Keyring
          </p>
        </div>
      </div>
    </div>
  );
}
