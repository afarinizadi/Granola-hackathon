interface LoadingSpinnerProps {
  message?: string;
  progress?: number;
}

export const LoadingSpinner = ({ message, progress }: LoadingSpinnerProps) => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      {message && <p className="loading-message">{message}</p>}
      {progress !== undefined && progress > 0 && (
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${progress}%` }}></div>
          <span className="progress-text">{Math.round(progress)}%</span>
        </div>
      )}
    </div>
  );
};
