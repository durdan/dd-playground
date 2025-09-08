import React, { useState, useContext, createContext } from 'react';
import axios from 'axios';

// Authentication context
const AuthContext = createContext(null);

// Use this hook to access auth functions and state
export const useAuth = () => useContext(AuthContext);

// Provider component that wraps your app and makes auth object available to any child component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/auth/login', { email, password });
      setUser(response.data.user);
      localStorage.setItem('token', response.data.token);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Higher order component for protected routes
export const withProtected = (Component) => (props) => {
  const { user } = useAuth();
  return user ? <Component {...props} /> : <p>You must be logged in to view this page.</p>;
};
