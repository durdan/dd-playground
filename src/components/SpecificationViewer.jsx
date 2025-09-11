import React, { useState, useCallback } from 'react';
import CollapsibleSection from './CollapsibleSection';
import ExportButton from './ExportButton';
import SpecificationContent from './SpecificationContent';
import { exportToPDF, exportToJSON } from '../utils/exportUtils';
import './SpecificationViewer.css';

const SpecificationViewer = ({ specification, title = "Specification" }) => {
  const [expandedSections, setExpandedSections] = useState(new Set());
  const [isExporting, setIsExporting] = useState(false);

  const toggleSection = useCallback((sectionId) => {
    setExpandedSections(prev => {
      const newSet = new Set(prev);
      if (newSet.has(sectionId)) {
        newSet.delete(sectionId);
      } else {
        newSet.add(sectionId);
      }
      return newSet;
    });
  }, []);

  const handleExport = useCallback(async (format) => {
    if (!specification) return;
    
    setIsExporting(true);
    try {
      if (format === 'pdf') {
        await exportToPDF(specification, title);
      } else if (format === 'json') {
        exportToJSON(specification, title);
      }
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setIsExporting(false);
    }
  }, [specification, title]);

  if (!specification) {
    return (
      <div className="spec-viewer spec-viewer--empty" role="status">
        <p>No specification data available</p>
      </div>
    );
  }

  return (
    <div className="spec-viewer" role="main" aria-label={`${title} specification`}>
      <header className="spec-viewer__header">
        <h1 className="spec-viewer__title">{title}</h1>
        <div className="spec-viewer__actions">
          <ExportButton 
            onExport={handleExport}
            disabled={isExporting}
            loading={isExporting}
          />
        </div>
      </header>

      <div className="spec-viewer__content">
        {specification.sections?.map((section, index) => (
          <CollapsibleSection
            key={section.id || index}
            id={section.id || `section-${index}`}
            title={section.title}
            isExpanded={expandedSections.has(section.id || `section-${index}`)}
            onToggle={toggleSection}
          >
            <SpecificationContent content={section.content} type={section.type} />
          </CollapsibleSection>
        ))}
      </div>
    </div>
  );
};

export default SpecificationViewer;