export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  role: string;
}

export interface UserContextType {
  user: User | null;
  logout: () => Promise<void>;
  isLoading: boolean;
}