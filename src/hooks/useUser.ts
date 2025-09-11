import { useState, useEffect, useCallback } from 'react';
import { User } from '../types/User';
import UserService from '../services/UserService';

export const useUser = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const userService = UserService.getInstance();

  useEffect(() => {
    const loadUser = async () => {
      setIsLoading(true);
      try {
        const currentUser = await userService.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Failed to load user:', error);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, [userService]);

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await userService.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setIsLoading(false);
    }
  }, [userService]);

  return { user, logout, isLoading };
};