# application.py
# flask scoreboard app (english ui) for elastic beanstalk docker
# wsgi entrypoint: `app` (see wsgi.py)

from flask import Flask, request, redirect, url_for, render_template, jsonify
import socket, time
from functions import (
    sort_scores_by_key, add_score, delete_score_by_name,
    edit_score, calc_average
)

app = Flask(__name__)
scores = []  # in-memory for demo; each EB instance/worker has its own copy

@app.after_request
def no_cache(resp):
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/")
def index():
    sort_key = (request.args.get("sort") or "").lower()
    order = (request.args.get("order") or "asc").lower()
    show_average = request.args.get("average") is not None

    view = list(scores)
    if sort_key in {"name", "game", "score"}:
        sort_scores_by_key(view, sort_key, reverse=(order == "desc"))

    avg = calc_average(view) if show_average else None

    return render_template(
        "index.html",
        hostname=socket.gethostname(),
        scores=view,
        average=avg,
        now_ms=int(time.time() * 1000),
    )

@app.route("/sort/<key>")
def sort_view(key: str):
    key = (key or "").lower()
    if key not in {"name", "game", "score"}:
        return redirect(url_for("index"))
    order = "desc" if key == "score" else "asc"
    return redirect(url_for("index", sort=key, order=order, t=int(time.time()*1000)))

@app.route("/add", methods=["POST"])
def add_view():
    name = (request.form.get("name") or "").strip()
    game = (request.form.get("game") or "").strip()
    score = (request.form.get("score") or "").strip()
    if name and game and score != "":
        add_score(scores, name=name, game=game, score=score)
    return redirect(url_for("index", t=int(time.time()*1000)))

@app.route("/delete", methods=["POST"])
def delete_view():
    name = (request.form.get("name") or "").strip()
    game = (request.form.get("game") or "").strip() or None
    if name:
        delete_score_by_name(scores, name=name, game=game)
    return redirect(url_for("index", t=int(time.time()*1000)))

@app.route("/edit", methods=["POST"])
def edit_view():
    current_name = (request.form.get("current_name") or "").strip()
    current_game = (request.form.get("current_game") or "").strip()
    new_name = (request.form.get("new_name") or "").strip() or None
    new_game = (request.form.get("new_game") or "").strip() or None
    new_score = (request.form.get("new_score") or "").strip() or None
    if current_name and current_game:
        edit_score(scores, current_name=current_name, current_game=current_game,
                   new_name=new_name, new_game=new_game, new_score=new_score)
    return redirect(url_for("index", t=int(time.time()*1000)))

# simple json helpers (optional)
@app.route("/api/scores")
def api_scores():
    return jsonify(scores), 200

@app.route("/api/average")
def api_average():
    return jsonify({"average": calc_average(scores)}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
