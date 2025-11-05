#!/bin/bash

# Git Commit Message Composer - CLI Version
# Uses Google Gemini API to generate standardized commit messages

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Load API key from .env file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/backend/.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | grep 'GEMINI_API_KEY' | xargs)
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${RED}Error: GEMINI_API_KEY not found in backend/.env${NC}"
    exit 1
fi

# Function to get staged changes
get_staged_changes() {
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}Error: Not a git repository${NC}"
        exit 1
    fi

    # Check if there are staged changes
    if ! git diff --cached --quiet; then
        DIFF=$(git diff --cached --unified=3 | head -c 3000)
        FILES=$(git diff --cached --name-only)

        # Get statistics
        STATS=$(git diff --cached --numstat)
        INSERTIONS=$(echo "$STATS" | awk '{sum+=$1} END {print sum+0}')
        DELETIONS=$(echo "$STATS" | awk '{sum+=$2} END {print sum+0}')

        echo "$DIFF|$FILES|$INSERTIONS|$DELETIONS"
    else
        echo -e "${YELLOW}No staged changes found. Use 'git add' to stage files.${NC}"
        exit 0
    fi
}

# Function to call Gemini API
generate_commit_message() {
    local diff="$1"
    local files="$2"

    # Create the prompt
    local prompt="You are an expert at writing clear, concise git commit messages following conventional commits format.

Analyze this git diff and generate a commit message.

**Files changed:**
$files

**Diff:**
$diff

**Instructions:**
1. Choose the appropriate type: feat, fix, docs, style, refactor, test, chore, perf
2. Write a short, clear subject line (50 chars max)
3. Add a body explaining WHAT changed and WHY (if significant changes)
4. Use present tense (\"add\" not \"added\")

**Format your response EXACTLY like this:**
TYPE: [type]
SUBJECT: [subject line]
BODY: [optional body, can be empty]"

    # Escape the prompt for JSON
    local escaped_prompt=$(echo "$prompt" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

    # Create JSON payload
    local json_payload="{\"contents\":[{\"parts\":[{\"text\":$escaped_prompt}]}]}"

    # Call Gemini API
    local response=$(curl -s -X POST \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d "$json_payload")

    # Extract the text from response
    local text=$(echo "$response" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    print(text)
except Exception as e:
    print("ERROR: " + str(e), file=sys.stderr)
    sys.exit(1)
')

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to parse Gemini API response${NC}"
        exit 1
    fi

    echo "$text"
}

# Function to parse the AI response
parse_response() {
    local response="$1"

    local type=$(echo "$response" | grep "^TYPE:" | sed 's/TYPE: *//' | tr -d '\r')
    local subject=$(echo "$response" | grep "^SUBJECT:" | sed 's/SUBJECT: *//' | tr -d '\r')
    local body=$(echo "$response" | sed -n '/^BODY:/,$p' | sed '1s/BODY: *//' | sed 's/^$//' | tr -d '\r')

    # Validate type
    if [[ ! "$type" =~ ^(feat|fix|docs|style|refactor|test|chore|perf)$ ]]; then
        type="chore"
    fi

    # Construct the message
    if [ -z "$body" ] || [ "$body" == "N/A" ] || [ "$body" == "None" ]; then
        echo "$type: $subject"
    else
        echo -e "$type: $subject\n\n$body"
    fi
}

# Function to display commit message with colors
display_message() {
    local message="$1"
    local type="$2"
    local files="$3"
    local insertions="$4"
    local deletions="$5"

    # Choose color based on type
    local type_color=$CYAN
    case "$type" in
        feat) type_color=$GREEN ;;
        fix) type_color=$RED ;;
        docs) type_color=$BLUE ;;
        refactor) type_color=$YELLOW ;;
    esac

    echo -e "\n${BOLD}=== Generated Commit Message ===${NC}\n"
    echo -e "${type_color}${message}${NC}"
    echo -e "\n${BOLD}=== Statistics ===${NC}"
    echo -e "${GREEN}+${insertions}${NC} ${RED}-${deletions}${NC}"
    echo -e "\n${BOLD}=== Files Changed ===${NC}"
    echo "$files"
}

# Main execution
main() {
    echo -e "${BOLD}${CYAN}Git Commit Message Composer${NC}\n"

    # Get staged changes
    echo -e "${YELLOW}Analyzing staged changes...${NC}"
    IFS='|' read -r diff files insertions deletions <<< "$(get_staged_changes)"

    # Generate commit message
    echo -e "${YELLOW}Generating commit message with AI...${NC}"
    ai_response=$(generate_commit_message "$diff" "$files")

    # Parse response
    commit_message=$(parse_response "$ai_response")
    commit_type=$(echo "$ai_response" | grep "^TYPE:" | sed 's/TYPE: *//' | tr -d '\r')

    # Display the message
    display_message "$commit_message" "$commit_type" "$files" "$insertions" "$deletions"

    # Ask user if they want to commit
    echo -e "\n${BOLD}Would you like to create this commit?${NC}"
    echo -e "${YELLOW}[y] Yes  [n] No  [e] Edit message${NC}"
    read -p "> " choice

    case "$choice" in
        y|Y|yes|Yes|YES)
            git commit -m "$commit_message"
            echo -e "${GREEN}✓ Commit created successfully!${NC}"
            ;;
        e|E|edit|Edit|EDIT)
            # Create temporary file with message
            temp_file=$(mktemp)
            echo "$commit_message" > "$temp_file"
            ${EDITOR:-nano} "$temp_file"
            edited_message=$(cat "$temp_file")
            rm "$temp_file"

            git commit -m "$edited_message"
            echo -e "${GREEN}✓ Commit created with edited message!${NC}"
            ;;
        *)
            echo -e "${YELLOW}Commit message saved to clipboard (if available)${NC}"
            # Try to copy to clipboard (works on different systems)
            if command -v clip.exe &> /dev/null; then
                echo "$commit_message" | clip.exe
            elif command -v xclip &> /dev/null; then
                echo "$commit_message" | xclip -selection clipboard
            elif command -v pbcopy &> /dev/null; then
                echo "$commit_message" | pbcopy
            fi
            ;;
    esac
}

# Run main function
main
