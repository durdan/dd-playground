import React from 'react';
import CodeBlock from './CodeBlock';

const SpecificationContent = ({ content, type = 'text' }) => {
  if (!content) {
    return <p className="spec-content--empty">No content available</p>;
  }

  switch (type) {
    case 'code':
      return (
        <CodeBlock
          code={content.code || content}
          language={content.language || 'javascript'}
          title={content.title}
        />
      );
    
    case 'list':
      return (
        <ul className="spec-content__list">
          {(Array.isArray(content) ? content : [content]).map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      );
    
    case 'table':
      if (!content.headers || !content.rows) {
        return <p>Invalid table data</p>;
      }
      return (
        <div className="spec-content__table-wrapper">
          <table className="spec-content__table">
            <thead>
              <tr>
                {content.headers.map((header, index) => (
                  <th key={index}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {content.rows.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    
    case 'text':
    default:
      return (
        <div className="spec-content__text">
          {typeof content === 'string' ? (
            <p>{content}</p>
          ) : (
            <div dangerouslySetInnerHTML={{ __html: content.html || content }} />
          )}
        </div>
      );
  }
};

export default SpecificationContent;