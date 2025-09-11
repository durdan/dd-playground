import React, { forwardRef, ButtonHTMLAttributes } from 'react';
import { cn } from '../../utils/cn';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    className, 
    variant = 'primary', 
    size = 'md', 
    loading = false,
    leftIcon,
    rightIcon,
    children, 
    disabled,
    ...props 
  }, ref) => {
    const baseStyles = `
      inline-flex items-center justify-center gap-2 font-medium 
      transition-all duration-200 ease-in-out
      focus:outline-none focus:ring-2 focus:ring-offset-2
      disabled:opacity-50 disabled:cursor-not-allowed
      relative overflow-hidden
    `;

    const variants = {
      primary: `
        bg-blue-600 text-white hover:bg-blue-700 
        focus:ring-blue-500 active:bg-blue-800
        shadow-sm hover:shadow-md
      `,
      secondary: `
        bg-gray-100 text-gray-900 hover:bg-gray-200 
        focus:ring-gray-500 active:bg-gray-300
        shadow-sm hover:shadow-md
      `,
      outline: `
        border border-gray-300 bg-white text-gray-700 
        hover:bg-gray-50 focus:ring-blue-500 active:bg-gray-100
        shadow-sm hover:shadow-md
      `,
      ghost: `
        text-gray-700 hover:bg-gray-100 
        focus:ring-gray-500 active:bg-gray-200
      `,
      danger: `
        bg-red-600 text-white hover:bg-red-700 
        focus:ring-red-500 active:bg-red-800
        shadow-sm hover:shadow-md
      `
    };

    const sizes = {
      sm: 'px-3 py-1.5 text-sm rounded-md',
      md: 'px-4 py-2 text-sm rounded-lg',
      lg: 'px-6 py-3 text-base rounded-lg'
    };

    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          loading && 'cursor-wait',
          className
        )}
        disabled={disabled || loading}
        aria-busy={loading}
        {...props}
      >
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
          </div>
        )}
        
        <span className={cn('flex items-center gap-2', loading && 'opacity-0')}>
          {leftIcon && <span className="flex-shrink-0">{leftIcon}</span>}
          {children}
          {rightIcon && <span className="flex-shrink-0">{rightIcon}</span>}
        </span>
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button };