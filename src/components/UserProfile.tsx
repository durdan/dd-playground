import React from 'react';
import { useUser } from '../hooks/useUser';
import './UserProfile.css';

const UserProfile: React.FC = () => {
  const { user, logout, isLoading } = useUser();

  const handleLogout = async () => {
    if (window.confirm('Are you sure you want to logout?')) {
      await logout();
    }
  };

  const sanitizeText = (text: string): string => {
    return text.replace(/[<>]/g, '');
  };

  if (isLoading) {
    return (
      <div className="user-profile loading" role="status" aria-label="Loading user information">
        <div className="spinner" />
        <span>Loading...</span>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="user-profile error" role="alert">
        <p>Unable to load user information</p>
      </div>
    );
  }

  return (
    <div className="user-profile" data-testid="user-profile">
      <div className="user-info">
        {user.avatar && (
          <img 
            src={user.avatar} 
            alt={`${user.name}'s avatar`}
            className="user-avatar"
            onError={(e) => {
              e.currentTarget.style.display = 'none';
            }}
          />
        )}
        <div className="user-details">
          <h2 className="user-name">{sanitizeText(user.name)}</h2>
          <p className="user-email">{sanitizeText(user.email)}</p>
          <span className="user-role">{sanitizeText(user.role)}</span>
        </div>
      </div>
      <button 
        className="logout-button"
        onClick={handleLogout}
        disabled={isLoading}
        aria-label="Logout from account"
        data-testid="logout-button"
      >
        {isLoading ? 'Logging out...' : 'Logout'}
      </button>
    </div>
  );
};

export default UserProfile;