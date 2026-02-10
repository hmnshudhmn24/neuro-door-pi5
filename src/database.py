"""Database Operations"""
import sqlite3
import logging
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class Database:
    """Handles database operations"""
    
    def __init__(self, db_path='data/neurodoor.db'):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        logger.info(f"Database initialized: {db_path}")
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                face_encoding BLOB,
                pin_hash TEXT,
                active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_access DATETIME
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN,
                method TEXT,
                confidence REAL,
                photo_path TEXT,
                risk_score REAL,
                anomaly_detected BOOLEAN DEFAULT 0,
                reason TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        self.conn.commit()
    
    def get_user(self, user_id):
        """Get user by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ? AND active = 1", (user_id,))
        result = cursor.fetchone()
        return dict(result) if result else None
    
    def get_user_count(self):
        """Get total user count"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE active = 1")
        return cursor.fetchone()['count']
    
    def log_access(self, log_entry):
        """Log access attempt"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO access_log 
            (user_id, timestamp, success, method, confidence, risk_score, anomaly_detected, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            log_entry.get('user_id'),
            log_entry.get('timestamp', datetime.now()),
            log_entry.get('success'),
            log_entry.get('method'),
            log_entry.get('confidence'),
            log_entry.get('risk_score'),
            log_entry.get('anomaly_detected', False),
            log_entry.get('reason', '')
        ))
        self.conn.commit()
    
    def get_recent_access(self, limit=10):
        """Get recent access log"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.*, u.name as user_name 
            FROM access_log a 
            LEFT JOIN users u ON a.user_id = u.id 
            ORDER BY a.timestamp DESC LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_user_access_history(self, user_id, days=30):
        """Get user access history"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM access_log 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 100
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_access_log(self, start_date=None, end_date=None, limit=100):
        """Get access log with filters"""
        cursor = self.conn.cursor()
        query = """
            SELECT a.*, u.name as user_name 
            FROM access_log a 
            LEFT JOIN users u ON a.user_id = u.id 
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND a.timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND a.timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY a.timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database closed")
