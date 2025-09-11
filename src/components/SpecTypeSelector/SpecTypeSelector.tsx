import React from 'react';
import { SpecType } from '../../types/chat';
import styles from './SpecTypeSelector.module.css';

interface SpecTypeSelectorProps {
  currentSpecType: SpecType;
  onSpecTypeChange: (specType: SpecType) => void;
  disabled?: boolean;
}

const SPEC_TYPES: { value: SpecType; label: string }[] = [
  { value: 'general', label: 'General' },
  { value: 'technical', label: 'Technical' },
  { value: 'creative', label: 'Creative' },
  { value: 'analytical', label: 'Analytical' }
];

export const SpecTypeSelector: React.FC<SpecTypeSelectorProps> = ({
  currentSpecType,
  onSpecTypeChange,
  disabled = false
}) => {
  return (
    <div className={styles.container}>
      <label htmlFor="spec-type-select" className={styles.label}>
        Mode:
      </label>
      <select
        id="spec-type-select"
        value={currentSpecType}
        onChange={(e) => onSpecTypeChange(e.target.value as SpecType)}
        disabled={disabled}
        className={styles.select}
      >
        {SPEC_TYPES.map(({ value, label }) => (
          <option key={value} value={value}>
            {label}
          </option>
        ))}
      </select>
    </div>
  );
};