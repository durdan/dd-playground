import React, { useState, useEffect } from 'react';
import LoadingSpinner from './LoadingSpinner';
import useLoading from '../hooks/useLoading';
import apiService from '../services/apiService';

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
    return <LoadingSpinner message="Loading users..." />;
  }

  if (error) {
    return (
      <div className="error-container">
        <p style={{ color: 'red' }}>Error: {error}</p>
        <button onClick={loadUsers}>Retry</button>
      </div>
    );
  }

  return (
    <div className="user-list">
      <h2>Users</h2>
      
      {deleteLoading.error && (
        <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
          {deleteLoading.error}
        </div>
      )}

      {users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        <div className="users-grid">
          {users.map(user => (
            <div key={user.id} className="user-card">
              <h3>{user.name}</h3>
              <p>Email: {user.email}</p>
              {user.phone && <p>Phone: {user.phone}</p>}
              
              <button
                onClick={() => handleDelete(user.id)}
                disabled={deleteLoading.isLoading}
                className={deleteLoading.isLoading ? 'btn-loading' : ''}
                style={{ 
                  backgroundColor: '#dc3545', 
                  color: 'white',
                  border: 'none',
                  padding: '5px 10px',
                  cursor: 'pointer'
                }}
              >
                {deleteLoading.isLoading && <span className="btn-spinner"></span>}
                {deleteLoading.isLoading ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          ))}
        </div>
      )}
      
      <button onClick={loadUsers} disabled={isLoading}>
        Refresh
      </button>
    </div>
  );
};

export default UserList;