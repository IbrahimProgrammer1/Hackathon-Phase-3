import { useState } from 'react';
import { Task, taskApi } from '@/lib/api';
import { AuthService } from '@/lib/auth';

interface TaskDetailProps {
  task: Task;
  onTaskUpdated?: (updatedTask: Task) => void;
  onTaskDeleted?: (taskId: number) => void;
}

export default function TaskDetail({ task, onTaskUpdated, onTaskDeleted }: TaskDetailProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const userId = AuthService.getCurrentUser()?.id;

  const handleUpdate = async () => {
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
        description: description.trim()
      });

      setIsEditing(false);
      if (onTaskUpdated) {
        onTaskUpdated(updatedTask);
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
        setError(err.message || 'Failed to update task');
      }
    } finally {
      setLoading(false);
    }
  };

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
        if (onTaskDeleted) {
          onTaskDeleted(task.id);
        }
      } else {
        setError(err.message || 'Failed to update task completion');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border p-4 rounded-lg mb-4">
      {isEditing ? (
        <div>
          <div className="mb-4">
            <label htmlFor="edit-title" className="block text-sm font-medium mb-1">
              Title *
            </label>
            <input
              type="text"
              id="edit-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="edit-description" className="block text-sm font-medium mb-1">
              Description
            </label>
            <textarea
              id="edit-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded"
              rows={3}
            />
          </div>
          {error && <div className="text-red-500 mb-4">{error}</div>}
          <div className="flex space-x-2">
            <button
              onClick={handleUpdate}
              disabled={loading}
              className={`px-4 py-2 rounded ${
                loading
                  ? 'bg-blue-400 cursor-not-allowed'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
            >
              {loading ? 'Updating...' : 'Save'}
            </button>
            <button
              onClick={() => {
                setIsEditing(false);
                setTitle(task.title);
                setDescription(task.description || '');
                setError(null);
              }}
              className="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <h2 className="text-lg font-semibold">{task.title}</h2>
          {task.description && <p className="text-gray-600 mt-2">{task.description}</p>}
          <div className="flex items-center mt-2">
            <span className={`mr-2 ${task.completed ? 'text-green-500' : 'text-yellow-500'}`}>
              {task.completed ? '✓ Completed' : '○ Incomplete'}
            </span>
          </div>
          <div className="text-sm text-gray-500 mt-2">
            Created: {new Date(task.created_at).toLocaleString()}
          </div>
          <div className="text-sm text-gray-500">
            Updated: {new Date(task.updated_at).toLocaleString()}
          </div>
          <div className="mt-4 flex space-x-2">
            <button
              onClick={() => setIsEditing(true)}
              className="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded"
            >
              Edit
            </button>
            <button
              onClick={handleToggleCompletion}
              disabled={loading}
              className={`px-3 py-1 rounded ${
                task.completed
                  ? 'bg-yellow-500 hover:bg-yellow-600'
                  : 'bg-green-500 hover:bg-green-600'
              } text-white`}
            >
              {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
            </button>
            <button
              onClick={handleDelete}
              disabled={loading}
              className="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded"
            >
              Delete
            </button>
          </div>
          {error && <div className="text-red-500 mt-2">{error}</div>}
        </div>
      )}
    </div>
  );
}