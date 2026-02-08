// Frontend tests for error handling scenarios
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ErrorDisplay from '@/components/ErrorDisplay';

// Mock the router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    refresh: vi.fn(),
  }),
}));

describe('Error Handling Tests', () => {
  it('renders error message correctly', () => {
    render(<ErrorDisplay error="Something went wrong" />);

    expect(screen.getByText(/error/i)).toBeInTheDocument();
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
  });

  it('shows retry button when onRetry is provided', () => {
    const mockRetry = vi.fn();
    render(<ErrorDisplay error="Something went wrong" onRetry={mockRetry} />);

    const retryButton = screen.getByText(/retry/i);
    expect(retryButton).toBeInTheDocument();

    fireEvent.click(retryButton);
    expect(mockRetry).toHaveBeenCalledTimes(1);
  });

  it('does not show retry button when onRetry is not provided', () => {
    render(<ErrorDisplay error="Something went wrong" />);

    expect(screen.queryByText(/retry/i)).not.toBeInTheDocument();
  });

  it('handles 404 errors appropriately in task components', async () => {
    // This would be tested in integration with actual task components
    // Mocking how a task component would handle a 404 response
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    // Simulate a task component receiving a 404 error
    render(<ErrorDisplay error="Task not found or does not belong to you" />);

    expect(screen.getByText(/task not found or does not belong to you/i)).toBeInTheDocument();

    consoleSpy.mockRestore();
  });

  it('handles unauthorized errors appropriately', async () => {
    render(<ErrorDisplay error="Authentication required. Please log in again." />);

    expect(screen.getByText(/authentication required\. please log in again\./i)).toBeInTheDocument();
  });
});