import React, { useState } from 'react';
import { MessageBase } from './MessageBase';
import { SpecPreview as SpecPreviewType } from './types';
import { Code, ChevronDown, ChevronRight, Copy, Check } from 'lucide-react';

interface SpecPreviewProps {
  message: SpecPreviewType;
}

export const SpecPreview: React.FC<SpecPreviewProps> = ({ message }) => {
  const [isExpanded, setIsExpanded] = useState(!message.isCollapsible);
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const toggleExpanded = () => {
    if (message.isCollapsible) {
      setIsExpanded(!isExpanded);
    }
  };

  return (
    <MessageBase 
      variant="spec" 
      timestamp={message.timestamp}
      role="article"
    >
      <div className="flex items-center justify-between mb-2">
        <div 
          className={`flex items-center gap-2 ${message.isCollapsible ? 'cursor-pointer' : ''}`}
          onClick={toggleExpanded}
          role={message.isCollapsible ? 'button' : undefined}
          tabIndex={message.isCollapsible ? 0 : undefined}
          onKeyDown={(e) => {
            if (message.isCollapsible && (e.key === 'Enter' || e.key === ' ')) {
              e.preventDefault();
              toggleExpanded();
            }
          }}
          aria-expanded={message.isCollapsible ? isExpanded : undefined}
          aria-label={message.isCollapsible ? `${isExpanded ? 'Collapse' : 'Expand'} code preview` : undefined}
        >
          {message.isCollapsible && (
            isExpanded ? 
              <ChevronDown className="w-4 h-4 text-gray-500" aria-hidden="true" /> : 
              <ChevronRight className="w-4 h-4 text-gray-500" aria-hidden="true" />
          )}
          <Code className="w-4 h-4 text-slate-600" aria-hidden="true" />
          <span className="text-sm font-medium text-slate-700">
            {message.filename || `${message.language} Code`}
          </span>
          <span className="text-xs text-slate-500 bg-slate-200 px-2 py-1 rounded">
            {message.language}
          </span>
        </div>
        
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 px-2 py-1 text-xs text-slate-600 hover:text-slate-800 hover:bg-slate-200 rounded transition-colors"
          aria-label="Copy code to clipboard"
        >
          {isCopied ? (
            <>
              <Check className="w-3 h-3" aria-hidden="true" />
              Copied
            </>
          ) : (
            <>
              <Copy className="w-3 h-3" aria-hidden="true" />
              Copy
            </>
          )}
        </button>
      </div>

      {isExpanded && (
        <div className="relative">
          <pre className="bg-slate-900 text-slate-100 p-4 rounded-md overflow-x-auto text-sm">
            <code className={`language-${message.language}`}>
              {message.content}
            </code>
          </pre>
        </div>
      )}
    </MessageBase>
  );
};