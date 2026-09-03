from tabulate import tabulate

import json
import random 
import heapq

def save_problems(problems, filename="problems.json"):
     with open(filename,"w") as f:
        json.dump(problems,f, indent =4)

def load_problems(filename="problems.json"):
    with open(filename, "r") as f:
        return json.load(f)

def add_problem(problems, name, topic, difficulty, needed_hint):
    problems.append({
        "name":name, 
        "topic": topic, 
        "difficulty": difficulty, 
        "need_hint": needed_hint
        })
    
def get_new_problem():
    name = input("Enter problem name: ").strip().title()
    topic = input("Enter topic name: ").strip().title()
    difficulty = input("Enter difficulty: ").strip().title()
    hint_answer= input("Did you need a hint? (y/n): ").strip()
    needed_hint= hint_answer.lower()=="y"

    return name,topic, difficulty,needed_hint

def count_by_topic(problems): 
    count = {}
    for problem in problems: 
        topic = problem["topic"] #topic is one of the keys from problems dict 
        count[topic]= count.get(topic,0)+1
    
    return count 
    
def problems_needing_review(problems):
    matches = [p for p in problems if p["need_hint"]]
    line = []
    for i, problem in enumerate(matches):
        if problem["need_hint"]==True:
            result = f'{i+1}. {problem["name"]}'
            line.append(result)
          
            
    return "\n".join(line)
 

def print_problems(problems):
    lines=[]
    for i, p in enumerate(problems): 
            result= f'{i+1}. {p["name"]} ({p["topic"]}, {p["difficulty"]})' 
            if p["need_hint"] == True:
                result+= " - needs review"
            lines.append(result)
    return "\n".join(lines)

def print_table_v2(problems):
    rows= []
    headers= ["Name", "Topic", "Difficulty"]
    for p in problems:
        rows.append([p["name"], p["topic"], p["difficulty"]])
    print(tabulate(rows,headers=headers, tablefmt= "grid", showindex=range(1, len(rows)+1)))

def print_table(problems):
    lines= [f"{'':<4}{'Name':<27}{'Topic':21}{'Difficulty':<13}"]
    for i,p in enumerate(problems):
        lines.append(f'{str(i+1)+".":<4}{p["name"]:<25}  {p["topic"]:<20} {p["difficulty"]:<12}')
    return "\n".join(lines)

def print_numbered(problems):
    for i,problem in enumerate(problems):
        print(f"{i+1}. {problem['name']}: ({problem['topic']}, {problem['difficulty']})")

def get_search_problem():
    topic = input("Enter topic name: ").strip().title()

    return topic

def search_by_topic(problems, topic):
    result = []
    topic = topic.title()

    for problem in problems: 
        if problem["topic"]== topic:
            result.append(problem)


    if not result: 
        print(f"{topic}: Topic Not Found")

    return result 

def merge_sort(problems):
    if len(problems)<=1:
        return problems
    mid = len(problems)//2
    left = merge_sort(problems[:mid])
    right = merge_sort(problems[mid:])

    return merge(left,right)

def merge(left,right):
    result=[]
    i,j= 0,0
    difficult_rank={"Hard":0, "Medium":1, "Easy":2}
    while i <len(left) and j<len(right): 
        if difficult_rank[left[i]["difficulty"]]< difficult_rank[right[j]["difficulty"]]:
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1 
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result 

def quicksort(problems):
    if len(problems)<=1:
        return problems

    pivot_index= random.randint(0,len(problems)-1)
    pivot = problems[pivot_index]
    remaining = problems[:pivot_index]+ problems[pivot_index+1:]

    left= [p for p in remaining if p["name"]<pivot["name"]]
    right= [p for p in remaining if p["name"]>pivot["name"]]

    return quicksort(left)+ [pivot]+quicksort(right)

def find_by_name(problems, name):
    matches= [p for p in problems if p["name"].lower()== name.lower()]
    return matches 

def edit_topic(problems,name):
    matches= find_by_name(problems, name)
    if len(matches)==0:
        print("No Problem found with that name.")
        return
    elif len(matches)==1: 
        new_topic = input("Enter new topic: ")
        matches[0]["topic"]= new_topic.strip().title()
    elif len(matches)>1: 
        print_numbered(matches)
        choice = input("Enter a number: ").strip()
        choice = int(choice)
        for i, m in enumerate(matches): 
            if choice == i+1: 
                new_topic = input("Enter new topic: ")
                m["topic"]= new_topic.strip().title()

def heap(problems,k):
    rank = {"Hard":0, "Medium":1, "Easy":2}
    
    heap_data=[]
    for i, p in enumerate(problems): 
        heap_data.append((rank[p["difficulty"]],i ,p))
    heapq.heapify(heap_data)
    
    result=[]
    for _ in range(k):
        rank_val,index, problem = heapq.heappop(heap_data)
        result.append(problem)
    return result 

   


try:
    problems= load_problems("problems.json")
except FileNotFoundError: 
    problems=[]

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
    print("8. Print 3 of the Hardest Problems:")
    print("9. Quit?")
    choice = input("Enter a number: ").strip()

    if choice == "1":
        name, topic, difficulty, hint = get_new_problem()
        add_problem(problems, name, topic, difficulty, hint)
        save_problems(problems, "problems.json")
    elif choice == "2":
        topic = get_search_problem()
        
        result = search_by_topic(problems, topic)
        print("=" * 40)
        print(f"Topic: {topic}")
        print_numbered(result)
    elif choice == "3":
        print("=" * 40)
        print(print_table(problems))
    elif choice == "4":
        print("=" * 40)
        print("Topics needing Review: \n ")
        print(problems_needing_review(problems))   
    elif choice == "5":
        print("=" * 60)
        sorted_problem=(merge_sort(problems)) 
        print_table_v2(sorted_problem)
    elif choice == "6":
        print("=" * 60)
        sorted_problem=(quicksort(problems)) 
        print_table_v2(sorted_problem)
    elif choice == "7":
        name= input("Enter the problem name to edit: ").strip().title()
        print("=" * 60)
        edit_topic(problems,name)   
        save_problems(problems, "problems.json")
    elif choice == "8":
        print("=" * 60)
        heap_p= heap(problems,3)
        print_table_v2(heap_p)  

    elif choice == "9":
        break
    else: 
        print("Invalid choice, try again")




"""
add_new = input("Add a new problem? (y/n): ")
if add_new.lower()=='y':
    name, topic, difficulty, hint = get_new_problem()
    add_problem(problems, name, topic, difficulty, hint)
    save_problems(problems, "problems.json")

print("=" * 40)
search_prob = input("Search for a topic? (y/n): ")
if search_prob.lower()=='y':
    topic = get_search_problem()
    result = search_by_topic(problems, topic)
    print_numbered(result)

print("=" * 40)
print(f"Listing out problems: ")
for i,problem in enumerate(problems): # new line because this function doesn't have a return. it prints within the function 
    suffix = " - needs review" if problem["need_hint"] else ""
    print(f"{i+1}. {problem['name']} ({problem['topic']}, {problem['difficulty']}{suffix})")


print("=" * 40)
print(f"counting by topics:\n{count_by_topic(problems)}")

#print("=" * 40)
#topic = "dynamic programming"
#result= search_by_topic(problems, topic)
#print(f"Searching for {topic} problem: ")
#print_numbered(result)

#print(f"problems needing review: {problems_needing_review(problems)}")
"""