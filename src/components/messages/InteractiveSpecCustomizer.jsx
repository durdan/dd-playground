import React, { useState } from 'react';
import MessageBase from './MessageBase';
import './InteractiveSpecCustomizer.css';

const InteractiveSpecCustomizer = ({ 
  spec, 
  timestamp, 
  onSpecChange,
  customizableFields = [],
  title = 'Customize Specification'
}) => {
  const [localSpec, setLocalSpec] = useState(spec || {});
  const [hasChanges, setHasChanges] = useState(false);

  if (!onSpecChange) {
    throw new Error('onSpecChange callback is required');
  }

  const handleFieldChange = (fieldPath, value) => {
    const newSpec = { ...localSpec };
    setNestedValue(newSpec, fieldPath, value);
    setLocalSpec(newSpec);
    setHasChanges(true);
  };

  const setNestedValue = (obj, path, value) => {
    const keys = path.split('.');
    let current = obj;
    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) current[keys[i]] = {};
      current = current[keys[i]];
    }
    current[keys[keys.length - 1]] = value;
  };

  const getNestedValue = (obj, path) => {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  };

  const applyChanges = () => {
    onSpecChange(localSpec);
    setHasChanges(false);
  };

  const resetChanges = () => {
    setLocalSpec(spec);
    setHasChanges(false);
  };

  const renderField = (field) => {
    const { path, label, type = 'text', options = [] } = field;
    const value = getNestedValue(localSpec, path) || '';

    switch (type) {
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => handleFieldChange(path, e.target.value)}
          >
            {options.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      
      case 'boolean':
        return (
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={Boolean(value)}
              onChange={(e) => handleFieldChange(path, e.target.checked)}
            />
            <span className="toggle-slider"></span>
          </label>
        );
      
      case 'number':
        return (
          <input
            type="number"
            value={value}
            onChange={(e) => handleFieldChange(path, Number(e.target.value))}
          />
        );
      
      default:
        return (
          <input
            type="text"
            value={value}
            onChange={(e) => handleFieldChange(path, e.target.value)}
          />
        );
    }
  };

  return (
    <MessageBase type="interactive" timestamp={timestamp}>
      <div className="spec-customizer">
        <div className="customizer-header">
          <h3>{title}</h3>
          {hasChanges && <span className="changes-indicator">●</span>}
        </div>
        
        <div className="customizer-fields">
          {customizableFields.map((field, index) => (
            <div key={index} className="field-group">
              <label className="field-label">{field.label}</label>
              <div className="field-input">
                {renderField(field)}
              </div>
            </div>
          ))}
        </div>

        <div className="customizer-actions">
          <button 
            className="reset-button"
            onClick={resetChanges}
            disabled={!hasChanges}
          >
            Reset
          </button>
          <button 
            className="apply-button"
            onClick={applyChanges}
            disabled={!hasChanges}
          >
            Apply Changes
          </button>
        </div>
      </div>
    </MessageBase>
  );
};

export default InteractiveSpecCustomizer;