export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  uptime: number;
}