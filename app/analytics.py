import sqlite3
import pandas as pd

DB_NAME = "students.db"

def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    return df