import React, { useState } from 'react';
import MessageBase from './MessageBase';
import './SpecPreview.css';

const SpecPreview = ({ 
  spec, 
  timestamp, 
  title = 'Specification Preview',
  language = 'json',
  collapsible = true 
}) => {
  const [isExpanded, setIsExpanded] = useState(!collapsible);

  if (!spec) {
    throw new Error('Spec content is required');
  }

  const formatSpec = (specData) => {
    if (typeof specData === 'string') return specData;
    return JSON.stringify(specData, null, 2);
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(formatSpec(spec));
    } catch (err) {
      console.error('Failed to copy spec:', err);
    }
  };

  return (
    <MessageBase type="spec-preview" timestamp={timestamp}>
      <div className="spec-preview">
        <div className="spec-header">
          <div className="spec-title">
            {collapsible && (
              <button 
                className="expand-toggle"
                onClick={() => setIsExpanded(!isExpanded)}
                aria-label={isExpanded ? 'Collapse' : 'Expand'}
              >
                {isExpanded ? '▼' : '▶'}
              </button>
            )}
            <span>{title}</span>
            <span className="spec-language">{language}</span>
          </div>
          <button 
            className="copy-button"
            onClick={copyToClipboard}
            title="Copy to clipboard"
          >
            📋
          </button>
        </div>
        {isExpanded && (
          <div className="spec-content">
            <pre className={`language-${language}`}>
              <code>{formatSpec(spec)}</code>
            </pre>
          </div>
        )}
      </div>
    </MessageBase>
  );
};

export default SpecPreview;