# Development Plan: GitHub Repository Analyzer

## Overview
A Python serverless application that analyzes GitHub repositories using Claude API and generates comprehensive codebase summaries.

## Input/Output
- **Input**: GitHub repository URL + analysis prompt
- **Output**: Comprehensive text summary of the codebase

## Architecture
- **Platform**: Vercel serverless functions
- **Language**: Python
- **API**: Claude API (Anthropic)

## Development Steps

### 1. Project Setup
- [x] Create `requirements.txt` with dependencies:
  - `anthropic` (Claude API client)
  - `pygithub` or `requests` (GitHub API access)
  - `python-dotenv` (environment variables)
- [x] Set up Vercel configuration (`vercel.json`)
- [x] Create `.env.example` for API keys

### 2. Core Functionality
- [x] **GitHub Repository Fetcher**
  - Clone or fetch repository contents via GitHub API
  - Extract code files and structure
  - Organize files by type/language

- [x] **Codebase Processor**
  - Read and parse repository files
  - Build file tree structure
  - Extract key information (dependencies, structure, main files)

- [x] **Claude API Integration**
  - Format codebase data for Claude
  - Send analysis prompt with code context
  - Handle API responses and errors

### 3. Serverless Function
- [x] Create `/api/analyze.py` (Vercel serverless function)
  - Accept POST request with `repo_url` and `prompt`
  - Validate inputs
  - Process repository
  - Return analysis summary

### 4. API Endpoint Structure
```
POST /api/analyze
Body: {
  "repo_url": "https://github.com/user/repo",
  "prompt": "Analyze this codebase and provide..."
}
Response: {
  "summary": "..."
}
```

### 5. Error Handling
- [x] Validate GitHub URL format
- [x] Handle private repositories (if needed)
- [x] Handle Claude API rate limits
- [x] Handle large repositories (chunking/streaming)

### 6. Deployment
- [x] Configure Vercel for Python runtime
- [x] Set environment variables (Claude API key, GitHub token if needed)
- [x] Deploy and test endpoint (instructions provided)

#### Deployment Instructions

**Prerequisites:**
- Vercel account (sign up at vercel.com)
- Anthropic API key (get from console.anthropic.com)
- GitHub token (optional, get from github.com/settings/tokens)

**Deploy via Vercel Dashboard:**
1. Go to vercel.com/new and import your Git repository
2. Configure environment variables in project settings:
   - `ANTHROPIC_API_KEY` (required): Your Anthropic API key
   - `GITHUB_TOKEN` (optional): For private repos and higher rate limits
3. Click "Deploy" - Vercel automatically uses Python 3.12 runtime from vercel.json

**Deploy via Vercel CLI:**
```bash
npm i -g vercel
vercel login
vercel env add ANTHROPIC_API_KEY
vercel env add GITHUB_TOKEN  # optional
vercel --prod
```

**Test Deployment:**
```bash
# Test GET (API info)
curl https://your-project.vercel.app/api/analyze

# Test POST (analyze repository)
curl -X POST https://your-project.vercel.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/anthropics/anthropic-sdk-python",
    "prompt": "Provide a brief overview of this repository"
  }'
```

## File Structure
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
├── requirements.txt
├── vercel.json
└── .env.example
```

## Environment Variables
- `ANTHROPIC_API_KEY` - Claude API key
- `GITHUB_TOKEN` (optional) - For private repos or rate limits

## Testing
- [ ] Test with public repositories
- [ ] Test with different repository sizes
- [ ] Test error cases (invalid URLs, API failures)

**Test Cases:**

1. **Valid Public Repository:**
   ```bash
   curl -X POST http://localhost:3000/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"repo_url": "https://github.com/anthropics/anthropic-sdk-python", "prompt": "Summarize this codebase"}'
   ```

2. **Invalid URL:**
   ```bash
   curl -X POST http://localhost:3000/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"repo_url": "https://example.com/invalid", "prompt": "Test"}'
   ```
   Expected: 400 error with "Invalid GitHub repository URL"

3. **Missing Required Field:**
   ```bash
   curl -X POST http://localhost:3000/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"repo_url": "https://github.com/user/repo"}'
   ```
   Expected: 400 error with "Missing required field: prompt"

4. **Large Repository:**
   Test with a repository that has 1000+ files to ensure proper handling

5. **API Info Endpoint:**
   ```bash
   curl http://localhost:3000/api/analyze
   ```
   Expected: JSON response with API information

