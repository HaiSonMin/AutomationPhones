import React from 'react';
import { Button as AntButton } from 'antd';
import type { ButtonProps as AntButtonProps } from 'antd';
import { cn } from '../../lib/utils';

export interface ButtonProps extends Omit<AntButtonProps, 'type' | 'variant'> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  fullWidth = false,
  className,
  children,
  ...props
}) => {
  const variantClasses = {
    primary:
      'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 border-0 text-white shadow-lg hover:shadow-xl',
    secondary: 'bg-gray-600 hover:bg-gray-700 border-0 text-white',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50',
    ghost: 'border-0 text-blue-600 hover:bg-blue-50',
    danger: 'bg-red-600 hover:bg-red-700 border-0 text-white',
  };

  return (
    <AntButton
      {...props}
      className={cn(
        'h-12 py-5 font-semibold rounded-lg transition-all duration-200',
        variantClasses[variant],
        fullWidth && 'w-full',
        className
      )}
    >
      {children}
    </AntButton>
  );
};
