import React from 'react';
import { SpecType } from './types';
import './SpecTypeSelector.css';

interface SpecTypeSelectorProps {
  specTypes: SpecType[];
  selectedSpecType: string;
  onSpecTypeChange: (specTypeId: string) => void;
  disabled?: boolean;
}

export const SpecTypeSelector: React.FC<SpecTypeSelectorProps> = ({
  specTypes,
  selectedSpecType,
  onSpecTypeChange,
  disabled = false
}) => {
  return (
    <div className="spec-type-selector">
      <label 
        htmlFor="spec-type-select"
        className="spec-type-selector__label"
      >
        Specification Type:
      </label>
      <select
        id="spec-type-select"
        className="spec-type-selector__select"
        value={selectedSpecType}
        onChange={(e) => onSpecTypeChange(e.target.value)}
        disabled={disabled}
        aria-describedby="spec-type-description"
      >
        {specTypes.map((specType) => (
          <option key={specType.id} value={specType.id}>
            {specType.label}
          </option>
        ))}
      </select>
      <div 
        id="spec-type-description"
        className="spec-type-selector__description"
      >
        {specTypes.find(s => s.id === selectedSpecType)?.description}
      </div>
    </div>
  );
};