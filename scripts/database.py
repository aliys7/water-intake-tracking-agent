import sqlite3
import os
from datetime import datetime

os.makedirs('data', exist_ok=True)
DB_PATH = 'data/water_tracker.db'

def init_db():
    """Initialize the database with proper schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS water_intake (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        intake_ml INTEGER NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def log_intake(user_id, intake_ml):
    """Log water intake for a user"""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)  
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (user_id,))
        
        cursor.execute('''
        INSERT INTO water_intake (user_id, intake_ml)
        VALUES (?, ?)
        ''', (user_id, intake_ml))
        
        conn.commit()
    finally:
        conn.close()

def get_intake_history(user_id):
    """Get complete intake history for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT 
        id, 
        user_id, 
        intake_ml, 
        timestamp,
        (SELECT SUM(intake_ml) 
         FROM water_intake w2 
         WHERE w2.user_id = w1.user_id AND w2.timestamp <= w1.timestamp) as total_ml
    FROM water_intake w1
    WHERE user_id = ?
    ORDER BY timestamp
    ''', (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{
        'id': row[0],
        'user_id': row[1],
        'intake_ml': row[2],
        'timestamp': row[3],
        'total_ml': row[4]
    } for row in rows]