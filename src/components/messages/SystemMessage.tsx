import React from 'react';
import { MessageBase } from './MessageBase';
import { SystemMessage as SystemMessageType } from './types';
import { Bot, Info, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

interface SystemMessageProps {
  message: SystemMessageType;
}

const variantConfig = {
  info: {
    icon: Info,
    iconColor: 'text-blue-500',
    titleColor: 'text-blue-900'
  },
  success: {
    icon: CheckCircle,
    iconColor: 'text-green-500',
    titleColor: 'text-green-900'
  },
  warning: {
    icon: AlertTriangle,
    iconColor: 'text-yellow-500',
    titleColor: 'text-yellow-900'
  },
  error: {
    icon: XCircle,
    iconColor: 'text-red-500',
    titleColor: 'text-red-900'
  }
};

export const SystemMessage: React.FC<SystemMessageProps> = ({ message }) => {
  const variant = message.variant || 'info';
  const config = variantConfig[variant];
  const Icon = config.icon;

  return (
    <MessageBase 
      variant="system" 
      timestamp={message.timestamp}
      role="article"
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-gray-500 rounded-full flex items-center justify-center">
            <Bot className="w-4 h-4 text-white" aria-hidden="true" />
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <div className={`text-sm font-medium mb-1 flex items-center gap-2 ${config.titleColor}`}>
            <Icon className={`w-4 h-4 ${config.iconColor}`} aria-hidden="true" />
            Assistant
          </div>
          <div className="text-gray-800 whitespace-pre-wrap break-words">
            {message.content}
          </div>
        </div>
      </div>
    </MessageBase>
  );
};