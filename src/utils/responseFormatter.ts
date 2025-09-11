export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export const successResponse = <T>(data: T, message?: string): ApiResponse<T> => ({
  success: true,
  data,
  message
});

export const errorResponse = (error: string): ApiResponse => ({
  success: false,
  error
});

export const validationErrorResponse = (errors: string[]): ApiResponse => ({
  success: false,
  error: 'Validation failed',
  data: { errors }
});