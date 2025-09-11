import React from 'react';
import './StatsDisplay.css';

export interface StatItem {
  label: string;
  value: string | number;
  change?: number;
  unit?: string;
}

export interface StatsSection {
  title: string;
  stats: StatItem[];
}

interface StatsDisplayProps {
  sections: StatsSection[];
  title?: string;
  loading?: boolean;
}

export const StatsDisplay: React.FC<StatsDisplayProps> = ({ 
  sections, 
  title, 
  loading = false 
}) => {
  const formatValue = (value: string | number, unit?: string): string => {
    const formattedValue = typeof value === 'number' ? value.toLocaleString() : value;
    return unit ? `${formattedValue} ${unit}` : formattedValue;
  };

  const getChangeColor = (change: number): string => {
    if (change > 0) return 'change-positive';
    if (change < 0) return 'change-negative';
    return 'change-neutral';
  };

  const formatChange = (change: number): string => {
    const sign = change > 0 ? '+' : '';
    return `${sign}${change}%`;
  };

  if (loading) {
    return (
      <div className="stats-display">
        {title && <h3 className="stats-title">{title}</h3>}
        <div className="stats-loading">Loading statistics...</div>
      </div>
    );
  }

  if (!sections.length) {
    return (
      <div className="stats-display">
        {title && <h3 className="stats-title">{title}</h3>}
        <div className="stats-empty">No statistics available</div>
      </div>
    );
  }

  return (
    <div className="stats-display">
      {title && <h3 className="stats-title">{title}</h3>}
      
      {sections.map((section, sectionIndex) => (
        <div key={sectionIndex} className="stats-section">
          <h4 className="section-title">{section.title}</h4>
          
          <div className="stats-grid">
            {section.stats.map((stat, statIndex) => (
              <div key={statIndex} className="stat-item">
                <div className="stat-label">{stat.label}</div>
                <div className="stat-value">
                  {formatValue(stat.value, stat.unit)}
                  {stat.change !== undefined && (
                    <span className={`stat-change ${getChangeColor(stat.change)}`}>
                      {formatChange(stat.change)}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};