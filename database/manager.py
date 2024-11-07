# database/manager.py
import sqlite3
from pathlib import Path
import asyncio
from typing import Dict, List, Any

class DatabaseManager:
    def __init__(self):
        self.db_path = Path("data/system.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.setup_database()
        
    def setup_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            
            # Create tables
            cur.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    preferences TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    value REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
    async def store_metric(self, metric_type: str, value: float):
        """Store system metric"""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO metrics (type, value) VALUES (?, ?)",
                (metric_type, value)
            )
            
    async def get_metrics(self, metric_type: str, limit: int = 100) -> List[Dict]:
        """Retrieve metrics"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM metrics WHERE type = ? ORDER BY timestamp DESC LIMIT ?",
                (metric_type, limit)
            )
            return [dict(row) for row in cur.fetchall()]
