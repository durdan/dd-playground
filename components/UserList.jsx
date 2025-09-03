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
      await executeAsync(async () => {
        const data = await apiService.get('/users');
        setUsers(data);
        return data;
      });
    } catch (err) {
      console.error('Failed to load users:', err);
    }
  };

  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      await deleteLoading.executeAsync(async () => {
        await apiService.delete(`/users/${userId}`);
        setUsers(prev => prev.filter(user => user.id !== userId));
      });
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
        <p>Error: {error}</p>
        <button onClick={loadUsers}>Retry</button>
      </div>
    );
  }

  return (
    <div className="user-list">
      <div className="user-list-header">
        <h2>Users</h2>
        <button onClick={loadUsers} disabled={isLoading}>
          Refresh
        </button>
      </div>

      {users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        <div className="user-grid">
          {users.map(user => (
            <div key={user.id} className="user-card">
              <h3>{user.name}</h3>
              <p>{user.email}</p>
              {user.phone && <p>{user.phone}</p>}
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
            </div>
          ))}
        </div>
      )}

      {deleteLoading.error && (
        <div className="error-message">
          Delete failed: {deleteLoading.error}
        </div>
      )}
    </div>
  );
};

export default UserList;