interface FloatingButtonProps {
  onClick: () => void;
  icon?: React.ReactNode;
  className?: string;
}

export default function FloatingButton({ onClick, icon, className = '' }: FloatingButtonProps) {
  return (
    <button
      className={`fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] shadow-lg flex items-center justify-center text-white z-50 transition-all duration-300 hover:shadow-xl hover:scale-106 active:scale-95 group ${className}`}
      onClick={onClick}
      title="Add Task"
    >
      {icon || (
        <div className="relative">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
        </div>
      )}
      <div className="absolute -top-8 bg-gray-800 text-white text-xs rounded py-1 px-2 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
        Add Task
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-full w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-800"></div>
      </div>
    </button>
  );
}