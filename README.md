# 🚀 Git Commit Message Composer

An AI-powered tool that analyzes your code changes and generates standardized, meaningful git commit messages using Google Gemini Flash.

## 📋 About

This project helps developers write better commit messages by:
- Analyzing staged git changes automatically
- Generating conventional commit messages (feat, fix, docs, etc.)
- Learning from your commit history
- Providing a clean, modern UI for easy interaction

**Tech Stack:**
- **Backend:** Python 3.x + FastAPI
- **Frontend:** React + TypeScript + Tailwind CSS
- **Database:** SQLite
- **AI:** Google Gemini Flash

## 🎯 Features

✅ Analyze staged git changes
✅ AI-powered commit message generation
✅ Conventional Commits format support
✅ Commit history tracking
✅ Beautiful, responsive UI
✅ Copy-to-clipboard functionality
✅ Statistics and insights

## 📦 Project Structure

```
git_msg_composer/
├── backend/                  # Python FastAPI backend
│   ├── main.py              # Main API server
│   ├── git_analyzer.py      # Git diff analysis
│   ├── gemini_service.py    # Google Gemini integration
│   ├── database.py          # SQLite database management
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main app component
│   │   ├── main.tsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node dependencies
│   ├── vite.config.ts       # Vite configuration
│   └── tailwind.config.js   # Tailwind CSS config
└── README.md                # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- Git installed
- Google Gemini API key (free tier available)

### Step 1: Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (keep it secret!)

**WHY?** The AI needs this key to analyze your code and generate commit messages.

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (WHY? Isolates Python dependencies)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file and add your Gemini API key
# Replace 'your_api_key_here' with your actual key
```

**Your .env file should look like:**
```
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_PATH=commit_history.db
HOST=0.0.0.0
PORT=8000
```

### Step 3: Frontend Setup

```bash
# Open a new terminal
# Navigate to frontend directory
cd frontend

# Install dependencies (WHY? Downloads React, TypeScript, etc.)
npm install

# Or if you use yarn:
yarn install
```

## 🚀 Running the Application

You need to run both backend and frontend simultaneously.

### Terminal 1: Start Backend

```bash
cd backend

# Activate virtual environment first
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Run the server
python main.py

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**WHY separate terminal?** Backend runs continuously, so you need another terminal for frontend.

### Terminal 2: Start Frontend

```bash
cd frontend

# Start development server
npm run dev

# You should see:
# VITE v5.0.12  ready in 500 ms
# ➜  Local:   http://localhost:3000/
```

### Access the Application

Open your browser and go to: **http://localhost:3000**

## 📖 How to Use

### Basic Workflow

1. **Make changes to your code**
   ```bash
   # Example: Edit some files
   echo "console.log('hello')" >> app.js
   ```

2. **Stage your changes**
   ```bash
   git add .
   # Or stage specific files:
   git add app.js
   ```

3. **Open the web app** at http://localhost:3000

4. **Click "Generate Commit Message"**
   - The AI analyzes your changes
   - Generates a standardized commit message
   - Shows files changed and statistics

5. **Copy the message** and commit
   ```bash
   git commit -m "feat: add hello world logging

   Implement console logging functionality to display hello message. This provides basic debugging output for the application."
   ```

### Understanding Commit Types

The AI follows the **Conventional Commits** standard:

- **feat:** New feature for the user
  ```
  feat: add user authentication system
  ```

- **fix:** Bug fix
  ```
  fix: resolve login timeout issue
  ```

- **docs:** Documentation changes
  ```
  docs: update API documentation
  ```

- **style:** Code style changes (formatting, semicolons, etc.)
  ```
  style: format code with prettier
  ```

- **refactor:** Code refactoring without changing functionality
  ```
  refactor: extract validation logic into separate module
  ```

- **test:** Adding or updating tests
  ```
  test: add unit tests for user service
  ```

- **chore:** Maintenance tasks (dependencies, configs, etc.)
  ```
  chore: update dependencies to latest versions
  ```

- **perf:** Performance improvements
  ```
  perf: optimize database queries
  ```

**WHY these types?** They make commit history easier to understand and automate changelog generation.

## 🎓 Learning Points (For Students)

### Backend Architecture

**FastAPI (main.py)**
- Modern Python web framework
- Automatic API documentation
- Fast and async-capable
- Type checking with Pydantic

**Git Analysis (git_analyzer.py)**
- Uses subprocess to run git commands
- Extracts diff, stats, and file information
- Parses git output into structured data

**AI Integration (gemini_service.py)**
- Connects to Google Gemini API
- Crafts effective prompts for AI
- Parses AI responses into structured format

**Database (database.py)**
- SQLite for lightweight data storage
- Stores commit history
- Tracks usage statistics

### Frontend Architecture

**React + TypeScript**
- Component-based UI
- Type safety prevents bugs
- Hooks for state management (useState, useEffect)

**Tailwind CSS**
- Utility-first CSS framework
- Rapid UI development
- Responsive design built-in

**API Communication**
- Axios for HTTP requests
- Async/await pattern
- Error handling

## 🐛 Troubleshooting

### Backend Issues

**Error: "GEMINI_API_KEY environment variable not set"**
- Make sure you created the `.env` file in the `backend/` directory
- Check that your API key is correct
- Restart the backend server

**Error: "Not a git repository"**
- Run the app from within a git repository
- Initialize git: `git init`

**Error: "No staged changes found"**
- Make sure you've staged files with `git add`
- Check status: `git status`

### Frontend Issues

**Error: "Cannot connect to backend"**
- Make sure backend is running on port 8000
- Check backend terminal for errors
- Verify CORS settings in main.py

**Error: Module not found**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## 🔧 Development Tips

### Backend Development

**Test API endpoints:**
```bash
# FastAPI auto-generates API docs
# Visit: http://localhost:8000/docs
```

**Load environment variables:**
```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file
```

### Frontend Development

**Hot reload:**
- Vite automatically reloads when you save files
- No need to restart the dev server

**Debugging:**
```typescript
console.log('Debug:', someVariable)
// Opens Chrome DevTools with F12
```

## 📊 API Endpoints

### `POST /analyze`
Analyze staged changes and generate commit message.

**Request:**
```json
{
  "repo_path": null  // null = current directory
}
```

**Response:**
```json
{
  "message": "feat: add user authentication\n\nImplement JWT-based auth...",
  "type": "feat",
  "files_changed": ["auth.py", "models.py"],
  "insertions": 45,
  "deletions": 12
}
```

### `GET /history?limit=10`
Get recent commit history.

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "message": "feat: add authentication",
      "commit_type": "feat",
      "files": ["auth.py"],
      "created_at": "2024-01-15T10:30:00",
      "used": true
    }
  ]
}
```

## 🚀 Future Enhancements

- [ ] Multiple AI models support (GPT-4, Claude, etc.)
- [ ] Commit message templates
- [ ] Direct git commit from UI
- [ ] Team collaboration features
- [ ] Commit message style learning
- [ ] GitHub/GitLab integration

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is a school project, but contributions and suggestions are welcome!

## 📧 Support

Having issues? Create an issue in the repository or check the troubleshooting section.

---

**Built with ❤️ for AI/ML students learning full-stack development**
