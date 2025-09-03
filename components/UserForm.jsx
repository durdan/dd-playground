import React, { useState } from 'react';
import useLoading from '../hooks/useLoading';
import apiService from '../services/apiService';

const UserForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: ''
  });
  
  const { isLoading, error, executeAsync } = useLoading();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      throw new Error('Name is required');
    }
    if (!formData.email.trim()) {
      throw new Error('Email is required');
    }
    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      throw new Error('Email is invalid');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      validateForm();
      
      await executeAsync(async () => {
        const result = await apiService.post('/users', formData);
        setFormData({ name: '', email: '', phone: '' });
        onSuccess?.(result);
        return result;
      });
    } catch (err) {
      // Error is handled by useLoading hook
      console.error('Form submission failed:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="user-form">
      <h2>Create User</h2>
      
      {error && (
        <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
          {error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleInputChange}
          disabled={isLoading}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          disabled={isLoading}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="phone">Phone:</label>
        <input
          type="tel"
          id="phone"
          name="phone"
          value={formData.phone}
          onChange={handleInputChange}
          disabled={isLoading}
        />
      </div>

      <button 
        type="submit" 
        disabled={isLoading}
        className={isLoading ? 'btn-loading' : ''}
      >
        {isLoading && <span className="btn-spinner"></span>}
        {isLoading ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
};

export default UserForm;