#!/usr/bin/env python3
"""Initialize Database"""
from src.database import Database

def init_database():
    print("Initializing NeuroDoor database...")
    db = Database()
    print("Database initialized successfully!")
    
    # Create default admin user (for testing)
    cursor = db.conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users (id, name, role, active)
        VALUES (1, 'Admin', 'admin', 1)
    """)
    db.conn.commit()
    db.close()
    print("Default admin user created")

if __name__ == '__main__':
    init_database()
