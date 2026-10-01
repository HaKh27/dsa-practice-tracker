from flask import Flask, request, jsonify, render_template
from db import get_connection,insert_problems
from datetime import date 

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

if __name__=="__main__":
    app.run(debug=True)  # starts the dev server, auto-reloads on code changes