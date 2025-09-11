import { useApi } from './useApi';
import { userService } from '../services/userService';
import { User } from '../types/api';

export function useUsers() {
  return useApi(() => userService.getUsers());
}

export function useUser(id: number) {
  return useApi(() => userService.getUser(id));
}

export function useCreateUser() {
  return useApi(
    (userData: Omit<User, 'id' | 'createdAt'>) => userService.createUser(userData),
    { immediate: false }
  );
}

export function useUpdateUser() {
  return useApi(
    ({ id, userData }: { id: number; userData: Partial<User> }) => 
      userService.updateUser(id, userData),
    { immediate: false }
  );
}

export function useDeleteUser() {
  return useApi(
    (id: number) => userService.deleteUser(id),
    { immediate: false }
  );
}