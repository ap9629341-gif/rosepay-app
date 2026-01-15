/**
 * Loading Spinner Component
 * 
 * WHAT THIS DOES:
 * - Shows a loading spinner
 * - Reusable across the app
 * - Beautiful animated spinner
 */

function LoadingSpinner({ size = 'md', text = 'Loading...' }) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div
        className={`${sizeClasses[size]} border-4 border-rose-200 border-t-rose-600 rounded-full animate-spin`}
      />
      {text && <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{text}</p>}
    </div>
  );
}

export default LoadingSpinner;
