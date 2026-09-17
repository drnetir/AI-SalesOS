import sqlite3
from contextlib import contextmanager
from pathlib import Path
DB_PATH=Path("./aisalesos.db")
def get_connection():
    c=sqlite3.connect(DB_PATH,check_same_thread=False); c.row_factory=sqlite3.Row; return c
def init_db():
    db=get_connection()
    db.executescript('''
    CREATE TABLE IF NOT EXISTS tasks(task_id TEXT PRIMARY KEY,objective TEXT NOT NULL,status TEXT NOT NULL,state_json TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS checkpoints(id INTEGER PRIMARY KEY AUTOINCREMENT,task_id TEXT NOT NULL,checkpoint_json TEXT NOT NULL,created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS memories(memory_id TEXT PRIMARY KEY,scope TEXT NOT NULL,task_id TEXT,key TEXT NOT NULL,value TEXT NOT NULL,importance INTEGER DEFAULT 5,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_memories_task ON memories(task_id);
    '''); db.commit(); db.close()
@contextmanager
def transaction():
    db=get_connection()
    try: yield db; db.commit()
    except: db.rollback(); raise
    finally: db.close()
