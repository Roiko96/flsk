# application.py – שרת Flask
from flask import Flask, render_template, request, redirect, url_for  # * יבוא Flask ותבניות
from functions import (  # * לוגיקה עסקית
    add_score_data, delete_score_by_name, sort_scores_by_key,
    calculate_average, edit_score_data, get_scores
)

app = Flask(__name__)  # * יצירת אפליקציית Flask

@app.route("/")  # * דף ראשי
def index():
    return render_template("index.html", scores=get_scores())  # * הצגת הטבלה

@app.route("/add", methods=["POST"])  # * הוספה
def add():
    name = request.form.get("name", "").strip()   # * שם
    game = request.form.get("game", "").strip()   # * משחק
    score_raw = request.form.get("score", "").strip()  # * ניקוד (טקסט גולמי)
    if name and game and score_raw:  # * ולידציה בסיסית
        try:
            add_score_data(name, game, float(score_raw))  # * המרה לשבר
        except ValueError:
            pass  # * קלט לא תקין – מתעלמים
    return redirect(url_for("index"))  # * רענון הדף אחרי פעולה (PRG)

@app.route("/delete", methods=["POST"])  # * מחיקה
def delete():
    name = request.form.get("name", "").strip()
    if name:
        delete_score_by_name(name)
    return redirect(url_for("index"))

@app.route("/sort/<key>")  # * מיון
def sort_view(key):
    sort_scores_by_key(key)
    return redirect(url_for("index"))

@app.route("/average")  # * ממוצע
def average():
    avg = calculate_average()
    return render_template("index.html", scores=get_scores(), average=avg)

@app.route("/edit", methods=["POST"])  # * עריכה
def edit():
    cur_name = request.form.get("current_name", "").strip()
    cur_game = request.form.get("current_game", "").strip()
    new_name = request.form.get("new_name", "").strip()
    new_game = request.form.get("new_game", "").strip()
    new_score_raw = request.form.get("new_score", "").strip()
    if cur_name and cur_game and new_name and new_game and new_score_raw:
        try:
            edit_score_data(cur_name, cur_game, new_name, new_game, float(new_score_raw))
        except ValueError:
            pass
    return redirect(url_for("index"))

if __name__ == "__main__":  # * הרצה מקומית
    app.run(host="0.0.0.0", port=5000)  # * מאזין על 5000 לכל הכתובות
