'use client';

interface PremiumEmptyStateProps {
  onCreateTask: () => void;
}

export default function PremiumEmptyState({ onCreateTask }: PremiumEmptyStateProps) {
  return (
    <div className="empty-state card p-8 md:p-12 text-center">
      <div className="mx-auto w-16 h-16 md:w-20 md:h-20 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center mb-6 md:mb-8">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 md:h-10 md:w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      </div>
      <h3 className="text-xl md:text-2xl font-bold text-text mb-3">Your day, perfectly organized</h3>
      <p className="text-muted mb-6 md:mb-8 max-w-md mx-auto">
        Add your first task and take control of your productivity. Transform your ideas into actionable steps.
      </p>
      <button
        onClick={onCreateTask}
        className="btn btn-primary px-6 py-3 rounded-xl text-base font-medium shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Create Your First Task
      </button>
    </div>
  );
}