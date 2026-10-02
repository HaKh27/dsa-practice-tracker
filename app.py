from flask import Flask, request, jsonify, render_template
from db import get_connection,insert_problems, get_all_problems, needs_review
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
    data = [{"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in result]

    return jsonify(data)

@app.route("/get-needs-review", methods=["GET"])
def get_needs_review():
    conn=get_connection()
    result= needs_review(conn)
    data = [{"name":r[1],"topic":r[2], "difficulty":r[3],"last_reviewed": r[4]} for r in result]
    return jsonify(data)

if __name__=="__main__":
    app.run(debug=True)  # starts the dev server, auto-reloads on code changes