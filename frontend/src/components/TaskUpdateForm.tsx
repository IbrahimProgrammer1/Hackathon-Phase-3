'use client';

import { useState } from 'react';
import { Task, taskApi } from '@/lib/api';
import { AuthService } from '@/lib/auth';

interface TaskUpdateFormProps {
  task: Task;
  onTaskUpdated?: (updatedTask: Task) => void;
  onCancel?: () => void;
}

export default function TaskUpdateForm({ task, onTaskUpdated, onCancel }: TaskUpdateFormProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const userId = AuthService.getCurrentUser()?.id;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (!userId) {
      setError('User not authenticated');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const updatedTask = await taskApi.updateTask(userId, task.id, {
        title: title.trim(),
        description: description.trim() || undefined
      });

      if (onTaskUpdated) {
        onTaskUpdated(updatedTask);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-5 md:p-6 mt-5 border-2 border-primary/20 rounded-xl">
      <h3 className="text-lg font-semibold mb-4 text-text flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Update Task
      </h3>

      {error && <div className="text-error text-sm p-3 bg-error/10 rounded-lg mb-4">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="update-title" className="block text-sm font-medium mb-2 text-muted">
            Task Title *
          </label>
          <input
            type="text"
            id="update-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="input w-full"
            placeholder="What needs to be done?"
            required
          />
        </div>

        <div>
          <label htmlFor="update-description" className="block text-sm font-medium mb-2 text-muted">
            Description
          </label>
          <textarea
            id="update-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="input w-full"
            placeholder="Add more details (optional)"
            rows={2}
          />
        </div>

        <div className="flex gap-3 pt-2">
          <button
            type="submit"
            disabled={loading}
            className={`btn btn-primary flex-1 py-2.5 rounded-xl ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </>
            ) : (
              'Save Changes'
            )}
          </button>

          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className={`btn btn-secondary py-2.5 px-4 rounded-xl ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}