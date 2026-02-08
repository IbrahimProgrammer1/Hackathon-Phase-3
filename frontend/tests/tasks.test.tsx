// Frontend integration tests for task actions
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import TasksPage from '@/app/tasks/page';

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
    getCurrentUser: vi.fn(() => ({ id: 'user123' })),
    isAuthenticated: vi.fn(() => true),
  },
}));

// Mock the taskApi
vi.mock('@/lib/api', () => ({
  taskApi: {
    getTasks: vi.fn(() => Promise.resolve([
      { id: 1, user_id: 'user123', title: 'Test Task', description: 'Test Description', completed: false, created_at: '2026-01-06T10:00:00Z', updated_at: '2026-01-06T10:00:00Z' }
    ])),
    createTask: vi.fn(() => Promise.resolve({ id: 2, user_id: 'user123', title: 'New Task', description: 'New Description', completed: false, created_at: '2026-01-06T10:00:00Z', updated_at: '2026-01-06T10:00:00Z' })),
    updateTask: vi.fn(() => Promise.resolve({ id: 1, user_id: 'user123', title: 'Updated Task', description: 'Updated Description', completed: false, created_at: '2026-01-06T10:00:00Z', updated_at: '2026-01-06T10:00:00Z' })),
    deleteTask: vi.fn(() => Promise.resolve({})),
    toggleTaskCompletion: vi.fn(() => Promise.resolve({ id: 1, user_id: 'user123', title: 'Test Task', description: 'Test Description', completed: true, created_at: '2026-01-06T10:00:00Z', updated_at: '2026-01-06T10:00:00Z' })),
  },
}));

describe('Task Operations Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders task list page with tasks', async () => {
    render(<TasksPage />);

    await waitFor(() => {
      expect(screen.getByText(/my tasks/i)).toBeInTheDocument();
    });

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('shows loading state initially', () => {
    render(<TasksPage />);

    expect(screen.getByText(/loading tasks\.\.\./i)).toBeInTheDocument();
  });

  it('allows creating new tasks', async () => {
    render(<TasksPage />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Mock the form submission
    const titleInput = screen.getByLabelText(/title \*/i);
    fireEvent.change(titleInput, { target: { value: 'New Task' } });

    const descriptionInput = screen.getByLabelText(/description/i);
    fireEvent.change(descriptionInput, { target: { value: 'New Description' } });

    fireEvent.click(screen.getByRole('button', { name: /create task/i }));

    await waitFor(() => {
      expect(screen.getByText('New Task')).toBeInTheDocument();
    });
  });

  it('allows updating tasks', async () => {
    render(<TasksPage />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/edit/i));

    const titleInput = screen.getByDisplayValue('Test Task');
    fireEvent.change(titleInput, { target: { value: 'Updated Task' } });

    fireEvent.click(screen.getByText(/save/i));

    await waitFor(() => {
      expect(screen.getByText('Updated Task')).toBeInTheDocument();
    });
  });

  it('allows deleting tasks', async () => {
    render(<TasksPage />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    // Mock window.confirm to return true
    window.confirm = vi.fn(() => true);

    fireEvent.click(screen.getByText(/delete/i));

    await waitFor(() => {
      expect(screen.queryByText('Test Task')).not.toBeInTheDocument();
    });
  });

  it('allows toggling task completion', async () => {
    render(<TasksPage />);

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/mark complete/i));

    await waitFor(() => {
      expect(screen.getByText(/✓ completed/i)).toBeInTheDocument();
    });
  });
});