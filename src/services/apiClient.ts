import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { ApiResponse, ApiError } from '../types/api';
import { cacheManager } from './cacheManager';

class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.REACT_APP_API_URL || 'http://localhost:3001/api') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error: AxiosError) => {
        const apiError: ApiError = {
          message: error.response?.data?.message || error.message || 'An error occurred',
          status: error.response?.status || 500,
          code: error.code
        };
        return Promise.reject(apiError);
      }
    );
  }

  async get<T>(url: string, useCache: boolean = true, cacheTTL?: number): Promise<T> {
    const cacheKey = `GET:${url}`;
    
    if (useCache) {
      const cached = cacheManager.get<T>(cacheKey);
      if (cached) return cached;
    }

    const response = await this.client.get<ApiResponse<T>>(url);
    const data = response.data.data;
    
    if (useCache) {
      cacheManager.set(cacheKey, data, cacheTTL);
    }
    
    return data;
  }

  async post<T>(url: string, data: any, invalidateCache?: string[]): Promise<T> {
    const response = await this.client.post<ApiResponse<T>>(url, data);
    
    if (invalidateCache) {
      invalidateCache.forEach(pattern => cacheManager.invalidatePattern(pattern));
    }
    
    return response.data.data;
  }

  async put<T>(url: string, data: any, invalidateCache?: string[]): Promise<T> {
    const response = await this.client.put<ApiResponse<T>>(url, data);
    
    if (invalidateCache) {
      invalidateCache.forEach(pattern => cacheManager.invalidatePattern(pattern));
    }
    
    return response.data.data;
  }

  async delete<T>(url: string, invalidateCache?: string[]): Promise<T> {
    const response = await this.client.delete<ApiResponse<T>>(url);
    
    if (invalidateCache) {
      invalidateCache.forEach(pattern => cacheManager.invalidatePattern(pattern));
    }
    
    return response.data.data;
  }
}

export const apiClient = new ApiClient();