# Frontend Plan: Repository Tutorial Generator

## Application Flow

1. **User Input** → Prompt + Repo URL
2. **Generate Tutorial** → Backend API returns conversational tutorial text
3. **Display Tutorial** → Show formatted conversational content
4. **Generate Video** → Backend converts tutorial to video
5. **Play Video** → Display final video tutorial to user

---

## Architecture Overview

### Technology Stack

- **Framework**: React with TypeScript
- **State Management**: Context API (or Zustand for more complex state)
- **Styling**: Tailwind CSS or styled-components
- **HTTP Client**: Axios or Fetch API
- **Build Tool**: Vite or Create React App

---

## Component Structure

```
src/
├── components/
│   ├── InputForm.tsx              # User input for prompt & repo URL
│   ├── ConversationalTutorial.tsx # Display tutorial text with formatting
│   ├── VideoPlayer.tsx            # Video display component
│   ├── LoadingSpinner.tsx         # Loading states
│   └── ErrorMessage.tsx           # Error handling UI
├── services/
│   └── api.ts                     # API calls to backend
├── context/
│   └── TutorialContext.tsx        # Global state management
├── types/
│   └── index.ts                   # TypeScript interfaces
├── hooks/
│   └── useTutorialGeneration.ts   # Custom hook for tutorial logic
└── App.tsx                        # Main application component
```

---

## Key Components Breakdown

### 1. InputForm Component

- Two input fields: prompt (textarea) and repo URL (text input)
- Submit button to trigger tutorial generation
- Validation for URL format and required fields
- Clear/reset functionality

### 2. ConversationalTutorial Component

- Display tutorial text in a conversational, readable format
- Support markdown rendering for code blocks
- Step-by-step progression UI
- "Generate Video" button when tutorial is complete
- Copy/share functionality

### 3. VideoPlayer Component

- Video embed/player (HTML5 video or YouTube-style player)
- Playback controls
- Download option
- Full-screen capability
- Progress tracking

### 4. State Management

```typescript
interface TutorialState {
  userInput: { prompt: string; repoUrl: string };
  tutorialText: string | null;
  videoUrl: string | null;
  isLoadingTutorial: boolean;
  isLoadingVideo: boolean;
  error: string | null;
  currentStep: 'input' | 'tutorial' | 'video';
}
```

---

## API Service Layer

### Type Definitions

```typescript
// services/api.ts
interface GenerateTutorialRequest {
  prompt: string;
  repoUrl: string;
}

interface GenerateTutorialResponse {
  tutorialText: string;
  tutorialId: string;
}

interface GenerateVideoRequest {
  tutorialId: string;
  tutorialText: string;
}

interface GenerateVideoResponse {
  videoUrl: string;
  status: 'processing' | 'complete';
}
```

### API Endpoints

- `POST /api/generate-tutorial` - Generate conversational tutorial
- `POST /api/generate-video` - Convert tutorial to video
- `GET /api/video-status/:id` - Poll video generation status

---

## User Journey

### Step 1: Input

- User lands on clean input form
- Enters prompt (e.g., "Explain authentication flow")
- Enters repo URL (e.g., "https://github.com/user/repo")
- Clicks "Generate Tutorial"

### Step 2: Tutorial Generation

- Loading spinner with status message
- Once complete, display conversational tutorial
- Tutorial appears with smooth transitions
- Formatted with headers, code blocks, and explanations

### Step 3: Video Generation

- "Generate Video Tutorial" button appears
- User clicks to start video generation
- Progress indicator (polling backend)
- Video processing status updates

### Step 4: Video Playback

- Video player appears with generated tutorial
- User can watch, pause, replay
- Options to download or share

---

## Key Features

### UX Enhancements

- Progressive disclosure (show steps one at a time)
- Smooth transitions between states
- Persistent state (localStorage) to save progress
- Responsive design for mobile/tablet/desktop
- Dark/light mode toggle

### Error Handling

- Invalid repo URL detection
- API timeout handling
- Rate limiting feedback
- Retry mechanisms

### Performance

- Lazy loading for video player
- Optimistic UI updates
- Request cancellation on unmount
- Debounced input validation

---

## Implementation Checklist

- [x] Set up TypeScript React project with necessary dependencies
- [x] Create TypeScript type definitions
- [x] Create API service layer for backend communication
- [x] Implement state management (Zustand)
- [x] Add loading states and error handling components
- [x] Create InputForm component for prompt and repo URL
- [x] Build ConversationalTutorial component to display text tutorial
- [x] Implement VideoPlayer component for generated video tutorial
- [x] Build main App component
- [x] Style components with CSS
- [x] Add responsive design
- [ ] Implement error boundaries
- [ ] Add unit tests for components
- [ ] Add integration tests for user flows

---

## Future Enhancements

- Tutorial history/bookmarking
- Social sharing capabilities
- Multiple video format exports
- Interactive code playground integration
- User authentication and saved tutorials
- Tutorial customization options (voice, speed, style)
- Multi-language support
