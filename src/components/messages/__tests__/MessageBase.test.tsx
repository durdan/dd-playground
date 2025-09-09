import React from 'react';
import { render, screen } from '@testing-library/react';
import { MessageBase } from '../MessageBase';

describe('MessageBase', () => {
  it('renders children correctly', () => {
    render(
      <MessageBase>
        <div>Test content</div>
      </MessageBase>
    );
    
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });

  it('applies correct variant classes', () => {
    const { container } = render(
      <MessageBase variant="user">
        <div>User message</div>
      </MessageBase>
    );
    
    expect(container.firstChild).toHaveClass('bg-blue-50', 'border-blue-500');
  });

  it('displays timestamp when provided', () => {
    const timestamp = new Date('2023-01-01T12:00:00Z');
    render(
      <MessageBase timestamp={timestamp}>
        <div>Content</div>
      </MessageBase>
    );
    
    expect(screen.getByRole('time')).toBeInTheDocument();
  });

  it('has proper accessibility attributes', () => {
    render(
      <MessageBase variant="system">
        <div>System message</div>
      </MessageBase>
    );
    
    expect(screen.getByRole('article')).toHaveAttribute('aria-label', 'system message');
  });
});