// Frontend integration tests for auth flow
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LoginPage from '@/app/auth/login/page';

// Mock the router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    refresh: vi.fn(),
  }),
}));

// Mock the AuthService
vi.mock('@/lib/auth', () => ({
  AuthService: {
    storeToken: vi.fn(),
    storeUser: vi.fn(),
    isAuthenticated: vi.fn(() => false),
  },
}));

describe('Auth Flow Tests', () => {
  it('renders login page with email and password fields', () => {
    render(<LoginPage />);

    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  it('shows error when login fails', async () => {
    render(<LoginPage />);

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrongpassword' },
    });

    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/login failed/i)).toBeInTheDocument();
    });
  });

  it('allows navigation to register page', () => {
    render(<LoginPage />);

    const registerLink = screen.getByText(/don't have an account\? register/i);
    expect(registerLink).toBeInTheDocument();
    expect(registerLink.closest('a')).toHaveAttribute('href', '/auth/register');
  });
});