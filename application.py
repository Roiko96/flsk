from flask import Flask, render_template, request, redirect, url_for
from functions import add_score_data, delete_score_by_name, edit_score_data, get_scores
import os, re

app = Flask(__name__)

def _parse_score(raw: str):
    if raw is None: return None
    raw = raw.strip().replace(",", ".")
    raw = re.sub(r"[^0-9.\-]", "", raw)
    try:
        return float(raw)
    except Exception:
        return None

@app.after_request
def no_cache(resp):
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

@app.context_processor
def inject_host():
    return {"host": os.getenv("HOSTNAME", "eb")}

@app.route("/")
def index():
    sort_key = request.args.get("sort")
    order = request.args.get("order", "asc")
    return render_template("index.html", scores=get_scores(sort_key, order))

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name","").strip()
    game = request.form.get("game","").strip()
    score = _parse_score(request.form.get("score",""))
    if name and game and score is not None:
        add_score_data(name, game, score)
    # מוסיפים קוורי קטן כדי לשבור קאש של פרוקסי אם יש
    return redirect(url_for("index", t=int(os.times().elapsed*1000)))

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name","").strip()
    if name:
        delete_score_by_name(name)
    return redirect(url_for("index", t=int(os.times().elapsed*1000)))

@app.route("/sort/<key>")
def sort_view(key):
    order = "desc" if key == "score" else "asc"
    return redirect(url_for("index", sort=key, order=order, t=int(os.times().elapsed*1000)))

@app.route("/edit", methods=["POST"])
def edit():
    cur_name = request.form.get("current_name","").strip()
    cur_game = request.form.get("current_game","").strip()
    new_name = request.form.get("new_name","").strip()
    new_game = request.form.get("new_game","").strip()
    new_score = _parse_score(request.form.get("new_score",""))
    if cur_name and cur_game and new_name and new_game and new_score is not None:
        edit_score_data(cur_name, cur_game, new_name, new_game, new_score)
    return redirect(url_for("index", t=int(os.times().elapsed*1000)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
