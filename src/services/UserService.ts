import { User } from '../types/User';

class UserService {
  private static instance: UserService;
  private baseUrl = process.env.REACT_APP_API_URL || '/api';

  static getInstance(): UserService {
    if (!UserService.instance) {
      UserService.instance = new UserService();
    }
    return UserService.instance;
  }

  async getCurrentUser(): Promise<User | null> {
    try {
      const token = this.getAuthToken();
      if (!token) return null;

      const response = await fetch(`${this.baseUrl}/user/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          this.clearAuthToken();
          return null;
        }
        throw new Error(`Failed to fetch user: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching current user:', error);
      return null;
    }
  }

  async logout(): Promise<void> {
    try {
      const token = this.getAuthToken();
      if (token) {
        await fetch(`${this.baseUrl}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
      }
    } catch (error) {
      console.error('Logout request failed:', error);
    } finally {
      this.clearAuthToken();
      window.location.href = '/login';
    }
  }

  private getAuthToken(): string | null {
    return localStorage.getItem('authToken');
  }

  private clearAuthToken(): void {
    localStorage.removeItem('authToken');
  }
}

export default UserService;