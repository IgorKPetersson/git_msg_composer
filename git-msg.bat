@echo off
REM Git Commit Message Composer - Windows Batch Version
REM Uses Google Gemini API to generate standardized commit messages

setlocal enabledelayedexpansion

REM Load API key from .env file
set "ENV_FILE=%~dp0backend\.env"
if not exist "%ENV_FILE%" (
    echo Error: backend/.env file not found
    exit /b 1
)

REM Read API key from .env
for /f "tokens=1,2 delims==" %%a in ('type "%ENV_FILE%" ^| findstr "GEMINI_API_KEY"') do (
    set "GEMINI_API_KEY=%%b"
)

if "%GEMINI_API_KEY%"=="" (
    echo Error: GEMINI_API_KEY not found in backend/.env
    exit /b 1
)

REM Check if in git repository
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo Error: Not a git repository
    exit /b 1
)

REM Check for staged changes
git diff --cached --quiet
if %errorlevel% equ 0 (
    echo No staged changes found. Use 'git add' to stage files.
    exit /b 0
)

echo.
echo ================================
echo Git Commit Message Composer
echo ================================
echo.

echo Analyzing staged changes...

REM Get diff and files
git diff --cached --unified=3 > temp_diff.txt
git diff --cached --name-only > temp_files.txt
git diff --cached --numstat > temp_stats.txt

REM Get statistics
set /a insertions=0
set /a deletions=0
for /f "tokens=1,2" %%a in (temp_stats.txt) do (
    if "%%a" neq "-" (
        set /a insertions+=%%a
        set /a deletions+=%%b
    )
)

echo Generating commit message with AI...

REM Create prompt for Python script
set "TEMP_PROMPT=%TEMP%\gemini_prompt.txt"
set "TEMP_RESPONSE=%TEMP%\gemini_response.txt"

(
echo You are an expert at writing clear, concise git commit messages following conventional commits format.
echo.
echo Analyze this git diff and generate a commit message.
echo.
echo **Files changed:**
type temp_files.txt
echo.
echo **Diff:**
type temp_diff.txt
echo.
echo **Instructions:**
echo 1. Choose the appropriate type: feat, fix, docs, style, refactor, test, chore, perf
echo 2. Write a short, clear subject line ^(50 chars max^)
echo 3. Add a body explaining WHAT changed and WHY ^(if significant changes^)
echo 4. Use present tense ^("add" not "added"^)
echo.
echo **Format your response EXACTLY like this:**
echo TYPE: [type]
echo SUBJECT: [subject line]
echo BODY: [optional body, can be empty]
) > "%TEMP_PROMPT%"

REM Call Python script to interact with Gemini API
python "%~dp0gemini_api.py" "%TEMP_PROMPT%" "%TEMP_RESPONSE%" 2>nul

if errorlevel 1 (
    echo Error: Failed to generate commit message
    del /f temp_*.txt "%TEMP_PROMPT%" "%TEMP_RESPONSE%" 2>nul
    exit /b 1
)

REM Parse response
for /f "usebackq delims=" %%a in ("%TEMP_RESPONSE%") do (
    set "line=%%a"
    if "!line:~0,5!"=="TYPE:" (
        set "type=!line:~6!"
    )
    if "!line:~0,8!"=="SUBJECT:" (
        set "subject=!line:~9!"
    )
)
# detta är en test
REM Display the generated message
echo.
echo ================================
echo Generated Commit Message
echo ================================
echo.
type "%TEMP_RESPONSE%"
echo.
echo ================================
echo Statistics
echo ================================
echo +%insertions% -%deletions%
echo.
echo ================================
echo Files Changed
echo ================================
type temp_files.txt
echo.

REM Construct full commit message
set "COMMIT_MSG_FILE=%TEMP%\commit_msg.txt"
(
echo !type!: !subject!
type "%TEMP_RESPONSE%" | findstr /v "^TYPE: ^SUBJECT:"
) > "%COMMIT_MSG_FILE%"

REM Ask user if they want to commit
echo.
set /p "choice=Create this commit? [y/n/e=edit]: "

if /i "%choice%"=="y" (
    git commit -F "%COMMIT_MSG_FILE%"
    echo Commit created successfully!
) else if /i "%choice%"=="e" (
    notepad "%COMMIT_MSG_FILE%"
    git commit -F "%COMMIT_MSG_FILE%"
    echo Commit created with edited message!
) else (
    echo Commit message saved to: %COMMIT_MSG_FILE%
    type "%COMMIT_MSG_FILE%" | clip
    echo Message copied to clipboard!
)

REM Cleanup
del /f temp_*.txt "%TEMP_PROMPT%" "%TEMP_RESPONSE%" 2>nul

endlocal
pause
