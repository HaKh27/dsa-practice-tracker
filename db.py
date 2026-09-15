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

def insert_problems(conn,name,topic,difficulty,last_reviewed):
    conn.execute("""
        INSERT INTO problems(name,topic, difficulty,last_reviewed)
        VALUES(?,?,?,?)
    """, (name, topic, difficulty,last_reviewed))
    conn.commit()    

def get_all_problems(conn):
    cursor= conn.execute("SELECT * FROM problems")
    return cursor.fetchall()

def get_by_topic(conn, topic):
    cursor= conn.execute("""
    SELECT * 
    FROM problems
    WHERE topic = ?
    """, (topic,)) 
    return cursor.fetchall()

if __name__=="__main__":
    conn= get_connection()
    create_table(conn)
    print("Table created.")