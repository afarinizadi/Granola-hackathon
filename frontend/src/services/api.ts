import axios from 'axios';
import type {
  GenerateTutorialRequest,
  GenerateTutorialResponse,
  GenerateVideoRequest,
  GenerateVideoResponse,
  VideoStatusResponse,
} from '../types';

// Configure base URL - adjust this based on your backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for tutorial generation
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data.error || error.response.data.message || 'An error occurred';
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request made but no response
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

/**
 * Generate a conversational tutorial from a repository
 */
export const generateTutorial = async (
  request: GenerateTutorialRequest
): Promise<GenerateTutorialResponse> => {
  // Map frontend request to backend format
  const backendRequest = {
    repo_url: request.repoUrl,
    prompt: request.prompt,
  };

  const response = await apiClient.post('/analyze', backendRequest);

  // Map backend response to frontend format
  if (!response.data.success) {
    throw new Error(response.data.error || 'Failed to generate tutorial');
  }

  return {
    tutorialText: response.data.summary,
    tutorialId: response.data.repo_name || 'tutorial',
    metadata: {
      repoName: response.data.repo_name,
      language: response.data.metadata?.language,
      stars: response.data.metadata?.stars,
      description: response.data.metadata?.description,
      stats: response.data.stats,
    },
  };
};

/**
 * Generate a video tutorial from the conversational text
 * Note: This assumes a video generation endpoint exists
 */
export const generateVideo = async (
  request: GenerateVideoRequest
): Promise<GenerateVideoResponse> => {
  const response = await apiClient.post('/generate-video', {
    tutorialId: request.tutorialId,
    tutorialText: request.tutorialText,
  });

  // Map backend response to frontend format
  if (!response.data.success) {
    throw new Error(response.data.error || 'Failed to generate video');
  }

  return {
    videoUrl: response.data.videoUrl,
    status: response.data.status || 'complete',
  };
};

/**
 * Poll the status of video generation
 * Note: This assumes a video status endpoint exists
 */
export const getVideoStatus = async (
  tutorialId: string
): Promise<VideoStatusResponse> => {
  const response = await apiClient.get(`/video-status/${tutorialId}`);

  // Map backend response to frontend format
  if (!response.data.success) {
    throw new Error(response.data.error || 'Failed to get video status');
  }

  return {
    videoUrl: response.data.videoUrl,
    status: response.data.status,
    progress: response.data.progress,
  };
};

/**
 * Utility function to poll video status until complete
 */
export const pollVideoStatus = async (
  tutorialId: string,
  onProgress?: (progress: number) => void,
  pollInterval: number = 2000
): Promise<string> => {
  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        const status = await getVideoStatus(tutorialId);

        if (status.progress !== undefined && onProgress) {
          onProgress(status.progress);
        }

        if (status.status === 'complete' && status.videoUrl) {
          resolve(status.videoUrl);
        } else if (status.status === 'failed') {
          reject(new Error('Video generation failed'));
        } else {
          // Continue polling
          setTimeout(poll, pollInterval);
        }
      } catch (error) {
        reject(error);
      }
    };

    poll();
  });
};
