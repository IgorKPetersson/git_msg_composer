# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

✅ Python 3.8+
✅ Node.js 18+
✅ Git
✅ Google Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))

## Setup (One Time)

### 1. Get API Key
Visit https://makersuite.google.com/app/apikey and copy your key

### 2. Configure Backend
```bash
cd backend
cp .env.example .env
# Edit .env and paste your API key
```

### 3. Install Dependencies

**Windows:**
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend (new terminal)
cd frontend
npm install
```

**Mac/Linux:**
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend (new terminal)
cd frontend
npm install
```

## Running the App

### Option 1: Use Startup Scripts (Easiest)

**Windows:**
- Double-click `start_backend.bat`
- Double-click `start_frontend.bat` (in a new terminal)

**Mac/Linux:**
```bash
chmod +x start_backend.sh start_frontend.sh
./start_backend.sh  # Terminal 1
./start_frontend.sh # Terminal 2
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Using the App

1. Open http://localhost:3000
2. Make code changes in your project
3. Run `git add .`
4. Click "Generate Commit Message"
5. Copy and use: `git commit -m "..."`

## Quick Test

```bash
# Create a test change
echo "test" > test.txt
git add test.txt

# Go to http://localhost:3000
# Click "Generate Commit Message"
# See the AI-generated message!
```

## Troubleshooting

**Backend won't start?**
- Check .env file exists with valid API key
- Make sure port 8000 is free

**Frontend won't start?**
- Delete node_modules and run `npm install` again
- Check port 3000 is free

**"No staged changes" error?**
- Run `git add .` first
- Make sure you're in a git repository

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the code structure
- Try different types of changes to see different commit messages

---

**Happy coding! 🚀**
