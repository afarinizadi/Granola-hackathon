interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
  onRetry?: () => void;
}

export const ErrorMessage = ({ message, onDismiss, onRetry }: ErrorMessageProps) => {
  return (
    <div className="error-container">
      <div className="error-icon">⚠️</div>
      <p className="error-message">{message}</p>
      <div className="error-actions">
        {onRetry && (
          <button className="btn btn-primary" onClick={onRetry}>
            Retry
          </button>
        )}
        {onDismiss && (
          <button className="btn btn-secondary" onClick={onDismiss}>
            Dismiss
          </button>
        )}
      </div>
    </div>
  );
};
