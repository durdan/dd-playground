import React from 'react';
import { useUser } from '../contexts/UserContext';
import './UserInfo.css';

const UserInfo = () => {
  const { user, logout, isLoading, error } = useUser();

  if (isLoading) {
    return <div data-testid="loading">Loading user information...</div>;
  }

  if (error) {
    return <div data-testid="error" className="error">Error: {error}</div>;
  }

  if (!user) {
    return <div data-testid="no-user">No user logged in</div>;
  }

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  return (
    <div data-testid="user-info" className="user-info">
      <div className="user-avatar">
        {user.avatar ? (
          <img 
            src={user.avatar} 
            alt={`${user.name}'s avatar`}
            data-testid="user-avatar"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        ) : (
          <div data-testid="default-avatar" className="default-avatar">
            {user.name?.charAt(0)?.toUpperCase() || '?'}
          </div>
        )}
      </div>
      
      <div className="user-details">
        <h2 data-testid="user-name">{user.name || 'Unknown User'}</h2>
        <p data-testid="user-email">{user.email || 'No email provided'}</p>
        {user.role && (
          <span data-testid="user-role" className="user-role">
            {user.role}
          </span>
        )}
      </div>
      
      <button 
        data-testid="logout-button"
        onClick={handleLogout}
        className="logout-button"
        type="button"
      >
        Logout
      </button>
    </div>
  );
};

export default UserInfo;