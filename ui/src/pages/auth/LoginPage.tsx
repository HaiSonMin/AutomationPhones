import { LoadingOutlined, LoginOutlined } from '@ant-design/icons';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { z } from 'zod';
import { Button, Input, PasswordInput } from '../../components';
import { authService } from '../../services/authService';
import { useAuthStore } from '../../stores/authStore';

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
    <div className='relative min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50'>
      {/* Decorative gradient blobs */}
      <div className='absolute top-20 left-10 w-72 h-72 bg-blue-400/20 rounded-full blur-3xl' />
      <div className='absolute bottom-20 right-10 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl' />
      <div className='absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-300/10 rounded-full blur-3xl' />

      <div className='relative z-10 w-full max-w-md'>
        {/* Logo & Title */}
        <div className='text-center mb-8'>
          <div className='inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-3xl mb-6 shadow-2xl shadow-blue-500/30'>
            <svg
              className='w-10 h-10 text-white'
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
          <h1 className='text-4xl font-bold mb-3 bg-gradient-to-r from-gray-900 via-blue-800 to-purple-900 bg-clip-text text-transparent'>
            Phone Manager
          </h1>
          <p className='text-gray-600 font-medium'>Automation Tool - Desktop Application</p>
        </div>

        {/* Login Card */}
        <div className='rounded-3xl shadow-2xl p-8 border bg-white/80 backdrop-blur-xl border-gray-200'>
          <h2 className='text-2xl font-bold mb-6 text-gray-900'>Sign In</h2>

          {/* Error Message */}
          {error && (
            <div className='mb-6 p-4 border rounded-xl flex items-start gap-3 bg-red-50 border-red-200'>
              <svg
                className='w-5 h-5 text-red-600 mt-0.5 shrink-0'
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
                <p className='text-sm font-semibold text-red-800'>{error}</p>
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
              className='mt-2'
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
