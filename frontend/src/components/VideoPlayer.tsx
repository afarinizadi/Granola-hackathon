import { useRef, useState } from 'react';
import { useTutorialStore } from '../store/useTutorialStore';

export const VideoPlayer = () => {
  const { videoUrl, resetState } = useTutorialStore();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  if (!videoUrl) {
    return null;
  }

  const handlePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const handleDownload = () => {
    const a = document.createElement('a');
    a.href = videoUrl;
    a.download = 'tutorial-video.mp4';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="video-container">
      <div className="video-header">
        <h2>Your Video Tutorial</h2>
        <div className="video-actions">
          <button
            className="btn btn-icon"
            onClick={handleDownload}
            title="Download video"
          >
            📥 Download
          </button>
          <button
            className="btn btn-secondary"
            onClick={resetState}
            title="Create new tutorial"
          >
            🔄 New Tutorial
          </button>
        </div>
      </div>

      <div className="video-player-wrapper">
        <video
          ref={videoRef}
          className="video-player"
          src={videoUrl}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onEnded={() => setIsPlaying(false)}
        />

        <div className="video-controls">
          <button
            className="control-btn play-pause"
            onClick={handlePlayPause}
            aria-label={isPlaying ? 'Pause' : 'Play'}
          >
            {isPlaying ? '⏸️' : '▶️'}
          </button>

          <div className="time-display">
            {formatTime(currentTime)} / {formatTime(duration)}
          </div>

          <input
            type="range"
            className="seek-bar"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            step="0.1"
          />
        </div>
      </div>

      <div className="video-footer">
        <div className="video-info">
          <h3>🎉 Your tutorial video is ready!</h3>
          <p>
            Watch your AI-generated tutorial video. You can download it, share it, or create a new
            tutorial.
          </p>
        </div>

        <div className="share-section">
          <h4>Share your tutorial:</h4>
          <div className="share-buttons">
            <button
              className="btn btn-share"
              onClick={() => {
                navigator.clipboard.writeText(videoUrl);
                alert('Video URL copied to clipboard!');
              }}
            >
              📋 Copy Link
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
