import React from 'react';
import { cn } from '../../lib/utils';

interface MessageBaseProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'user' | 'system' | 'spec' | 'loading';
  timestamp?: Date;
  role?: string;
}

export const MessageBase: React.FC<MessageBaseProps> = ({
  children,
  className,
  variant = 'system',
  timestamp,
  role
}) => {
  const baseClasses = "flex flex-col gap-2 p-4 rounded-lg max-w-4xl";
  
  const variantClasses = {
    user: "bg-blue-50 border-l-4 border-blue-500 ml-auto",
    system: "bg-gray-50 border-l-4 border-gray-400",
    spec: "bg-slate-50 border border-slate-200",
    loading: "bg-yellow-50 border-l-4 border-yellow-400"
  };

  return (
    <div
      className={cn(baseClasses, variantClasses[variant], className)}
      role={role || "article"}
      aria-label={`${variant} message`}
    >
      {children}
      {timestamp && (
        <time 
          className="text-xs text-gray-500 mt-2"
          dateTime={timestamp.toISOString()}
          aria-label={`Sent at ${timestamp.toLocaleString()}`}
        >
          {timestamp.toLocaleTimeString()}
        </time>
      )}
    </div>
  );
};