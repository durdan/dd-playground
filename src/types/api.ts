export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface User {
  id: number;
  name: string;
  email: string;
  createdAt: string;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  userId: number;
  createdAt: string;
}

export interface ApiError {
  message: string;
  status: number;
  code?: string;
}

export interface LoadingState {
  isLoading: boolean;
  error: ApiError | null;
}