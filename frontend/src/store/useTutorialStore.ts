import { create } from 'zustand';
import type { TutorialState } from '../types';
import { generateTutorial, generateVideo, pollVideoStatus } from '../services/api';

export const useTutorialStore = create<TutorialState>((set, get) => ({
  // Initial state
  prompt: '',
  repoUrl: '',
  tutorialText: null,
  tutorialId: null,
  videoUrl: null,
  isLoadingTutorial: false,
  isLoadingVideo: false,
  videoProgress: 0,
  error: null,
  currentStep: 'input',

  // Actions
  setPrompt: (prompt: string) => set({ prompt }),

  setRepoUrl: (repoUrl: string) => set({ repoUrl }),

  generateTutorial: async () => {
    const { prompt, repoUrl } = get();

    // Validate inputs
    if (!prompt.trim()) {
      set({ error: 'Please enter a prompt' });
      return;
    }

    if (!repoUrl.trim()) {
      set({ error: 'Please enter a repository URL' });
      return;
    }

    // Basic URL validation
    try {
      new URL(repoUrl);
    } catch {
      set({ error: 'Please enter a valid URL' });
      return;
    }

    set({
      isLoadingTutorial: true,
      error: null,
      tutorialText: null,
      tutorialId: null,
    });

    try {
      const response = await generateTutorial({ prompt, repoUrl });
      set({
        tutorialText: response.tutorialText,
        tutorialId: response.tutorialId,
        currentStep: 'tutorial',
        isLoadingTutorial: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to generate tutorial',
        isLoadingTutorial: false,
      });
    }
  },

  generateVideo: async () => {
    const { tutorialId, tutorialText } = get();

    if (!tutorialId || !tutorialText) {
      set({ error: 'No tutorial available to generate video' });
      return;
    }

    set({
      isLoadingVideo: true,
      error: null,
      videoProgress: 0,
      videoUrl: null,
    });

    try {
      // Start video generation
      const response = await generateVideo({ tutorialId, tutorialText });

      if (response.status === 'complete' && response.videoUrl) {
        // Video is ready immediately
        set({
          videoUrl: response.videoUrl,
          currentStep: 'video',
          isLoadingVideo: false,
          videoProgress: 100,
        });
      } else {
        // Need to poll for status
        const videoUrl = await pollVideoStatus(
          tutorialId,
          (progress) => {
            set({ videoProgress: progress });
          }
        );

        set({
          videoUrl,
          currentStep: 'video',
          isLoadingVideo: false,
          videoProgress: 100,
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to generate video',
        isLoadingVideo: false,
        videoProgress: 0,
      });
    }
  },

  resetState: () => set({
    prompt: '',
    repoUrl: '',
    tutorialText: null,
    tutorialId: null,
    videoUrl: null,
    isLoadingTutorial: false,
    isLoadingVideo: false,
    videoProgress: 0,
    error: null,
    currentStep: 'input',
  }),

  clearError: () => set({ error: null }),
}));
