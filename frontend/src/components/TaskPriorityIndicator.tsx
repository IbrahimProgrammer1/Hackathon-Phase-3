import { Task } from '@/lib/api';

interface TaskPriorityIndicatorProps {
  task: Task;
}

export default function TaskPriorityIndicator({ task }: TaskPriorityIndicatorProps) {
  // For now, we'll use a simple heuristic based on task characteristics
  // In a real app, you might have a priority field in your task model
  let priorityClass = '';
  let priorityLabel = '';

  // Simple priority determination based on length of title or description
  const taskComplexity = (task.title.length + (task.description?.length || 0));

  if (taskComplexity > 100) {
    priorityClass = 'task-priority-high';
    priorityLabel = 'High Priority';
  } else if (taskComplexity > 50) {
    priorityClass = 'task-priority-medium';
    priorityLabel = 'Medium Priority';
  } else {
    priorityClass = 'task-priority-low';
    priorityLabel = 'Low Priority';
  }

  return (
    <div className={`w-1 h-full ${priorityClass}`}></div>
  );
}