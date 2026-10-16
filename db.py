import sqlite3
from datetime import datetime
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "typecheck.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inspection_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    passed_count INTEGER,
                    failed_count INTEGER,
                    review_count INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inspection_findings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    rule_id TEXT,
                    category TEXT,
                    status TEXT,
                    evidence TEXT,
                    FOREIGN KEY(run_id) REFERENCES inspection_runs(id)
                )
            """)
            conn.commit()

    def save_run(self, filename: str, findings: List[Dict[str, Any]]) -> int:
        passed = sum(1 for f in findings if f["status"] == "Passed")
        failed = sum(1 for f in findings if f["status"] == "Failed")
        review = sum(1 for f in findings if f["status"] == "Review Required")
        timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inspection_runs (filename, timestamp, passed_count, failed_count, review_count)
                VALUES (?, ?, ?, ?, ?)
            """, (filename, timestamp, passed, failed, review))
            run_id = cursor.lastrowid

            for f in findings:
                cursor.execute("""
                    INSERT INTO inspection_findings (run_id, rule_id, category, status, evidence)
                    VALUES (?, ?, ?, ?, ?)
                """, (run_id, f["rule_id"], f["category"], f["status"], f["evidence"]))

            conn.commit()
            return run_id