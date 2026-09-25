def days_since(date_str):
    stored= date.fromisoformat(date_str)
    days_ago= (date.today()-stored).days

    return days_ago 

def save_problems(problems, filename="problems.json"):
     with open(filename,"w") as f:
        json.dump(problems,f, indent =4)

def load_problems(filename="problems.json"):
    with open(filename, "r") as f:
        return json.load(f)

def needs_review_by_date(problems,threshold_days):
    result= []
    for p in problems: 
        if days_since(p["last_reviewed"])>= threshold_days:
            result.append(p)

    return result

def backfill_last_reviewed(problems):
    for p in problems: 
        if "last_reviewed" not in p: 
            p["last_reviewed"]= str(date.today())

def add_problem(problems, name, topic, difficulty, needed_hint):
    problems.append({
        "name":name, 
        "topic": topic, 
        "difficulty": difficulty, 
        "need_hint": needed_hint, 
        "last_reviewed": str(date.today())
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
    headers= ["Name", "Topic", "Difficulty", "Last Reviewed"]
    for p in problems:
        rows.append([p["name"], p["topic"], p["difficulty"], p["last_reviewed"]])
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
"""""
def search_by_topic(problems, topic):
    result = []
    topic = topic.title()

    for problem in problems: 
        if problem["topic"]== topic:
            result.append(problem)


    if not result: 
        print(f"{topic}: Topic Not Found")

    return result 
"""

def search_by_topic(problems, partial):
    result=[]

    for problem in problems: 
        if partial.lower() in problem["topic"].lower(): 
            result.append(problem)

    if not result: 
        print(f"{partial} not found")

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
    return [p for p in problems if name.lower() in p["name"].lower()]

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


def edit_difficulty(problems, name):
    matches= find_by_name(problems,name)
    if len(matches)==0: 
        print("No problem found with that name.")
        return
    elif len(matches)==1:
        new_rank= input("Enter new level of difficulty: ")
        matches[0]["difficulty"]= new_rank.strip().title()
    elif len(matches)>1:
        print_numbered(matches)
        choice = input("Enter a number").strip()
        choice = int(choice)
        for i,m in enumerate(matches):
            if choice == i+1:
                new_rank= input("Enter new level of difficulty: ")
                m["difficulty"]=new_rank.strip().title()
                
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

def search_by_partial_name(problems,partial):
    matches=[]
    for p in problems: 
        if partial.lower() in p["name"].lower():
            matches.append(p)

    return matches 

def mark_reviewed(problems,name):
    matches= find_by_name(problems,name)
    if len(matches)==0:
        print(f"No problem found with that {name}.")
        return
    elif len(matches)==1: 
        print_numbered(matches)
        matches[0]["last_reviewed"]=str(date.today())
    elif len(matches)>=2:
        print_numbered(matches)
        choice= input("Please choose a problem to mark as reviewed: ").strip()
        choice= int(choice)
        for i,m in enumerate(matches):
            if choice==i+1:
                m["last_reviewed"]=str(date.today())
            
def delete_problem(problems,name):
    matches= find_by_name(problems,name)
    if len(matches)==0:
        print(f"No problem found with that {name}.")
        return 
    elif len(matches)==1: 
        problems.remove(matches[0])
    elif len(matches)>=2:
        print_numbered(matches)
        choice=input("Select the problem you'd like to remove: ").strip()
        choice=int(choice)
        for i,m in enumerate(matches):
            if choice==i+1: 
                problems.remove(m)


def convert_rows(rows):
    result= [{"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in rows]
    print_table_v2(result) 
