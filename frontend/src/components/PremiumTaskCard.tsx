import { Task } from '@/lib/api';
import TaskActions from './TaskActions';

interface PremiumTaskCardProps {
  task: Task;
  onTaskCompletion: (task: Task) => void;
  onTaskUpdated: (updatedTask: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}

export default function PremiumTaskCard({
  task,
  onTaskCompletion,
  onTaskUpdated,
  onTaskDeleted
}: PremiumTaskCardProps) {
  // Determine priority based on task characteristics
  const taskComplexity = (task.title.length + (task.description?.length || 0));
  let priorityColor = 'bg-[var(--primary)]';
  let priorityLabel = 'Normal';

  if (taskComplexity > 100) {
    priorityColor = 'bg-[var(--accent-high)]';
    priorityLabel = 'High Priority';
  } else if (taskComplexity > 50) {
    priorityColor = 'bg-[var(--accent-medium)]';
    priorityLabel = 'Medium Priority';
  } else {
    priorityColor = 'bg-[var(--accent-low)]';
    priorityLabel = 'Low Priority';
  }

  return (
    <div className="task-card card p-6 rounded-2xl shadow-sm transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5 group">
      <div className={`w-1.5 rounded-l-lg ${priorityColor} transition-all duration-300`}></div>
      <div className="flex-1 pl-5">
        <div className="flex items-start gap-4">
          <div
            className={`checkbox mt-0.5 cursor-pointer w-5 h-5 border-2 rounded-lg flex items-center justify-center transition-all duration-200 ${
              task.completed
                ? 'bg-[var(--primary)] border-[var(--primary)]'
                : 'border-[var(--border)] hover:border-[var(--primary)] group-hover:scale-105'
            }`}
            onClick={() => onTaskCompletion(task)}
          >
            {task.completed && (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-3.5 w-3.5 text-white"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <h3
              className={`text-base md:text-lg font-semibold truncate ${
                task.completed
                  ? 'line-through text-[var(--muted)] opacity-60'
                  : 'text-[var(--text)]'
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p
                className={`mt-2 text-sm md:text-base truncate ${
                  task.completed
                    ? 'text-[var(--muted)] opacity-60'
                    : 'text-[var(--muted)]'
                }`}
              >
                {task.description}
              </p>
            )}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between mt-4 gap-3 sm:gap-0">
              <div className="flex items-center gap-3">
                <span className={`text-xs md:text-sm px-2.5 py-1 rounded-full ${
                  task.completed
                    ? 'bg-[var(--success)]/[0.1] text-[var(--success)]'
                    : 'bg-[var(--primary)]/[0.1] text-[var(--primary)]'
                }`}>
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
                <span className="text-xs text-[var(--muted)]">
                  {new Date(task.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="task-actions-container">
                <TaskActions
                  task={task}
                  onTaskUpdated={onTaskUpdated}
                  onTaskDeleted={onTaskDeleted}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}