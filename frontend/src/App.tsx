import './App.css';
import { useTutorialStore } from './store/useTutorialStore';
import { InputForm } from './components/InputForm';
import { ConversationalTutorial } from './components/ConversationalTutorial';
import { VideoPlayer } from './components/VideoPlayer';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';

function App() {
  const {
    currentStep,
    isLoadingTutorial,
    isLoadingVideo,
    videoProgress,
    error,
    clearError,
    generateTutorial,
  } = useTutorialStore();

  return (
    <div className="app">
      <div className="app-container">
        {error && (
          <ErrorMessage
            message={error}
            onDismiss={clearError}
            onRetry={currentStep === 'input' ? generateTutorial : undefined}
          />
        )}

        {isLoadingTutorial && (
          <LoadingSpinner message="Analyzing repository and generating your tutorial..." />
        )}

        {isLoadingVideo && (
          <LoadingSpinner
            message="Creating your video tutorial..."
            progress={videoProgress}
          />
        )}

        {!isLoadingTutorial && !isLoadingVideo && (
          <>
            {currentStep === 'input' && <InputForm />}
            {currentStep === 'tutorial' && <ConversationalTutorial />}
            {currentStep === 'video' && <VideoPlayer />}
          </>
        )}
      </div>

      <footer className="app-footer">
        <p>
          Powered by AI • Generate conversational tutorials from any GitHub repository
        </p>
      </footer>
    </div>
  );
}

export default App;
