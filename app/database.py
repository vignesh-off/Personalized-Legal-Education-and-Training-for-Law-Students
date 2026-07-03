import sqlite3

DB_NAME = "students.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        topic TEXT,
        score REAL,
        time_spent REAL,
        attempts INTEGER,
        difficulty_level INTEGER,
        mastery_level TEXT,
        risk_level TEXT,
        next_topic TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_prediction(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions (
        student_id, topic, score, time_spent, attempts,
        difficulty_level, mastery_level, risk_level, next_topic
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["student_id"],
        data["topic"],
        data["score"],
        data["time_spent"],
        data["attempts"],
        data["difficulty_level"],
        data["mastery_level"],
        data["risk_level"],
        data["next_topic_recommendation"]
    ))

    conn.commit()
    conn.close()