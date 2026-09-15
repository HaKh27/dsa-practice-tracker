import sqlite3

def get_connection():
    return sqlite3.connect("tracker.db")

def get_unreviewed(conn):
    cursor= conn.execute("""
        SELECT problems.name, problems.difficulty
        FROM problems
        LEFT JOIN sessions ON problems.name= sessions.problem_name
        WHERE sessions.problem_name IS NULL
    """)
    return cursor.fetchall()

def create_table(conn):
    conn.execute("""
        CREATE TABLE problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            topic TEXT,
            difficulty TEXT,
            last_reviewed TEXT
        )
    """)
    conn.commit()

if __name__=="__main__":
    conn= get_connection()
    create_table(conn)
    print("Table created.")