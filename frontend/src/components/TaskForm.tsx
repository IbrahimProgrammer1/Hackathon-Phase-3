'use client';

import { useState } from 'react';
import { taskApi } from '@/lib/api';
import { AuthService } from '@/lib/auth';

interface TaskFormProps {
  onTaskCreated?: () => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
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
      await taskApi.createTask(userId, {
        title: title.trim(),
        description: description.trim()
      });

      setTitle('');
      setDescription('');

      if (onTaskCreated) {
        onTaskCreated();
      }
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && <div className="text-error text-sm p-3 bg-error/10 rounded-lg">{error}</div>}

      <div>
        <label htmlFor="title" className="block text-sm font-medium mb-2 text-muted">
          Task Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="input w-full"
          placeholder="What needs to be done?"
          required
          autoFocus
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium mb-2 text-muted">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="input w-full"
          placeholder="Add more details (optional)"
          rows={3}
        />
      </div>

      <div className="flex gap-3 pt-2">
        <button
          type="submit"
          disabled={loading}
          className={`btn btn-primary flex-1 py-3 rounded-xl ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating...
            </>
          ) : (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Task
            </>
          )}
        </button>

        <button
          type="button"
          onClick={() => {
            setTitle('');
            setDescription('');
            if (onTaskCreated) onTaskCreated();
          }}
          className="btn btn-secondary py-3 px-4 rounded-xl"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}