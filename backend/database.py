"""
SQLite Database for Commit History
WHY database? Store history of generated commits for reference
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict
import os

class Database:
    """Manages SQLite database for commit history"""

    def __init__(self, db_path: str = "commit_history.db"):
        """
        Initialize database connection

        WHY SQLite? Lightweight, no server needed, perfect for this app
        """
        # Create database directory if needed
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """
        Create database tables if they don't exist

        WHY migration? Sets up schema on first run
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Commits table - stores generated commit messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    commit_type TEXT NOT NULL,
                    files TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    used BOOLEAN DEFAULT FALSE
                )
            """)

            # Settings table - store user preferences
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

            conn.commit()

    def save_commit(self, message: str, commit_type: str, files: List[str]) -> int:
        """
        Save a generated commit message

        WHY? Keep history of what AI generated for future reference
        Returns: commit_id
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Convert files list to JSON string for storage
            # WHY JSON? SQLite doesn't have array type, JSON is standard
            files_json = json.dumps(files)

            cursor.execute("""
                INSERT INTO commits (message, commit_type, files)
                VALUES (?, ?, ?)
            """, (message, commit_type, files_json))

            conn.commit()
            return cursor.lastrowid

    def get_recent_commits(self, limit: int = 10) -> List[Dict]:
        """
        Get recent commit history

        WHY? Show user what was generated before
        """
        with sqlite3.connect(self.db_path) as conn:
            # Enable row factory to get dict results
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, message, commit_type, files, created_at, used
                FROM commits
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()

            # Convert to list of dicts
            commits = []
            for row in rows:
                commits.append({
                    "id": row["id"],
                    "message": row["message"],
                    "commit_type": row["commit_type"],
                    "files": json.loads(row["files"]),  # Parse JSON back to list
                    "created_at": row["created_at"],
                    "used": bool(row["used"])
                })

            return commits

    def mark_as_used(self, commit_id: int):
        """
        Mark a commit as used (actually committed to git)

        WHY? Track which AI suggestions were actually used
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE commits
                SET used = TRUE
                WHERE id = ?
            """, (commit_id,))

            conn.commit()

    def get_stats(self) -> Dict:
        """
        Get usage statistics

        WHY? Show user insights: most common type, total commits, etc.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total commits generated
            cursor.execute("SELECT COUNT(*) as total FROM commits")
            total = cursor.fetchone()[0]

            # Total actually used
            cursor.execute("SELECT COUNT(*) as used FROM commits WHERE used = TRUE")
            used = cursor.fetchone()[0]

            # Most common type
            cursor.execute("""
                SELECT commit_type, COUNT(*) as count
                FROM commits
                GROUP BY commit_type
                ORDER BY count DESC
                LIMIT 1
            """)
            most_common_row = cursor.fetchone()
            most_common = most_common_row[0] if most_common_row else "N/A"

            return {
                "total_generated": total,
                "total_used": used,
                "most_common_type": most_common
            }

    def clear_history(self):
        """
        Clear all commit history

        WHY? User might want fresh start
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM commits")
            conn.commit()
