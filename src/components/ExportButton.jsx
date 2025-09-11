import React, { useState } from 'react';
import './ExportButton.css';

const ExportButton = ({ onExport, disabled = false, loading = false }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleExport = (format) => {
    onExport(format);
    setIsOpen(false);
  };

  const handleKeyDown = (event, format) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleExport(format);
    }
  };

  return (
    <div className="export-button" role="group" aria-label="Export options">
      <button
        className="export-button__trigger"
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled}
        aria-expanded={isOpen}
        aria-haspopup="menu"
        type="button"
      >
        {loading ? '⏳ Exporting...' : '📤 Export'}
      </button>
      
      {isOpen && (
        <div className="export-button__menu" role="menu">
          <button
            className="export-button__option"
            onClick={() => handleExport('pdf')}
            onKeyDown={(e) => handleKeyDown(e, 'pdf')}
            disabled={disabled}
            role="menuitem"
            type="button"
          >
            📄 Export as PDF
          </button>
          <button
            className="export-button__option"
            onClick={() => handleExport('json')}
            onKeyDown={(e) => handleKeyDown(e, 'json')}
            disabled={disabled}
            role="menuitem"
            type="button"
          >
            📋 Export as JSON
          </button>
        </div>
      )}
    </div>
  );
};

export default ExportButton;