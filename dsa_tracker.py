from tabulate import tabulate
from datetime import date
from db import get_connection, insert_problems, get_all_problems, get_by_topic, needs_review, get_sorted_by_difficulty, get_sorted_by_name,edit_topic_sql, find_by_name_sql, edit_topic_by_id_sql,edit_difficulty_by_id_sql, edit_difficulty_sql, return_top_3_hardest_problems,edit_last_reviewed, edit_last_reviewed_by_name, delete_problem_by_name_sql, delete_problem_sql

def get_new_problem():
    name = input("Enter problem name: ").strip().title()
    topic = input("Enter topic name: ").strip().title()
    difficulty = input("Enter difficulty: ").strip().title()
    hint_answer= input("Did you need a hint? (y/n): ").strip()
    needed_hint= hint_answer.lower()=="y"

    return name,topic, difficulty,needed_hint

def print_table_v2(problems):
    rows= []
    headers= ["Name", "Topic", "Difficulty", "Last Reviewed"]
    for p in problems:
        rows.append([p["name"], p["topic"], p["difficulty"], p["last_reviewed"]])
    print(tabulate(rows,headers=headers, tablefmt= "grid", showindex=range(1, len(rows)+1)))

def print_numbered(problems):
    for i,problem in enumerate(problems):
        print(f"{i+1}. {problem['name']}: ({problem['topic']}, {problem['difficulty']})")

def convert_rows(rows):
    result= [{"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in rows]
    print_table_v2(result) 



if __name__=="__main__":
    conn = get_connection()


    print("\nDS&A TRACKER: ")
    print("=" * 40)

    while True:
        print("\n")
        print("What would you like to do?")
        print("1. Add a new problem?")
        print("2. Search by topic")
        print("3. View all problems?")
        print("4. View problems needing review?")
        print("5. Sort Problems by Difficulty: ")
        print("6. Sort Problems by Name: ")
        print("7. Change Topic name: ")
        print("8. Change level of difficulty: ")
        print("9. Print 3 of the Hardest Problems:")
        print("10. Search a problem by name using substring:")
        print("11. Mark a problem as reviewed: ")
        print("12. Delete a problem?")
        print("13. Quit?")
        choice = input("Enter a number: ").strip()

        if choice == "1":
            name, topic, difficulty, hint = get_new_problem()
            insert_problems(conn, name, topic, difficulty, last_reviewed= str(date.today()))
        elif choice == "2":
            print("=" * 40)
            partial= input("Enter partial Topic name: ").strip()
            result = get_by_topic(conn, partial)
            convert_rows(result)
        elif choice == "3":
            print("=" * 40)
            rows= get_all_problems(conn) #raw tuples 
            #convert the tuples to dict 
            converted= [{"name":r[1], "topic":r[2], "difficulty":r[3], "last_reviewed": r[4]} for r in rows]
            print_table_v2(converted)
        elif choice == "4":
            print("=" * 40)
            stale= needs_review(conn)
            convert_rows(stale)
        elif choice == "5":
            print("=" * 60)
            sorted_problem=get_sorted_by_difficulty(conn) 
            convert_rows(sorted_problem)

        elif choice == "6":
            print("=" * 60)
            sorted_problem=get_sorted_by_name(conn) 
            convert_rows(sorted_problem)
        elif choice == "7":
            name= input("Enter the problem name to edit: ").strip().title()
            print("=" * 60)
            matches= find_by_name_sql(conn,name)

            if len(matches)==0:
                print("No problems found with that name.")
            elif len(matches)==1:
                new_topic= input("Enter a new topic name: ").strip().title()
                edit_topic_sql(conn, new_topic, name)
            elif len(matches)>1:
                convert_matches= [{"name":m[1], "topic":m[2], "difficulty":m[3], "last_reviewed":m[4]} for m in matches]
                print_numbered(convert_matches)
                c= input("Enter a number: ").strip() 
                c= int(c)
                for i,m in enumerate(matches):
                    if c==i+1:
                        new_topic= input("Enter a new topic name: ").strip().title()
                        edit_topic_by_id_sql(conn,new_topic, m[0])
            print("Topic Updated")
          
        elif choice == "8":
            name= input("Enter the problem name to edit its difficulty: ").strip().title()
            print("=" * 60)
            matches= find_by_name_sql(conn,name)
            
            if len(matches)==0:
                print("No problems found with that name.")
            elif len(matches)==1:
                new_rank= input("Enter a new difficulty rank: ").strip().title()
                edit_difficulty_sql(conn, new_rank, name)
                print("Difficulty Updated")
            elif len(matches)>1:
                convert_matches= [{"name":m[1], "topic":m[2], "difficulty":m[3], "last_reviewed":m[4]} for m in matches]
                print_numbered(convert_matches)
                c= input("Enter a number: ").strip() 
                c= int(c)
                for i,m in enumerate(matches):
                    if c==i+1:
                        new_rank= input("Enter a new difficulty rank: ").strip().title()
                        edit_difficulty_by_id_sql(conn,new_rank, m[0])
                        print("Difficulty Updated")        

        elif choice == "9":
            print("=" * 60)
            result= return_top_3_hardest_problems(conn)
            convert_rows(result)
        elif choice == "10":
            print("=" * 60)
            partial= input("Enter partial problem name: ").strip()
            results= find_by_name_sql(conn,partial)
            if not results:
                print(f"No problems found matching '{partial}'.")
            else:
                convert_rows(results)
        elif choice == "11":
            print("=" * 60)
            name= input("Enter the problem name to update its last reviewed date: ").strip().title()
            matches= find_by_name_sql(conn,name)        
            if len(matches)==0:
                print("No problems found with that name.")
            elif len(matches)==1:
                new_date= str(date.today())
                edit_last_reviewed_by_name(conn, new_date, name)
                print("Date Updated")
            elif len(matches)>1:
                convert_matches= [{"name":m[1], "topic":m[2], "difficulty":m[3], "last_reviewed":m[4]} for m in matches]
                print_numbered(convert_matches)
                c= input("Enter a number: ").strip() 
                c= int(c)
                for i,m in enumerate(matches):
                    if c==i+1:
                        new_date= str(date.today())
                        edit_last_reviewed(conn,new_date, m[0])
                        print("Date Updated")   
        elif choice == "12":
            print("=" * 60)
            name= input("Enter the name of the problem you'd like to delete: ").strip().title()
            matches= find_by_name_sql(conn,name)        
            if len(matches)==0:
                print("No problems found with that name.")
            elif len(matches)==1:
                delete_problem_by_name_sql(conn, name)
                print(f"{name} Deleted")
            elif len(matches)>1:
                convert_matches= [{"name":m[1], "topic":m[2], "difficulty":m[3], "last_reviewed":m[4]} for m in matches]
                print_numbered(convert_matches)
                c= input("Choose which problem to delete by number: ").strip() 
                c= int(c)
                for i,m in enumerate(matches):
                    if c==i+1:
                        delete_problem_sql(conn, m[0])
                        print(f"{m[1]} Deleted") 
            
        elif choice == "13":
            break
        else: 
            print("Invalid choice, try again")



