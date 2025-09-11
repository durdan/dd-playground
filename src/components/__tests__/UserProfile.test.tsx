import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserProfile from '../UserProfile';
import { useUser } from '../../hooks/useUser';

// Mock the useUser hook
jest.mock('../../hooks/useUser');
const mockUseUser = useUser as jest.MockedFunction<typeof useUser>;

// Mock window.confirm
const mockConfirm = jest.fn();
Object.defineProperty(window, 'confirm', {
  value: mockConfirm,
  writable: true,
});

describe('UserProfile', () => {
  const mockUser = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin',
    avatar: 'https://example.com/avatar.jpg'
  };

  const mockLogout = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('displays loading state', () => {
    mockUseUser.mockReturnValue({
      user: null,
      logout: mockLogout,
      isLoading: true,
    });

    render(<UserProfile />);
    
    expect(screen.getByRole('status')).toBeInTheDocument();
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('displays error when user is null and not loading', () => {
    mockUseUser.mockReturnValue({
      user: null,
      logout: mockLogout,
      isLoading: false,
    });

    render(<UserProfile />);
    
    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('Unable to load user information')).toBeInTheDocument();
  });

  it('displays user information correctly', () => {
    mockUseUser.mockReturnValue({
      user: mockUser,
      logout: mockLogout,
      isLoading: false,
    });

    render(<UserProfile />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('admin')).toBeInTheDocument();
    expect(screen.getByAltText("John Doe's avatar")).toBeInTheDocument();
  });

  it('sanitizes user input to prevent XSS', () => {
    const maliciousUser = {
      ...mockUser,
      name: 'John<script>alert("xss")</script>Doe',
      email: 'john<>@example.com',
    };

    mockUseUser.mockReturnValue({
      user: maliciousUser,
      logout: mockLogout,
      isLoading: false,
    });

    render(<UserProfile />);
    
    expect(screen.getByText('Johnscriptalert("xss")/scriptDoe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls logout when button is clicked and confirmed', async () => {
    mockConfirm.mockReturnValue(true);
    mockUseUser.mockReturnValue({
      user: mockUser,
      logout: mockLogout,
      isLoading: false,
    });

    render(<UserProfile />);
    
    const logoutButton = screen.getByTestId('logout-button');
    fireEvent.click(logoutButton);

    expect(mockConfirm).toHaveBeenCalledWith('Are you sure you want to logout?');
    await waitFor(() => {
      expect(mockLogout).toHaveBeenCalled();
    });
  });

  it('does not call logout when not confirmed', () => {
    mockConfirm.mockReturnValue(false);
    mockUseUser.mockReturnValue({
      user: mockUser,
      logout: mockLogout,
      isLoading: false,
    });

    render(<UserProfile />);
    
    const logoutButton = screen.getByTestId('logout-button');
    fireEvent.click(logoutButton);

    expect(mockConfirm).toHaveBeenCalled();
    expect(mockLogout).not.toHaveBeenCalled();
  });

  it('handles avatar load error gracefully', () => {
    mockUseUser.mockReturnValue({
      user: mockUser,
      logout: mockLogout,
      isLoading: false,
    });

    render(<UserProfile />);
    
    const avatar = screen.getByAltText("John Doe's avatar");
    fireEvent.error(avatar);

    expect(avatar.style.display).toBe('none');
  });
});