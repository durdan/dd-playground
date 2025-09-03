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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email) {
      return;
    }

    try {
      await executeAsync(async () => {
        const result = await apiService.post('/users', formData);
        setFormData({ name: '', email: '', phone: '' });
        onSuccess?.(result);
        return result;
      });
    } catch (err) {
      console.error('Form submission failed:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="user-form">
      <div className="form-group">
        <label htmlFor="name">Name *</label>
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
        <label htmlFor="email">Email *</label>
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
        <label htmlFor="phone">Phone</label>
        <input
          type="tel"
          id="phone"
          name="phone"
          value={formData.phone}
          onChange={handleInputChange}
          disabled={isLoading}
        />
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <button 
        type="submit" 
        disabled={isLoading}
        className="submit-button"
      >
        {isLoading ? (
          <>
            <LoadingSpinner size="small" />
            Submitting...
          </>
        ) : (
          'Submit'
        )}
      </button>
    </form>
  );
};

export default UserForm;