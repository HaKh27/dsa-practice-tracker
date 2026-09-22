import sqlite3
from datetime import date, timedelta

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

def insert_problems(conn,name,topic,difficulty,last_reviewed=str(date.today())):
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
    WHERE topic LIKE ?
    """, ( '%' + topic + '%',)) 
    return cursor.fetchall()

def migrate_json_to_sql(conn):
    from dsa_tracker import load_problems

    problems=load_problems(filename="problems.json")

    problem= get_all_problems(conn)

    for p in problems:
        found= False
        for row in problem: 
            if p["name"]== row[1] and p["topic"]== row[2]: 
                found= True
                break 
        if found==False:           
            insert_problems(conn,p["name"],p["topic"],p["difficulty"],p["last_reviewed"])

def needs_review(conn):
    cutoff= str(date.today()-timedelta(days=7))

    cursor= conn.execute("""
    SELECT * 
    FROM problems 
    WHERE last_reviewed < ? 
    """, (cutoff,))
    return cursor.fetchall()

def get_sorted_by_difficulty(conn):
    cursor= conn.execute("""
    SELECT * 
    FROM problems
    ORDER BY 
        CASE difficulty
            WHEN 'Easy' THEN 3
            WHEN 'Medium' THEN 2 
            WHEN 'Hard' THEN 1
        END
    """)
    return cursor.fetchall()

def edit_topic_sql(conn,new_topic,name):
    conn.execute(""" 
    UPDATE problems 
    SET topic=?
    WHERE name LIKE ?

    """, (new_topic, name,))
    conn.commit()

def find_by_name_sql(conn, name):
    cursor= conn.execute("""
    SELECT * 
    FROM problems 
    WHERE name LIKE ? 
    """, (name,))
    return cursor.fetchall()

def edit_topic_by_id_sql(conn, new_topic, id):
    conn.execute(""" 
    UPDATE problems 
    SET topic=?
    WHERE id= ?
    
    """, (new_topic, id,))
    conn.commit()

def get_sorted_by_name(conn):
    cursor= conn.execute("""
    SELECT * 
    FROM problems 
    ORDER BY name asc 
    """)
    return cursor.fetchall()



if __name__=="__main__":
    conn= get_connection()
    migrate_json_to_sql(conn)
    print("Migration complete.")