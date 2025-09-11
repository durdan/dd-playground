import React from 'react';
import './CollapsibleSection.css';

const CollapsibleSection = ({ 
  id, 
  title, 
  children, 
  isExpanded, 
  onToggle,
  level = 2 
}) => {
  const handleToggle = () => {
    onToggle(id);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleToggle();
    }
  };

  const HeadingTag = `h${Math.min(level, 6)}`;

  return (
    <section className="collapsible-section" aria-labelledby={`${id}-heading`}>
      <HeadingTag id={`${id}-heading`} className="collapsible-section__header">
        <button
          className="collapsible-section__toggle"
          onClick={handleToggle}
          onKeyDown={handleKeyDown}
          aria-expanded={isExpanded}
          aria-controls={`${id}-content`}
          type="button"
        >
          <span 
            className={`collapsible-section__icon ${isExpanded ? 'expanded' : ''}`}
            aria-hidden="true"
          >
            ▶
          </span>
          <span className="collapsible-section__title">{title}</span>
        </button>
      </HeadingTag>
      
      <div
        id={`${id}-content`}
        className={`collapsible-section__content ${isExpanded ? 'expanded' : ''}`}
        aria-hidden={!isExpanded}
        role="region"
        aria-labelledby={`${id}-heading`}
      >
        {isExpanded && (
          <div className="collapsible-section__body">
            {children}
          </div>
        )}
      </div>
    </section>
  );
};

export default CollapsibleSection;