// API client for frontend to communicate with backend
// Includes JWT token attachment for authenticated requests

interface ApiConfig {
  baseUrl: string;
  headers?: Record<string, string>;
}

class ApiClient {
  private config: ApiConfig;

  constructor(config: ApiConfig) {
    this.config = {
      baseUrl: config.baseUrl,
      headers: {
        'Content-Type': 'application/json',
        ...config.headers,
      },
    };
  }

  // Get JWT token from wherever it's stored (localStorage, cookie, etc.)
  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      // Get token from localStorage or wherever you store it
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  // Add auth token to headers
  private getAuthHeaders(): Record<string, string> {
    const token = this.getAuthToken();
    const headers: Record<string, string> = { ...this.config.headers };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Generic request method
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;
    const headers = this.getAuthHeaders();

    const response = await fetch(url, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    });

    // Handle 401 Unauthorized responses by logging out the user
    if (response.status === 401) {
      // Import AuthService dynamically to avoid circular dependencies
      import('./auth').then(({ AuthService }) => {
        AuthService.logout();
      });

      // Redirect to login page (in browser environment)
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/login';
      }

      throw new Error('Unauthorized - Please log in again');
    }

    if (!response.ok) {
      // Try to get error details from response
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        // If response is not JSON, use status text
        errorData = { error: response.statusText, code: response.status };
      }

      // Properly extract error message, handling both string and object types
      let errorMessage: string;
      if (typeof errorData === 'string') {
        errorMessage = errorData;
      } else if (errorData.error) {
        errorMessage = String(errorData.error);
      } else if (errorData.detail) {
        errorMessage = String(errorData.detail);
      } else {
        errorMessage = `HTTP error! status: ${response.status}`;
      }
      
      throw new Error(errorMessage);
    }

    // For DELETE requests, there might not be a response body
    if (response.status === 204) {
      return {} as T; // Return empty object for 204 responses
    }

    return response.json();
  }

  // GET request
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'GET',
    });
  }

  // POST request
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // PUT request
  async put<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // PATCH request
  async patch<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // DELETE request
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE',
    });
  }
}

// Create API client instance
export const apiClient = new ApiClient({
  baseUrl: `${(process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')}/api`,
});

// Specific API methods for task operations
export const taskApi = {
  // Get all tasks for a user
  getTasks: (userId: string) => {
    return apiClient.get<Task[]>(`/${userId}/tasks`);
  },

  // Create a new task
  createTask: (userId: string, taskData: { title: string; description?: string }) => {
    return apiClient.post<Task>(`/${userId}/tasks`, taskData);
  },

  // Get a specific task
  getTask: (userId: string, taskId: number) => {
    return apiClient.get<Task>(`/${userId}/tasks/${taskId}`);
  },

  // Update a task
  updateTask: (userId: string, taskId: number, taskData: { title?: string; description?: string }) => {
    return apiClient.put<Task>(`/${userId}/tasks/${taskId}`, taskData);
  },

  // Toggle task completion
  toggleTaskCompletion: (userId: string, taskId: number, completed: boolean) => {
    return apiClient.patch<Task>(`/${userId}/tasks/${taskId}/complete`, { completed });
  },

  // Delete a task
  deleteTask: (userId: string, taskId: number) => {
    return apiClient.delete<{}>(`/${userId}/tasks/${taskId}`);
  },
};

// Type definitions
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}