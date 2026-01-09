import React from 'react';
import { Input as AntInput, type InputProps as AntInputProps } from 'antd';
import { cn } from '../../lib/utils';

export interface CustomInputProps extends AntInputProps {
  label?: string;
  error?: string;
  fullWidth?: boolean;
  className?: string;
}

export const Input: React.FC<CustomInputProps> = ({
  label,
  error,
  fullWidth = true,
  className,
  ...props
}) => {
  return (
    <div className={cn('space-y-2', fullWidth && 'w-full')}>
      {label && <label className='block text-sm font-medium text-gray-700'>{label}</label>}
      <AntInput
        {...props}
        status={error ? 'error' : undefined}
        className={cn('h-12 rounded-lg', error && 'border-red-300', className)}
      />
      {error && <p className='text-sm text-red-600 mt-1.5'>{error}</p>}
    </div>
  );
};

export const PasswordInput: React.FC<CustomInputProps> = ({
  label,
  error,
  fullWidth = true,
  className,
  ...props
}) => {
  return (
    <div className={cn('space-y-2', fullWidth && 'w-full')}>
      {label && <label className='block text-sm font-medium text-gray-700'>{label}</label>}
      <AntInput.Password
        {...props}
        status={error ? 'error' : undefined}
        className={cn('h-12 rounded-lg', error && 'border-red-300', className)}
      />
      {error && <p className='text-sm text-red-600 mt-1.5'>{error}</p>}
    </div>
  );
};
