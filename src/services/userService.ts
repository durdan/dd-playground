import { apiClient } from './apiClient';
import { User } from '../types/api';

export const userService = {
  async getUsers(): Promise<User[]> {
    return apiClient.get<User[]>('/users');
  },

  async getUser(id: number): Promise<User> {
    return apiClient.get<User>(`/users/${id}`);
  },

  async createUser(userData: Omit<User, 'id' | 'createdAt'>): Promise<User> {
    return apiClient.post<User>('/users', userData, ['GET:/users']);
  },

  async updateUser(id: number, userData: Partial<User>): Promise<User> {
    return apiClient.put<User>(`/users/${id}`, userData, [`GET:/users/${id}`, 'GET:/users']);
  },

  async deleteUser(id: number): Promise<void> {
    return apiClient.delete<void>(`/users/${id}`, [`GET:/users/${id}`, 'GET:/users']);
  }
};