'use client';

import { useEffect, useState } from 'react';
import { taskApi, Task } from '@/lib/api';
import { AuthService } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import TaskForm from '@/components/TaskForm';
import FloatingButton from '@/components/FloatingButton';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumEmptyState from '@/components/PremiumEmptyState';
import PremiumTaskCard from '@/components/PremiumTaskCard';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const router = useRouter();

  // Get user ID from auth service
  const userId = AuthService.getCurrentUser()?.id;

  useEffect(() => {
    if (!userId) {
      // Redirect to login if not authenticated
      router.push('/auth/login');
      return;
    }

    const fetchTasks = async () => {
      try {
        setLoading(true);
        const userTasks = await taskApi.getTasks(userId);
        setTasks(userTasks);
      } catch (err: any) {
        // Check if the error is due to a 401 (unauthorized) or other auth issues
        if (err.message.includes('401') || err.message.includes('403') || err.message.toLowerCase().includes('unauthorized') || err.message.toLowerCase().includes('forbidden')) {
          // Redirect to login if unauthorized or forbidden
          router.push('/auth/login');
        } else {
          setError(err.message || 'Failed to fetch tasks');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [userId, router]);

  const handleTaskCreated = () => {
    if (userId) {
      taskApi.getTasks(userId).then(setTasks).catch(console.error);
    }
    setShowForm(false);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleTaskCompletion = async (task: Task) => {
    if (!userId) return;

    try {
      const updatedTask = await taskApi.toggleTaskCompletion(userId, task.id, !task.completed);
      handleTaskUpdated(updatedTask);
    } catch (err: any) {
      setError('Failed to update task completion');
      console.error('Error updating task completion:', err);
    }
  };

  const toggleFormVisibility = () => {
    setShowForm(!showForm);
  };

  if (loading) return (
    <ProtectedRoute unauthorizedRedirect="/auth/login">
      <div className="min-h-screen bg-[var(--bg)] flex items-center justify-center p-4">
        <div className="text-center">
          <div className="rounded-full h-12 w-12 border-b-2 border-[var(--primary)] mx-auto mb-4 animate-spin"></div>
          <p className="text-[var(--muted)]">Loading tasks...</p>
        </div>
      </div>
    </ProtectedRoute>
  );

  if (error) return (
    <ProtectedRoute unauthorizedRedirect="/auth/login">
      <div className="min-h-screen bg-[var(--bg)] flex items-center justify-center p-4">
        <div className="card p-6 max-w-md w-full mx-4">
          <h2 className="text-xl font-bold text-[var(--text)] mb-4">Error</h2>
          <p className="text-[var(--error)] mb-6">Error: {error}</p>
          <button
            onClick={() => window.location.reload()}
            className="btn btn-primary w-full py-3"
          >
            Retry
          </button>
        </div>
      </div>
    </ProtectedRoute>
  );

  return (
    <ProtectedRoute unauthorizedRedirect="/auth/login">
      <div className="min-h-screen bg-[var(--bg)]">
        <PremiumHeader />

        <div className="max-w-4xl mx-auto px-4 py-8">
          {showForm && (
            <div className="mb-8">
              <div className="task-form card p-6 shadow-sm rounded-2xl">
                <h2 className="text-xl font-bold mb-4 text-[var(--text)]">Create New Task</h2>
                <TaskForm onTaskCreated={handleTaskCreated} />
              </div>
            </div>
          )}

          <div className="mb-8">
            <h2 className="text-2xl md:text-3xl font-bold text-[var(--text)] mb-2">Your Tasks</h2>
            <p className="text-[var(--muted)] text-base">Manage and organize your daily activities</p>
            <div className="flex justify-between items-center mt-4">
              <span className="text-[var(--muted)] text-sm">
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
              </span>
            </div>
          </div>

          {tasks.length === 0 ? (
            <PremiumEmptyState onCreateTask={toggleFormVisibility} />
          ) : (
            <div className="space-y-5">
              {tasks.map((task) => (
                <PremiumTaskCard
                  key={task.id}
                  task={task}
                  onTaskCompletion={handleTaskCompletion}
                  onTaskUpdated={handleTaskUpdated}
                  onTaskDeleted={handleTaskDeleted}
                />
              ))}
            </div>
          )}
        </div>

        <FloatingButton onClick={toggleFormVisibility} />
      </div>
    </ProtectedRoute>
  );
}