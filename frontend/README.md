# Repository Tutorial Generator - Frontend

A React TypeScript frontend application that generates conversational tutorials and video content from GitHub repositories.

## Features

- **Input Form**: User-friendly interface to input repository URL and tutorial prompts
- **Tutorial Generation**: AI-powered conversational tutorials with markdown support
- **Video Generation**: Convert tutorials into narrated video content
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Zustand** for state management
- **Axios** for API communication
- **React Markdown** for rendering tutorial content
- **CSS3** with modern animations and responsive design

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── InputForm.tsx              # User input component
│   │   ├── ConversationalTutorial.tsx # Tutorial display with markdown
│   │   ├── VideoPlayer.tsx            # Video playback component
│   │   ├── LoadingSpinner.tsx         # Loading state indicator
│   │   └── ErrorMessage.tsx           # Error handling UI
│   ├── services/
│   │   └── api.ts                     # API service layer
│   ├── store/
│   │   └── useTutorialStore.ts        # Zustand state management
│   ├── types/
│   │   └── index.ts                   # TypeScript type definitions
│   ├── App.tsx                        # Main application component
│   ├── App.css                        # Global styles
│   └── main.tsx                       # Application entry point
├── .env.example                       # Environment variables template
├── package.json                       # Dependencies and scripts
└── vite.config.ts                     # Vite configuration
```

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running (see main project README)

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment configuration:
   ```bash
   cp .env.example .env
   ```

4. Update the `.env` file with your backend API URL:
   ```env
   VITE_API_BASE_URL=http://localhost:5000/api
   ```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building for Production

Build the application:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Component Overview

### InputForm
- Accepts repository URL and tutorial prompt
- Client-side validation for URLs
- Example prompts for quick testing
- Responsive form design

### ConversationalTutorial
- Displays AI-generated tutorial text
- Markdown rendering with syntax highlighting
- Copy to clipboard functionality
- Download as markdown file
- Button to generate video from tutorial

### VideoPlayer
- HTML5 video player with custom controls
- Play/pause, seek, and time display
- Download video functionality
- Share video URL

### LoadingSpinner
- Animated loading indicator
- Progress bar for video generation
- Status messages

### ErrorMessage
- User-friendly error display
- Retry and dismiss actions
- Error handling for API failures

## API Integration

The frontend communicates with the backend through the following endpoints:

- `POST /api/generate-tutorial` - Generate conversational tutorial
- `POST /api/generate-video` - Generate video from tutorial
- `GET /api/video-status/:id` - Poll video generation status

## State Management

Uses Zustand for lightweight, efficient state management:

- User input (prompt, repo URL)
- Tutorial data (text, ID)
- Video data (URL, progress)
- Loading states
- Error handling

## Styling

- Modern gradient background
- Card-based component design
- Smooth animations and transitions
- Responsive breakpoints for mobile/tablet/desktop
- Custom styled buttons and form elements
- Syntax-highlighted code blocks

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Future Enhancements

- Tutorial history and bookmarking
- Social sharing capabilities
- Dark/light mode toggle
- Multiple language support
- Interactive code playground
- User authentication
- Tutorial customization options

## Troubleshooting

### API Connection Issues

If you're having trouble connecting to the backend:

1. Verify the backend is running
2. Check the `VITE_API_BASE_URL` in your `.env` file
3. Check browser console for CORS errors
4. Ensure the backend allows CORS from your frontend origin

### Build Errors

If you encounter build errors:

1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear Vite cache: `rm -rf node_modules/.vite`

## License

See the main project LICENSE file.
