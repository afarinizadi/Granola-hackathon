import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useTutorialStore } from '../store/useTutorialStore';

export const ConversationalTutorial = () => {
  const {
    tutorialText,
    generateVideo,
    isLoadingVideo,
    resetState,
  } = useTutorialStore();

  const [copied, setCopied] = useState(false);

  if (!tutorialText) {
    return null;
  }

  const handleCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(tutorialText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([tutorialText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tutorial.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="tutorial-container">
      <div className="tutorial-header">
        <h2>Your Tutorial</h2>
        <div className="tutorial-actions">
          <button
            className="btn btn-icon"
            onClick={handleCopyToClipboard}
            title="Copy to clipboard"
          >
            {copied ? '✓ Copied!' : '📋 Copy'}
          </button>
          <button
            className="btn btn-icon"
            onClick={handleDownload}
            title="Download as markdown"
          >
            📥 Download
          </button>
          <button
            className="btn btn-secondary"
            onClick={resetState}
            title="Start over"
          >
            🔄 New Tutorial
          </button>
        </div>
      </div>

      <div className="tutorial-content">
        <ReactMarkdown
          components={{
            // Custom rendering for code blocks
            code(props) {
              const { node, inline, className, children, ...rest } = props as any;
              const match = /language-(\w+)/.exec(className || '');
              return !inline ? (
                <div className="code-block-wrapper">
                  {match && <span className="code-language">{match[1]}</span>}
                  <pre className="code-block">
                    <code className={className} {...rest}>
                      {children}
                    </code>
                  </pre>
                </div>
              ) : (
                <code className="inline-code" {...rest}>
                  {children}
                </code>
              );
            },
            // Custom rendering for headings
            h1: ({ children }) => <h1 className="tutorial-h1">{children}</h1>,
            h2: ({ children }) => <h2 className="tutorial-h2">{children}</h2>,
            h3: ({ children }) => <h3 className="tutorial-h3">{children}</h3>,
            // Custom rendering for paragraphs
            p: ({ children }) => <p className="tutorial-paragraph">{children}</p>,
            // Custom rendering for lists
            ul: ({ children }) => <ul className="tutorial-ul">{children}</ul>,
            ol: ({ children }) => <ol className="tutorial-ol">{children}</ol>,
            li: ({ children }) => <li className="tutorial-li">{children}</li>,
            // Custom rendering for links
            a: ({ href, children }) => (
              <a href={href} className="tutorial-link" target="_blank" rel="noopener noreferrer">
                {children}
              </a>
            ),
            // Custom rendering for blockquotes
            blockquote: ({ children }) => (
              <blockquote className="tutorial-blockquote">{children}</blockquote>
            ),
          }}
        >
          {tutorialText}
        </ReactMarkdown>
      </div>

      <div className="tutorial-footer">
        <div className="video-cta">
          <h3>Ready to watch this as a video?</h3>
          <p>Generate a video tutorial with AI-powered narration and visuals</p>
          <button
            className="btn btn-primary btn-large"
            onClick={generateVideo}
            disabled={isLoadingVideo}
          >
            {isLoadingVideo ? '🎬 Generating Video...' : '🎬 Generate Video Tutorial'}
          </button>
        </div>
      </div>
    </div>
  );
};
