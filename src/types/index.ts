export interface HealthResponse {
  status: string;
  timestamp: string;
  uptime: number;
}

export interface ErrorResponse {
  error: {
    message: string;
    stack?: string;
  };
}