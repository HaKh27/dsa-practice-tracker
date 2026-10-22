import sqlite3
from datetime import date, timedelta
import os 
from dotenv import load_dotenv
import psycopg2

load_dotenv()
db_host= os.environ.get("DB_HOST")
db_name= os.environ.get("DB_NAME")
db_user= os.environ.get("DB_USER")
db_password= os.environ.get("DB_PASSWORD")
db_port= os.environ.get("DB_PORT", "5432")


def get_connection(db_name=None):
    db_host= os.environ.get("DB_HOST")
    if db_name==None: 
        db_name= os.environ.get("DB_NAME")
    db_user= os.environ.get("DB_USER")
    db_password= os.environ.get("DB_PASSWORD")
    db_port= os.environ.get("DB_PORT", "5432")


    return psycopg2.connect(host=db_host, dbname= db_name, user=db_user, password= db_password, port=db_port)


ALLOWED_FIELDS={"name", "topic", "difficulty", "last_reviewed"}
def update_field_sql(conn,id, field, value):
    if field not in ALLOWED_FIELDS:
        raise ValueError("Invalid field")

    query=f"UPDATE problems SET {field}=%s WHERE id=%s"
    cursor= conn.cursor()
    cursor.execute(query, (value,id))
    conn.commit()


def filter_by_difficulty(conn,value):
    placeholder= ", ".join(["%s"]*len(value))
    cursor=conn.cursor()
    cursor.execute(f"""
        SELECT * FROM problems
        WHERE difficulty IN ({placeholder})
        ORDER BY
            CASE difficulty
                    WHEN 'Easy' THEN 1
                    WHEN 'Medium' THEN 2 
                    WHEN 'Hard' THEN 3
            END
    """ , value)
    return cursor.fetchall()

def filter_problems(conn, difficulties, topics):
    conditions=[]
    params=[]

    if difficulties:
        placeholders=", ".join(["%s"]* len(difficulties))
        conditions.append(f"difficulty IN ({placeholders})")
        params.extend(difficulties)

    if topics: 
        placeholders= ", ".join(["%s"]*len(topics))
        conditions.append(f"LOWER(topic) IN ({placeholders})")
        params.extend([t.lower() for t in topics])

    where_clause= " AND ".join(conditions) if conditions else "TRUE"

    cursor= conn.cursor()
    cursor.execute(f"""
        SELECT * FROM problems 
        WHERE {where_clause}
        ORDER BY 
            CASE difficulty
                WHEN 'Easy' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Hard' THEN 3 
            END
    """, params)
    return cursor.fetchall()


def get_distinct_topics(conn):
    cursor= conn.cursor()
    cursor.execute("""
        SELECT DISTINCT ON (LOWER(topic)) topic 
        FROM problems 
        ORDER BY LOWER(topic),topic
    """)
    return cursor.fetchall()

def create_table(conn):
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id SERIAL PRIMARY KEY,
            name TEXT,
            topic TEXT,
            difficulty TEXT,
            last_reviewed TEXT
        )
    """)
    conn.commit()


def insert_problems(conn,name,topic,difficulty,last_reviewed=str(date.today())):
    cursor= conn.cursor()
    cursor.execute("""
        INSERT INTO problems(name, topic, difficulty, last_reviewed)
        VALUES(%s, %s, %s, %s)
    """, (name, topic, difficulty, last_reviewed))
    conn.commit()



def get_all_problems(conn):
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM problems")
    return cursor.fetchall()

def get_by_topic(conn, topic):
    cursor= conn.cursor()
    cursor.execute("""
    SELECT * 
    FROM problems
    WHERE topic ILIKE %s
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

def migrate_sqlite_to_postgres(new_conn):
    old_conn= sqlite3.connect("tracker.db")
    old_cursor= old_conn.cursor()
    old_cursor.execute("SELECT * FROM problems")
    rows= old_cursor.fetchall()

    for r in rows: 
        name=r[1]
        topic=r[2]
        difficulty=r[3]
        last_reviewed=r[4]
        insert_problems(new_conn, name, topic, difficulty, last_reviewed)

    old_conn.close()


def needs_review(conn):
    cutoff= str(date.today()-timedelta(days=7))
    cursor= conn.cursor()
    cursor.execute("""
    SELECT * 
    FROM problems 
    WHERE last_reviewed < %s 
    ORDER BY last_reviewed ASC

    """, (cutoff,))
    return cursor.fetchall()

def get_sorted_by_difficulty(conn):
    cursor=conn.cursor()
    cursor.execute("""
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
    cursor= conn.cursor()
    cursor.execute(""" 
    UPDATE problems 
    SET topic=%s
    WHERE name LIKE %s

    """, (new_topic, name,))
    
    conn.commit()

def edit_last_reviewed(conn, last_reviewed,id ):
    cursor= conn.cursor()
    cursor.execute("""
    UPDATE problems 
    SET last_reviewed=%s
    WHERE id=%s
    
    """,(last_reviewed,id,))
    conn.commit()

def edit_last_reviewed_by_name(conn,last_reviewed,name):
    cursor= conn.cursor()
    cursor.execute("""
    UPDATE problems 
    SET last_reviewed=%s
    WHERE name LIKE %s
    """, (last_reviewed, name,))
    conn.commit()


def edit_difficulty_sql(conn,new_rank,name):
    cursor= conn.cursor()
    cursor.execute(""" 
    UPDATE problems 
    SET difficulty=%s
    WHERE name LIKE %s

    """, (new_rank, name,))
    conn.commit()


def find_by_name_sql(conn, name):
    cursor= conn.cursor()
    cursor.execute("""
    SELECT * 
    FROM problems 
    WHERE name ILIKE %s
    """, ('%'+ name+ '%',))
    return cursor.fetchall()

def edit_topic_by_id_sql(conn, new_topic, id):
    cursor= conn.cursor()
    cursor.execute(""" 
    UPDATE problems 
    SET topic=%s
    WHERE id= %s
    
    """, (new_topic, id,))
    conn.commit()

def edit_difficulty_by_id_sql(conn, new_rank, id):
    cursor= conn.cursor()
    cursor.execute("""
    UPDATE problems
    SET difficulty=%s
    WHERE id=%s
    
    """,(new_rank,id,))
    conn.commit()


def get_sorted_by_name(conn):
    cursor= conn.cursor()
    cursor.execute("""
    SELECT * 
    FROM problems 
    ORDER BY name asc 
    """)
    return cursor.fetchall()


def return_top_3_hardest_problems(conn):
    cursor= conn.cursor()
    cursor.execute("""
    SELECT * 
    FROM problems 
    ORDER BY
        CASE difficulty 
            WHEN 'Hard' THEN 1
            WHEN 'Medium' THEN 2
            WHEN 'Easy' THEN 3 
        END
        LIMIT  3;
    """)
    return cursor.fetchall()

def delete_problem_sql(conn, id):
    cursor= conn.cursor()
    cursor.execute("""
    DELETE FROM problems 
    WHERE id = %s 
     """, (id,))

    conn.commit()

def delete_problem_by_name_sql(conn, name):
    cursor= conn.cursor()
    cursor.execute("""
    DELETE FROM problems 
    WHERE name LIKE %s  
     """, (name,))

    conn.commit()



if __name__=="__main__":
    conn= get_connection()
    migrate_json_to_sql(conn)
    print("Migration complete.")