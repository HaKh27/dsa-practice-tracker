from flask import Flask, request, jsonify, render_template
from db import get_connection,insert_problems, get_all_problems, needs_review,delete_problem_sql, edit_topic_by_id_sql, get_by_topic,find_by_name_sql, update_field_sql
from datetime import date 
from dsa_tracker import convert_rows

app= Flask(__name__)  # creates the Flask application instance

@app.route("/")  # handles requests to the root URL
def home():
    return render_template("skeleton.html")


@app.route("/add-problem", methods=["POST"]) # only responds to POST requests
def add_problem():
    data= request.get_json() # parses the incoming JSON body into a Python dict
    name= data["name"]
    topic= data["topic"]
    difficulty= data["difficulty"]

    conn= get_connection() # open a connection to tracker.db
    insert_problems(conn,name,topic, difficulty, str(date.today())) # insert into SQL

    return jsonify({"message": "Problem added succesfully"})# send a JSON response back

@app.route("/get-problems", methods= ["GET"])
def get_problems():
    conn=get_connection()
    result= get_all_problems(conn)
    data = [{"id":r[0],"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in result]

    return jsonify(data)

@app.route("/get-needs-review", methods=["GET"])
def get_needs_review():
    conn=get_connection()
    result= needs_review(conn)
    data = [{"id":r[0],"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in result]
    return jsonify(data)

@app.route("/delete-problem", methods=["POST"])
def delete_problem():
    data=request.get_json()
    id=data["id"]

    conn=get_connection()
    delete_problem_sql(conn,id)
    return jsonify({"message": "Problem delete succesfully"})# send a JSON response back

@app.route("/edit-topic", methods=["PUT"])
def edit_topic():
    data=request.get_json()
    topic=data["topic"]
    id=data["id"]

    conn=get_connection()
    edit_topic_by_id_sql(conn,topic,id)
    return jsonify({"message":"Topic updated"})

@app.route("/search-by-name",methods=["GET"])
def search_by_name():
    conn=get_connection()
    partial=request.args.get("partial")
    result= find_by_name_sql(conn,partial)
    data = [{"id":r[0],"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in result]
    return jsonify(data)

@app.route("/search-by-topic", methods=["GET"])
def search_by_topic():
    conn= get_connection()
    topic=request.args.get("partial")
    result= get_by_topic(conn,topic)
    data = [{"id":r[0],"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in result]
    return jsonify(data)

@app.route("/update-field", methods=["PUT"])
def update_field():
    data=request.get_json()
    conn=get_connection()
    field=data["field"]
    id=data["id"]
    value=data["value"]
    
    try:
        update_field_sql(conn,id,field,value)
        return jsonify({"message":"field updated"})
    except ValueError as e:
        return jsonify({"error": str(e)}),400

if __name__=="__main__":
    app.run(debug=True)  # starts the dev server, auto-reloads on code changes