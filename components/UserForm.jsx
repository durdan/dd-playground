import React, { useState } from 'react';
import { useLoading } from '../hooks/useLoading';
import { apiService } from '../services/apiService';
import LoadingSpinner from './LoadingSpinner';

const UserForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: ''
  });
  
  const { isLoading, error, executeAsync } = useLoading();

  const validateForm = () => {
    if (!formData.name.trim()) throw new Error('Name is required');
    if (!formData.email.trim()) throw new Error('Email is required');
    if (!/\S+@\S+\.\S+/.test(formData.email)) throw new Error('Invalid email format');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      validateForm();
      
      const result = await executeAsync(() => 
        apiService.post('/users', formData)
      );
      
      setFormData({ name: '', email: '', phone: '' });
      onSuccess?.(result);
    } catch (err) {
      console.error('Form submission failed:', err);
    }
  };

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="user-form">
      <div className="form-group">
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
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
          onChange={handleChange}
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
          onChange={handleChange}
          disabled={isLoading}
        />
      </div>

      {error && <div className="error-message">{error}</div>}

      <button type="submit" disabled={isLoading} className="submit-button">
        {isLoading ? (
          <>
            <LoadingSpinner size="small" />
            <span>Submitting...</span>
          </>
        ) : (
          'Submit'
        )}
      </button>
    </form>
  );
};

export default UserForm;