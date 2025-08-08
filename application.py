from flask import Flask, render_template, request, redirect
from functions import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", scores=get_scores(), average=calculate_average())

@app.route('/add', methods=["POST"])
def add():
    add_score_data(request.form["name"], request.form["game"], request.form["score"])
    return redirect("/")

@app.route('/edit', methods=["POST"])
def edit():
    edit_score_data(request.form["cur_name"], request.form["cur_game"],
                    request.form["new_name"], request.form["new_game"], request.form["new_score"])
    return redirect("/")

@app.route('/delete', methods=["POST"])
def delete():
    delete_score_by_name(request.form["name"])
    return redirect("/")

@app.route('/sort', methods=["POST"])
def sort():
    sort_scores_by_key(request.form["key"])
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)