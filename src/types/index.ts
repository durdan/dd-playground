export interface ApiResponse<T = any> {
  data?: T;
  error?: {
    message: string;
    status: number;
    stack?: string;
  };
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  uptime: number;
}