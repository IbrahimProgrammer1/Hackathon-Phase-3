interface ErrorDisplayProps {
  error: string;
  onRetry?: () => void;
}

export default function ErrorDisplay({ error, onRetry }: ErrorDisplayProps) {
  return (
    <div className="border border-red-300 bg-red-50 p-4 rounded-lg mb-4">
      <div className="flex items-center">
        <div className="text-red-500 mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h3 className="text-red-800 font-medium">Error</h3>
          <p className="text-red-600">{error}</p>
        </div>
      </div>
      {onRetry && (
        <div className="mt-3">
          <button
            onClick={onRetry}
            className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded"
          >
            Retry
          </button>
        </div>
      )}
    </div>
  );
}