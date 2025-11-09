# GitHub Repository Analyzer

A Python serverless application that analyzes GitHub repositories using Claude API and generates comprehensive codebase summaries.

## Overview

This application fetches GitHub repository data, processes the codebase structure, and uses Claude AI to provide intelligent analysis and insights about the code.

## Features

- Fetch repository metadata and file structure from GitHub
- Extract dependencies from various package managers (npm, pip, cargo, go, maven, gradle)
- Build comprehensive codebase context summaries
- Analyze code using Claude AI with custom prompts
- RESTful API endpoint for easy integration
- Support for both public and private repositories
- CORS-enabled for cross-origin requests

## Tech Stack

- **Platform**: Vercel Serverless Functions
- **Language**: Python 3.12+
- **APIs**:
  - Anthropic Claude API
  - GitHub API (via PyGithub)

## Project Structure

```
/
├── api/
│   └── analyze.py          # Vercel serverless function
├── src/
│   └── documentation_generator/
│       ├── __init__.py
│       ├── github_client.py    # GitHub API interactions
│       ├── claude_client.py    # Claude API interactions
│       └── processor.py        # Codebase processing logic
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
├── .env.example           # Environment variables template
├── test_local.py          # Local testing script
└── README.md
```

## Setup

### Prerequisites

- Python 3.12 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- GitHub Personal Access Token (optional, for private repos)
- Vercel account (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Granola-hackathon
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key
   GITHUB_TOKEN=your_github_token_here  # Optional
   ```

4. **Test locally with Vercel CLI** (optional)
   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Run locally
   vercel dev
   ```

## Deployment to Vercel

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Set environment variables**
   ```bash
   vercel env add ANTHROPIC_API_KEY
   vercel env add GITHUB_TOKEN  # Optional
   ```

5. **Deploy to production**
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure environment variables:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `GITHUB_TOKEN`: Your GitHub token (optional)
5. Click "Deploy"

## API Usage

### Endpoint

```
POST /api/analyze
```

### Request Body

```json
{
  "repo_url": "https://github.com/user/repo",
  "prompt": "Analyze this codebase and provide a comprehensive summary of its architecture and main features"
}
```

### Optional Fields

```json
{
  "repo_url": "https://github.com/user/repo",
  "prompt": "Your analysis prompt",
  "github_token": "optional_github_token",
  "anthropic_api_key": "optional_anthropic_key"
}
```

### Response

```json
{
  "success": true,
  "repo_url": "https://github.com/user/repo",
  "repo_name": "user/repo",
  "summary": "Detailed AI-generated analysis...",
  "stats": {
    "total_files": 42,
    "total_dirs": 10,
    "total_size_kb": 1234.5
  },
  "metadata": {
    "language": "Python",
    "stars": 100,
    "description": "Repository description"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message",
  "status_code": 400
}
```

## Example Usage

### Using cURL

```bash
curl -X POST https://your-deployment.vercel.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/anthropics/anthropic-sdk-python",
    "prompt": "Analyze this SDK and explain its main components"
  }'
```

### Using JavaScript/Fetch

```javascript
const response = await fetch('https://your-deployment.vercel.app/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    repo_url: 'https://github.com/anthropics/anthropic-sdk-python',
    prompt: 'Analyze this SDK and explain its main components'
  })
});

const data = await response.json();
console.log(data.summary);
```

### Using Python

```python
import requests

response = requests.post(
    'https://your-deployment.vercel.app/api/analyze',
    json={
        'repo_url': 'https://github.com/anthropics/anthropic-sdk-python',
        'prompt': 'Analyze this SDK and explain its main components'
    }
)

data = response.json()
print(data['summary'])
```

## API Information Endpoint

Get API information and usage details:

```bash
curl https://your-deployment.vercel.app/api/analyze
```

## Error Handling

The API handles various error cases:

- **400 Bad Request**: Invalid JSON, missing required fields, invalid GitHub URL
- **500 Internal Server Error**: API failures, missing API keys, repository access errors

## Rate Limits

- **GitHub API**: 60 requests/hour (unauthenticated), 5000 requests/hour (authenticated with token)
- **Claude API**: Depends on your Anthropic plan

## Security Notes

- Never commit your `.env` file or expose API keys
- Use environment variables in Vercel for production
- The API accepts optional API keys in request body, but it's recommended to set them as environment variables
- For production use, consider implementing authentication and rate limiting

## Development

### Project Components

1. **GitHubClient** (`src/documentation_generator/github_client.py`)
   - Fetches repository metadata
   - Builds file tree structure
   - Extracts important files (README, dependencies, etc.)

2. **CodebaseProcessor** (`src/documentation_generator/processor.py`)
   - Formats file tree for readability
   - Extracts dependencies from multiple package managers
   - Builds comprehensive context summaries
   - Calculates codebase statistics

3. **ClaudeClient** (`src/documentation_generator/claude_client.py`)
   - Interfaces with Anthropic Claude API
   - Formats prompts for code analysis
   - Supports both regular and streaming responses

4. **Serverless Function** (`api/analyze.py`)
   - Vercel serverless endpoint handler
   - Input validation
   - Orchestrates the analysis pipeline
   - Returns formatted responses

### Adding New Features

To add support for new dependency managers, edit `src/documentation_generator/processor.py` and add extraction methods in the `extract_dependencies()` function.

## Troubleshooting

### Common Issues

1. **"ANTHROPIC_API_KEY is not configured"**
   - Make sure you've set the environment variable in Vercel or your `.env` file

2. **"Failed to fetch repository"**
   - Check if the GitHub URL is valid
   - For private repos, ensure you've set a valid `GITHUB_TOKEN`

3. **Rate limit errors**
   - Add a GitHub token to increase rate limits
   - Wait before making additional requests

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License