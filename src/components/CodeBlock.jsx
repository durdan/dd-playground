import React, { useEffect, useRef, useState } from 'react';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-json';
import 'prismjs/components/prism-yaml';
import './CodeBlock.css';

const CodeBlock = ({ code, language = 'javascript', title }) => {
  const codeRef = useRef(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (codeRef.current) {
      Prism.highlightElement(codeRef.current);
    }
  }, [code, language]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy code:', error);
    }
  };

  return (
    <div className="code-block" role="region" aria-label={`Code block${title ? `: ${title}` : ''}`}>
      <div className="code-block__header">
        {title && <span className="code-block__title">{title}</span>}
        <span className="code-block__language">{language}</span>
        <button
          className="code-block__copy"
          onClick={handleCopy}
          aria-label="Copy code to clipboard"
          type="button"
        >
          {copied ? '✓ Copied' : '📋 Copy'}
        </button>
      </div>
      
      <pre className="code-block__pre">
        <code
          ref={codeRef}
          className={`language-${language} code-block__code`}
          aria-label={`${language} code`}
        >
          {code}
        </code>
      </pre>
    </div>
  );
};

export default CodeBlock;