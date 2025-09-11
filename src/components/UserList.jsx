import React, { useState, useEffect } from 'react';
import ApiService from '../services/apiService';

const UserList = ({ onEditUser, onDeleteUser }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiService = new ApiService();

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const userData = await apiService.getUsers();
      setUsers(userData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      await apiService.deleteUser(userId);
      setUsers(users.filter(user => user.id !== userId));
      onDeleteUser && onDeleteUser(userId);
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div data-testid="loading">Loading...</div>;
  if (error) return <div data-testid="error">Error: {error}</div>;

  return (
    <div data-testid="user-list">
      <h2>Users</h2>
      {users.length === 0 ? (
        <p data-testid="no-users">No users found</p>
      ) : (
        <ul>
          {users.map(user => (
            <li key={user.id} data-testid={`user-${user.id}`}>
              <div>
                <strong>{user.name}</strong> - {user.email}
              </div>
              <div>
                <button 
                  onClick={() => onEditUser && onEditUser(user)}
                  data-testid={`edit-${user.id}`}
                >
                  Edit
                </button>
                <button 
                  onClick={() => handleDelete(user.id)}
                  data-testid={`delete-${user.id}`}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default UserList;