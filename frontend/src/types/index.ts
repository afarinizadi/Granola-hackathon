// API Request/Response Types
export interface GenerateTutorialRequest {
  prompt: string;
  repoUrl: string;
}

export interface GenerateTutorialResponse {
  tutorialText: string;
  tutorialId: string;
  metadata?: {
    repoName?: string;
    language?: string;
    stars?: number;
    description?: string;
    stats?: {
      totalFiles?: number;
      totalLines?: number;
      languages?: Record<string, number>;
    };
  };
}

export interface GenerateVideoRequest {
  tutorialId: string;
  tutorialText: string;
}

export interface GenerateVideoResponse {
  videoUrl: string;
  status: 'processing' | 'complete';
}

export interface VideoStatusResponse {
  videoUrl?: string;
  status: 'processing' | 'complete' | 'failed';
  progress?: number;
}

// Application State Types
export type AppStep = 'input' | 'tutorial' | 'video';

export interface TutorialState {
  // User input
  prompt: string;
  repoUrl: string;

  // Tutorial data
  tutorialText: string | null;
  tutorialId: string | null;

  // Video data
  videoUrl: string | null;

  // Loading states
  isLoadingTutorial: boolean;
  isLoadingVideo: boolean;
  videoProgress: number;

  // Error handling
  error: string | null;

  // Current step
  currentStep: AppStep;

  // Actions
  setPrompt: (prompt: string) => void;
  setRepoUrl: (repoUrl: string) => void;
  generateTutorial: () => Promise<void>;
  generateVideo: () => Promise<void>;
  resetState: () => void;
  clearError: () => void;
}
