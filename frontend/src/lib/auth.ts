// Authentication service for frontend
// Handles authentication state, token storage, and user management

// Authentication service functions
export class AuthService {
  private static readonly TOKEN_KEY = 'auth_token';
  private static readonly USER_KEY = 'current_user';

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem(this.TOKEN_KEY);
      return token !== null && token !== '';
    }
    return false;
  }

  // Get current user info
  static getCurrentUser(): any | null {
    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem(this.USER_KEY);
      if (userStr) {
        try {
          return JSON.parse(userStr);
        } catch (e) {
          console.error('Error parsing user data:', e);
          return null;
        }
      }
    }
    return null;
  }

  // Store user token after login
  static storeToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.TOKEN_KEY, token);
      // Keep a cookie in sync so Next.js middleware can see auth state.
      // (Not HTTP-only; use HTTP-only cookies in production with a server-side auth route.)
      document.cookie = `auth_token=${encodeURIComponent(token)}; Path=/; SameSite=Lax`;
    }
  }

  // Store user data after login
  static storeUser(userData: any): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.USER_KEY, JSON.stringify(userData));
    }
  }

  // Get stored token
  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  // Clear authentication data on logout
  static logout(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.TOKEN_KEY);
      localStorage.removeItem(this.USER_KEY);
      document.cookie = 'auth_token=; Path=/; Max-Age=0; SameSite=Lax';
    }
  }

  // Check if token is expired
  static isTokenExpired(): boolean {
    const token = this.getToken();
    if (!token) return true;

    try {
      // Decode JWT payload (second part after the dot)
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const payload = JSON.parse(window.atob(base64));

      // Check if token is expired
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < currentTime;
    } catch (e) {
      console.error('Error checking token expiration:', e);
      return true;
    }
  }

  // Refresh token if needed (simplified implementation)
  static async refreshToken(): Promise<string | null> {
    const token = this.getToken();
    if (!token) return null;

    // Check if token is expired or expiring soon (within 5 minutes)
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const payload = JSON.parse(window.atob(base64));

      const exp = payload.exp;
      const currentTime = Math.floor(Date.now() / 1000);

      // If token expires in less than 5 minutes, attempt refresh
      if (exp && exp - currentTime < 300) {
        // In a real implementation, you would call your backend to refresh the token
        // For now, we'll return the current token
        return token;
      }
    } catch (e) {
      console.error('Error checking token expiration:', e);
    }

    return token;
  }
}

// Type definitions
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
}