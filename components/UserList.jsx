import React, { useState, useEffect } from 'react';
import { useLoading } from '../hooks/useLoading';
import { apiService } from '../services/apiService';
import LoadingSpinner from './LoadingSpinner';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const { isLoading, error, executeAsync } = useLoading();
  const deleteLoading = useLoading();

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const userData = await executeAsync(() => apiService.get('/users'));
      setUsers(userData);
    } catch (err) {
      console.error('Failed to load users:', err);
    }
  };

  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      await deleteLoading.executeAsync(() => 
        apiService.delete(`/users/${userId}`)
      );
      setUsers(prev => prev.filter(user => user.id !== userId));
    } catch (err) {
      console.error('Failed to delete user:', err);
    }
  };

  if (isLoading) {
    return <LoadingSpinner size="large" message="Loading users..." />;
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
        <button onClick={loadUsers}>Retry</button>
      </div>
    );
  }

  return (
    <div className="user-list">
      <h2>Users</h2>
      {users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        <ul>
          {users.map(user => (
            <li key={user.id} className="user-item">
              <div className="user-info">
                <strong>{user.name}</strong>
                <span>{user.email}</span>
              </div>
              <button
                onClick={() => handleDelete(user.id)}
                disabled={deleteLoading.isLoading}
                className="delete-button"
              >
                {deleteLoading.isLoading ? (
                  <LoadingSpinner size="small" />
                ) : (
                  'Delete'
                )}
              </button>
            </li>
          ))}
        </ul>
      )}
      {deleteLoading.error && (
        <div className="error-message">{deleteLoading.error}</div>
      )}
    </div>
  );
};

export default UserList;