'use client';

import { useState } from 'react';
import { Task, taskApi } from '@/lib/api';
import { AuthService } from '@/lib/auth';
import TaskUpdateForm from './TaskUpdateForm';

interface TaskActionsProps {
  task: Task;
  onTaskUpdated?: (updatedTask: Task) => void;
  onTaskDeleted?: (taskId: number) => void;
}

export default function TaskActions({ task, onTaskUpdated, onTaskDeleted }: TaskActionsProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showUpdateForm, setShowUpdateForm] = useState(false);

  const userId = AuthService.getCurrentUser()?.id;

  const handleDelete = async () => {
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await taskApi.deleteTask(userId, task.id);

      if (onTaskDeleted) {
        onTaskDeleted(task.id);
      }
    } catch (err: any) {
      // Check if the error is due to a 404 (task not found or doesn't belong to user)
      if (err.message.includes('404') || err.message.toLowerCase().includes('not found')) {
        setError('Task not found or does not belong to you');
        // Optionally, handle the case where the task was deleted by another user
        if (onTaskDeleted) {
          onTaskDeleted(task.id);
        }
      } else {
        setError(err.message || 'Failed to delete task');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggleCompletion = async () => {
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const updatedTask = await taskApi.toggleTaskCompletion(userId, task.id, !task.completed);

      if (onTaskUpdated) {
        onTaskUpdated(updatedTask);
      }
    } catch (err: any) {
      // Check if the error is due to a 404 (task not found or doesn't belong to user)
      if (err.message.includes('404') || err.message.toLowerCase().includes('not found')) {
        setError('Task not found or does not belong to you');
        // Optionally, handle the case where the task was deleted by another user
        if (onTaskUpdated) {
          // Update the task to reflect that it might not exist anymore
          onTaskUpdated({...task, completed: !task.completed});
        }
      } else {
        setError(err.message || 'Failed to update task completion');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateSuccess = (updatedTask: Task) => {
    if (onTaskUpdated) {
      onTaskUpdated(updatedTask);
    }
    setShowUpdateForm(false);
  };

  return (
    <div className="task-actions flex flex-wrap gap-2 sm:gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
      <button
        onClick={handleToggleCompletion}
        disabled={loading}
        className={`btn btn-secondary text-xs px-3 py-2 min-w-[100px] ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
        title={task.completed ? 'Mark Incomplete' : 'Mark Complete'}
      >
        {loading ? (
          <svg className="animate-spin h-4 w-4 text-current mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        ) : task.completed ? (
          'Incomplete'
        ) : (
          'Complete'
        )}
      </button>
      <button
        onClick={() => setShowUpdateForm(!showUpdateForm)}
        disabled={loading}
        className={`btn btn-secondary text-xs px-3 py-2 ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
        title="Edit Task"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
      </button>
      <button
        onClick={handleDelete}
        disabled={loading}
        className={`btn btn-danger text-xs px-3 py-2 text-[var(--error)] hover:bg-[var(--error)]/[0.1] hover:text-[var(--error)] ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
        title="Delete Task"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
      {error && <div className="text-[var(--error)] text-xs mt-1 w-full">{error}</div>}

      {showUpdateForm && (
        <TaskUpdateForm
          task={task}
          onTaskUpdated={handleUpdateSuccess}
          onCancel={() => setShowUpdateForm(false)}
        />
      )}
    </div>
  );
}