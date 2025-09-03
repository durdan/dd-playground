import React from 'react';
import { render, screen } from '@testing-library/react';
import LoadingSpinner from '../components/LoadingSpinner';

describe('LoadingSpinner', () => {
  test('renders spinner with default props', () => {
    render(<LoadingSpinner />);
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    expect(document.querySelector('.spinner-medium')).toBeInTheDocument();
  });

  test('renders spinner with custom message', () => {
    render(<LoadingSpinner message="Please wait..." />);
    
    expect(screen.getByText('Please wait...')).toBeInTheDocument();
  });

  test('renders spinner with different sizes', () => {
    const { rerender } = render(<LoadingSpinner size="small" />);
    expect(document.querySelector('.spinner-small')).toBeInTheDocument();
    
    rerender(<LoadingSpinner size="large" />);
    expect(document.querySelector('.spinner-large')).toBeInTheDocument();
  });

  test('renders overlay when overlay prop is true', () => {
    render(<LoadingSpinner overlay />);
    
    expect(document.querySelector('.loading-overlay')).toBeInTheDocument();
  });

  test('renders without message when message is empty', () => {
    render(<LoadingSpinner message="" />);
    
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
  });
});