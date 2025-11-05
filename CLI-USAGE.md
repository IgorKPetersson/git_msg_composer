# Git Message Composer - CLI Usage

Use these scripts to generate AI-powered commit messages directly from your terminal without opening the web browser.

## Quick Start

### Option 1: Bash Script (Git Bash / Linux / macOS)

```bash
# Make changes and stage them
git add .

# Generate commit message
./git-msg.sh
```

### Option 2: Windows Batch Script

```cmd
# Make changes and stage them
git add .

# Generate commit message
git-msg.bat
```

## What It Does

1. **Analyzes** your staged git changes
2. **Calls** Google Gemini API to generate a standardized commit message
3. **Shows** the generated message with statistics
4. **Prompts** you to:
   - `[y]` Create the commit immediately
   - `[n]` Cancel (message copied to clipboard)
   - `[e]` Edit the message before committing

## Requirements

- Python 3.x (for API calls)
- Git installed
- Internet connection (to call Gemini API)
- Valid `GEMINI_API_KEY` in `backend/.env`

## Example Output

```
================================
Git Commit Message Composer
================================

Analyzing staged changes...
Generating commit message with AI...

=== Generated Commit Message ===

feat: add CLI script for commit message generation

Implement bash and batch scripts to generate commit messages
without requiring the web browser. Scripts call Gemini API
directly and provide interactive commit workflow.

=== Statistics ===
+245 -12

=== Files Changed ===
git-msg.sh
git-msg.bat

Create this commit? [y/n/e]:
```

## Commit Message Format

Messages follow the **Conventional Commits** standard:

```
<type>: <subject>

<body>
```

**Supported types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting (no code change)
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance
- `perf:` Performance improvement

## Troubleshooting

**"GEMINI_API_KEY not found"**
- Check that `backend/.env` file exists
- Verify the API key is set: `GEMINI_API_KEY=your_key_here`

**"Not a git repository"**
- Run the script from inside a git repository
- Initialize with `git init` if needed

**"No staged changes found"**
- Stage your changes first: `git add <files>`
- Or stage all: `git add .`

## Advanced Usage

### Create an alias for quick access

**Git Bash / Linux / macOS:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias gcm='./git-msg.sh'

# Then just use:
gcm
```

**Windows (Git Bash):**
```bash
# Add to ~/.bashrc
alias gcm='bash /c/Python/Hackaton/git_msg_composer/git-msg.sh'
```

**Windows (CMD):**
```cmd
# Create doskey macro
doskey gcm=C:\Python\Hackaton\git_msg_composer\git-msg.bat
```

### Use in any repository

Make the script globally accessible:

```bash
# Copy to a directory in your PATH
sudo cp git-msg.sh /usr/local/bin/git-msg
sudo chmod +x /usr/local/bin/git-msg

# Now use from any git repository
git-msg
```

## Comparison with Web UI

| Feature | CLI Script | Web Browser |
|---------|-----------|-------------|
| Generate message | ✅ | ✅ |
| Commit directly | ✅ | ❌ |
| Edit before commit | ✅ | ❌ |
| View history | ❌ | ✅ |
| Statistics display | ✅ | ✅ |
| Offline mode | ❌ | ❌ |
| Speed | ⚡ Fast | Slower (server startup) |

## Tips

1. **Stage intentionally** - Only stage related changes for better commit messages
2. **Review before committing** - Always review the AI-generated message
3. **Edit if needed** - Use the `[e]` option to customize the message
4. **Keep API key secure** - Never commit your `.env` file to version control

## Support

For issues or questions about the CLI scripts, check:
- The main project README
- Backend logs for API errors
- Git status to verify staged changes
