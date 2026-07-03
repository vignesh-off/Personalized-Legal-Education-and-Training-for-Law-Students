import sqlite3
import os
import sys

# Add current dir to path to import determine_risk_level
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.main import determine_risk_level

DB_PATH = "students.db"

def recalculate_db_risk():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all records
    cursor.execute("SELECT id, score, attempts, difficulty_level, time_spent, risk_level FROM predictions")
    rows = cursor.fetchall()
    
    updated_count = 0
    for row in rows:
        id_val, score, attempts, difficulty_level, time_spent, old_risk = row
        new_risk = determine_risk_level(score, attempts, difficulty_level, time_spent)
        
        if old_risk != new_risk:
            cursor.execute("UPDATE predictions SET risk_level = ? WHERE id = ?", (new_risk, id_val))
            updated_count += 1
            print(f"Updated record ID {id_val}: {old_risk} -> {new_risk}")

    conn.commit()
    conn.close()
    
    print(f"Recalculation complete. Updated {updated_count} out of {len(rows)} records.")

if __name__ == "__main__":
    recalculate_db_risk()
