"""
Google Gemini Flash Integration
WHY Gemini? It's fast, free tier available, and good at code analysis
"""
import os
from typing import Dict
import google.generativeai as genai

class GeminiService:
    """Service for interacting with Google Gemini AI"""

    def __init__(self):
        """
        Initialize Gemini API

        WHY environment variable? Keep API key secret, don't hardcode it
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. "
                "Get your key from: https://makersuite.google.com/app/apikey"
            )

        genai.configure(api_key=api_key)

        # WHY gemini-1.5-flash? It's fast and cost-effective for this task
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Commit message conventions (standardized format)
        self.commit_types = {
            "feat": "New feature",
            "fix": "Bug fix",
            "docs": "Documentation changes",
            "style": "Code style changes (formatting, semicolons, etc.)",
            "refactor": "Code refactoring (no feature change)",
            "test": "Adding or updating tests",
            "chore": "Maintenance tasks (dependencies, config, etc.)",
            "perf": "Performance improvements"
        }

    async def generate_commit_message(self, diff: str, files: list[str]) -> Dict:
        """
        Generate commit message from git diff

        WHY async? Doesn't block other operations while waiting for AI
        """

        # Create prompt for Gemini
        # WHY detailed prompt? Better prompts = better AI responses
        prompt = self._create_prompt(diff, files)

        try:
            # Call Gemini API
            response = self.model.generate_content(prompt)

            # Parse response
            message_data = self._parse_response(response.text)

            return message_data

        except Exception as e:
            # Fallback if AI fails
            return {
                "type": "chore",
                "message": f"chore: update {len(files)} file(s)\n\nFiles: {', '.join(files)}"
            }

    def _create_prompt(self, diff: str, files: list[str]) -> str:
        """
        Create prompt for Gemini

        WHY structured prompt? Tells AI exactly what format we want
        """
        return f"""You are an expert at writing clear, concise git commit messages following conventional commits format.

Analyze this git diff and generate a commit message.

**Files changed:**
{chr(10).join(f'- {f}' for f in files)}

**Diff:**
```
{diff[:3000]}
```

**Instructions:**
1. Choose the appropriate type: {', '.join(self.commit_types.keys())}
2. Write a short, clear subject line (50 chars max)
3. Add a body explaining WHAT changed and WHY (if significant changes)
4. Use present tense ("add" not "added")

**Format your response EXACTLY like this:**
TYPE: [type]
SUBJECT: [subject line]
BODY: [optional body, can be empty]

Example:
TYPE: feat
SUBJECT: add user authentication system
BODY: Implement JWT-based authentication with login and registration endpoints. This provides secure user access control for the application.
"""

    def _parse_response(self, response_text: str) -> Dict:
        """
        Parse Gemini's response into structured data

        WHY parsing? Convert AI text into usable format for our app
        """
        lines = response_text.strip().split("\n")

        commit_type = "chore"
        subject = ""
        body = ""

        # Extract each part
        for line in lines:
            if line.startswith("TYPE:"):
                commit_type = line.replace("TYPE:", "").strip().lower()
            elif line.startswith("SUBJECT:"):
                subject = line.replace("SUBJECT:", "").strip()
            elif line.startswith("BODY:"):
                body = line.replace("BODY:", "").strip()

        # Validate type
        if commit_type not in self.commit_types:
            commit_type = "chore"

        # Construct final message
        if body:
            full_message = f"{commit_type}: {subject}\n\n{body}"
        else:
            full_message = f"{commit_type}: {subject}"

        return {
            "type": commit_type,
            "subject": subject,
            "message": full_message,
            "body": body
        }

    def regenerate_with_style(self, diff: str, files: list[str], style: str = "concise") -> Dict:
        """
        Generate commit message with specific style

        WHY? Give users options: concise, detailed, emoji, etc.
        """
        styles = {
            "concise": "Be very brief and to the point",
            "detailed": "Provide detailed explanation of changes",
            "emoji": "Use relevant emojis in the message",
        }

        style_instruction = styles.get(style, styles["concise"])

        # Modify prompt with style
        prompt = self._create_prompt(diff, files)
        prompt += f"\n\nSTYLE: {style_instruction}"

        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)
