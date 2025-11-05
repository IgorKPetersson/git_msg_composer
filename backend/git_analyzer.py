"""
Git Analysis Module
WHY? We need to extract what changed in the code (diff) to send to AI
"""
import subprocess
import os
from typing import Dict, List

class GitAnalyzer:
    """Analyzes git repository changes"""

    def get_staged_changes(self, repo_path: str = ".") -> Dict:
        """
        Get staged changes (files added with 'git add')

        WHY staged changes? These are the changes the user wants to commit
        """
        original_dir = os.getcwd()
        try:
            os.chdir(repo_path)

            # Check if it's a git repository
            if not self._is_git_repo():
                raise Exception("Not a git repository")

            # Get the diff of staged changes
            # WHY --cached? Shows only staged changes (git add)
            # WHY --unified=3? Shows 3 lines of context around changes
            diff_result = subprocess.run(
                ["git", "diff", "--cached", "--unified=3"],
                capture_output=True,
                text=True,
                check=True
            )

            diff_text = diff_result.stdout

            # Get statistics (how many lines added/removed)
            stats_result = subprocess.run(
                ["git", "diff", "--cached", "--numstat"],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse statistics
            stats = self._parse_stats(stats_result.stdout)

            # Get list of changed files
            files_result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )

            files = [f for f in files_result.stdout.split("\n") if f.strip()]

            return {
                "has_changes": bool(diff_text.strip()),
                "diff": diff_text,
                "files": files,
                "insertions": stats["insertions"],
                "deletions": stats["deletions"]
            }

        finally:
            os.chdir(original_dir)

    def get_unstaged_changes(self, repo_path: str = ".") -> Dict:
        """
        Get unstaged changes (modified but not added)

        WHY? User might want to see what they haven't staged yet
        """
        original_dir = os.getcwd()
        try:
            os.chdir(repo_path)

            diff_result = subprocess.run(
                ["git", "diff", "--unified=3"],
                capture_output=True,
                text=True,
                check=True
            )

            return {
                "has_changes": bool(diff_result.stdout.strip()),
                "diff": diff_result.stdout
            }

        finally:
            os.chdir(original_dir)

    def _is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def _parse_stats(self, stats_text: str) -> Dict:
        """
        Parse git diff statistics

        Example input: "5\t3\tfilename.py"
        Means: 5 insertions, 3 deletions
        """
        total_insertions = 0
        total_deletions = 0

        for line in stats_text.strip().split("\n"):
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                try:
                    insertions = int(parts[0]) if parts[0] != "-" else 0
                    deletions = int(parts[1]) if parts[1] != "-" else 0
                    total_insertions += insertions
                    total_deletions += deletions
                except ValueError:
                    continue

        return {
            "insertions": total_insertions,
            "deletions": total_deletions
        }

    def get_recent_commits(self, count: int = 5) -> List[Dict]:
        """
        Get recent commit messages for reference

        WHY? AI can learn from your commit style
        """
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--pretty=format:%h|%s|%an|%ar"],
                capture_output=True,
                text=True,
                check=True
            )

            commits = []
            for line in result.stdout.split("\n"):
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) == 4:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1],
                        "author": parts[2],
                        "date": parts[3]
                    })

            return commits

        except subprocess.CalledProcessError:
            return []
