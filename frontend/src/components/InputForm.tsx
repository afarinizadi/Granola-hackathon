import { useState } from 'react';
import { useTutorialStore } from '../store/useTutorialStore';

export const InputForm = () => {
  const {
    prompt,
    repoUrl,
    setPrompt,
    setRepoUrl,
    generateTutorial,
    isLoadingTutorial,
  } = useTutorialStore();

  const [validationError, setValidationError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError('');

    // Client-side validation
    if (!prompt.trim()) {
      setValidationError('Please enter a prompt');
      return;
    }

    if (!repoUrl.trim()) {
      setValidationError('Please enter a repository URL');
      return;
    }

    // Validate URL format
    try {
      const url = new URL(repoUrl);
      if (!url.protocol.startsWith('http')) {
        setValidationError('Please enter a valid HTTP/HTTPS URL');
        return;
      }
    } catch {
      setValidationError('Please enter a valid URL');
      return;
    }

    await generateTutorial();
  };

  const handleReset = () => {
    setPrompt('');
    setRepoUrl('');
    setValidationError('');
  };

  return (
    <div className="input-form-container">
      <div className="form-header">
        <h1>Repository Tutorial Generator</h1>
        <p>Generate an AI-powered conversational tutorial from any GitHub repository</p>
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
          <label htmlFor="repoUrl">Repository URL</label>
          <input
            id="repoUrl"
            type="text"
            className="form-input"
            placeholder="https://github.com/username/repository"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            disabled={isLoadingTutorial}
          />
          <small className="form-hint">
            Enter the full URL of the GitHub repository you want to learn about
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="prompt">Your Question or Topic</label>
          <textarea
            id="prompt"
            className="form-textarea"
            placeholder="e.g., Explain the authentication flow, How does the API routing work?, Walk me through the database schema..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isLoadingTutorial}
            rows={4}
          />
          <small className="form-hint">
            Describe what you want to learn about this repository
          </small>
        </div>

        {validationError && (
          <div className="validation-error">
            {validationError}
          </div>
        )}

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary btn-large"
            disabled={isLoadingTutorial}
          >
            {isLoadingTutorial ? 'Generating Tutorial...' : 'Generate Tutorial'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleReset}
            disabled={isLoadingTutorial}
          >
            Clear
          </button>
        </div>
      </form>

      <div className="form-footer">
        <h3>Examples:</h3>
        <div className="example-prompts">
          <button
            className="example-prompt"
            onClick={() => {
              setPrompt('Explain the authentication and authorization flow');
              setRepoUrl('https://github.com/vercel/next.js');
            }}
            disabled={isLoadingTutorial}
          >
            Authentication flow in Next.js
          </button>
          <button
            className="example-prompt"
            onClick={() => {
              setPrompt('How does the state management work?');
              setRepoUrl('https://github.com/facebook/react');
            }}
            disabled={isLoadingTutorial}
          >
            State management in React
          </button>
          <button
            className="example-prompt"
            onClick={() => {
              setPrompt('Walk me through the API routing architecture');
              setRepoUrl('https://github.com/nestjs/nest');
            }}
            disabled={isLoadingTutorial}
          >
            API routing in NestJS
          </button>
        </div>
      </div>
    </div>
  );
};
