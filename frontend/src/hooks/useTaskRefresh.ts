/**
 * Task Refresh Event System
 *
 * Provides a lightweight event system to notify components when tasks are modified.
 * Uses localStorage events for cross-component communication.
 *
 * T035: Task refresh trigger system
 */

'use client';

import { useEffect, useCallback, useRef } from 'react';

// Event types for task modifications
export type TaskEventType = 'task_created' | 'task_updated' | 'task_deleted' | 'tasks_refresh';

export interface TaskEvent {
  type: TaskEventType;
  taskId?: number;
  timestamp: number;
}

// Storage key for task events
const TASK_EVENT_KEY = 'task_refresh_event';

/**
 * Emit a task event to notify other components
 *
 * @param type - Type of event (created, updated, deleted, refresh)
 * @param taskId - Optional task ID for specific task events
 */
export function emitTaskEvent(type: TaskEventType, taskId?: number): void {
  if (typeof window === 'undefined') return;

  const event: TaskEvent = {
    type,
    taskId,
    timestamp: Date.now(),
  };

  // Store event in localStorage for cross-tab communication
  localStorage.setItem(TASK_EVENT_KEY, JSON.stringify(event));

  // Dispatch a custom event for same-window listeners
  window.dispatchEvent(new CustomEvent('task-update', { detail: event }));
}

/**
 * Hook to listen for task update events
 *
 * @param onTaskCreated - Callback when a task is created
 * @param onTaskUpdated - Callback when a task is updated
 * @param onTaskDeleted - Callback when a task is deleted
 * @param onTasksRefresh - Callback for general refresh
 */
export function useTaskRefreshEvents({
  onTaskCreated,
  onTaskUpdated,
  onTaskDeleted,
  onTasksRefresh,
}: {
  onTaskCreated?: () => void;
  onTaskUpdated?: () => void;
  onTaskDeleted?: () => void;
  onTasksRefresh?: () => void;
} = {}) {
  const lastEventRef = useRef<number>(0);

  const handleEvent = useCallback((event: Event) => {
    const customEvent = event as CustomEvent<TaskEvent>;
    const eventData = customEvent.detail;

    // Prevent duplicate events (debounce)
    if (eventData.timestamp <= lastEventRef.current) {
      return;
    }
    lastEventRef.current = eventData.timestamp;

    switch (eventData.type) {
      case 'task_created':
        onTaskCreated?.();
        break;
      case 'task_updated':
        onTaskUpdated?.();
        break;
      case 'task_deleted':
        onTaskDeleted?.();
        break;
      case 'tasks_refresh':
        onTasksRefresh?.();
        break;
    }
  }, [onTaskCreated, onTaskUpdated, onTaskDeleted, onTasksRefresh]);

  useEffect(() => {
    // Listen for custom events
    window.addEventListener('task-update', handleEvent);

    // Also listen for storage events (cross-tab)
    const handleStorageEvent = (event: StorageEvent) => {
      if (event.key === TASK_EVENT_KEY && event.newValue) {
        try {
          const eventData = JSON.parse(event.newValue) as TaskEvent;
          // Dispatch locally to trigger handleEvent
          window.dispatchEvent(new CustomEvent('task-update', { detail: eventData }));
        } catch (e) {
          console.error('Failed to parse task event:', e);
        }
      }
    };

    window.addEventListener('storage', handleStorageEvent);

    return () => {
      window.removeEventListener('task-update', handleEvent);
      window.removeEventListener('storage', handleStorageEvent);
    };
  }, [handleEvent]);
}

/**
 * Hook specifically for refreshing task list
 * Provides a refresh function that can be called externally
 */
export function useTaskListRefresh() {
  const refreshFnRef = useRef<(() => void) | null>(null);

  const registerRefresh = useCallback((fn: () => void) => {
    refreshFnRef.current = fn;
  }, []);

  const refresh = useCallback(() => {
    refreshFnRef.current?.();
  }, []);

  // Listen for refresh events
  useTaskRefreshEvents({
    onTasksRefresh: refresh,
  });

  return { registerRefresh, refresh };
}
