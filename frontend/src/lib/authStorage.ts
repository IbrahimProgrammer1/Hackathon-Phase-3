// Authentication storage implementation
// Handles JWT storage and retrieval with security best practices

export class AuthStorage {
  private static readonly TOKEN_KEY = 'auth_token';
  private static readonly USER_KEY = 'current_user';
  private static readonly TOKEN_EXPIRY_KEY = 'auth_token_expiry';

  // Store the JWT token
  static storeToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.TOKEN_KEY, token);

      // Calculate and store the token expiry time
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.exp) {
          const expiryTime = payload.exp * 1000; // Convert to milliseconds
          localStorage.setItem(this.TOKEN_EXPIRY_KEY, expiryTime.toString());
        }
      } catch (e) {
        console.error('Error parsing token:', e);
      }
    }
  }

  // Get the stored JWT token
  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      // Check if token is expired before returning
      if (this.isTokenExpired()) {
        this.clearAuthData();
        return null;
      }

      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  // Store user data
  static storeUser(userData: any): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.USER_KEY, JSON.stringify(userData));
    }
  }

  // Get stored user data
  static getUser(): any | null {
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

  // Check if the token is expired
  static isTokenExpired(): boolean {
    if (typeof window !== 'undefined') {
      const expiryStr = localStorage.getItem(this.TOKEN_EXPIRY_KEY);
      if (expiryStr) {
        const expiryTime = parseInt(expiryStr, 10);
        const now = Date.now();
        return now >= expiryTime;
      }
    }
    return true; // If we can't find expiry time, assume expired
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    const token = this.getToken();
    return token !== null && token !== '';
  }

  // Clear all authentication data
  static clearAuthData(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.TOKEN_KEY);
      localStorage.removeItem(this.USER_KEY);
      localStorage.removeItem(this.TOKEN_EXPIRY_KEY);
    }
  }

  // Get the time remaining before token expires (in milliseconds)
  static getTokenTimeRemaining(): number | null {
    if (typeof window !== 'undefined') {
      const expiryStr = localStorage.getItem(this.TOKEN_EXPIRY_KEY);
      if (expiryStr) {
        const expiryTime = parseInt(expiryStr, 10);
        const now = Date.now();
        return expiryTime - now;
      }
    }
    return null;
  }
}