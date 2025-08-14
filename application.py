from flask import Flask, render_template, request, redirect, url_for
from functions import (
    add_score_data, delete_score_by_name, edit_score_data,
    calculate_average, get_scores, get_sorted_scores
)
import os, re, time

app = Flask(__name__)

def parse_score(raw):
    if raw is None: return None
    raw = str(raw).strip().replace(",", ".")
    raw = re.sub(r"[^0-9.\-]", "", raw)
    try: return float(raw)
    except Exception: return None

@app.after_request
def no_cache(resp):
    resp.headers["Cache-Control"]="no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"]="no-cache"; resp.headers["Expires"]="0"
    return resp

@app.context_processor
def inject_host():
    return {"host": os.getenv("HOSTNAME","eb")}

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/")
def index():
    sort_key = request.args.get("sort")
    order = (request.args.get("order","asc") or "asc").lower()
    allowed = {"name","game","score"}
    if sort_key in allowed:
        view = get_sorted_scores(sort_key, reverse=(order=="desc"))
    else:
        view = get_scores()
    if request.args.get("average") is not None:
        avg = calculate_average()
        return render_template("index.html", scores=view, average=avg)
    return render_template("index.html", scores=view)

@app.route("/sort/<key>")
def sort_view(key):
    key = key.lower()
    if key not in {"name","game","score"}:
        return redirect(url_for("index"))
    order = "desc" if key == "score" else "asc"
    return redirect(url_for("index", sort=key, order=order, t=int(time.time()*1000)))

@app.route("/add", methods=["POST"])
def add():
    name = (request.form.get("name") or "").strip()
    game = (request.form.get("game") or "").strip()
    score = parse_score(request.form.get("score"))
    if name and game and score is not None:
        add_score_data(name, game, score)
    return redirect(url_for("index", t=int(time.time()*1000)))

@app.route("/delete", methods=["POST"])
def delete():
    name = (request.form.get("name") or "").strip()
    game = (request.form.get("game") or "").strip()
    if name:
        delete_score_by_name(name, game if game else None)
    return redirect(url_for("index", t=int(time.time()*1000)))

@app.route("/average")
def average():
    avg = calculate_average()
    return render_template("index.html", scores=get_scores(), average=avg)

@app.route("/edit", methods=["POST"])
def edit():
    cur_name = (request.form.get("current_name") or "").strip()
    cur_game = (request.form.get("current_game") or "").strip()
    new_name = (request.form.get("new_name") or "").strip()
    new_game = (request.form.get("new_game") or "").strip()
    new_score = parse_score(request.form.get("new_score"))
    if cur_name and cur_game:
        edit_score_data(
            cur_name, cur_game,
            new_name if new_name else None,
            new_game if new_game else None,
            new_score if new_score is not None else None
        )
    return redirect(url_for("index", t=int(time.time()*1000)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)