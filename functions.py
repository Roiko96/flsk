# functions.py
scores = []  # * רשימת ציונים בזיכרון (ללא DB)

def add_score_data(name, game, score):  # * הוספת רשומה
    scores.append({"name": name, "game": game, "score": float(score)})

def delete_score_by_name(name):  # * מחיקה לפי שם
    global scores  # * עדכון גלובלי של הרשימה
    scores = [s for s in scores if s["name"] != name]

def sort_scores_by_key(key):  # * מיון לפי שדה
    reverse = key == "score"  # * ניקוד – יורד
    if key in ["name", "game", "score"]:
        scores.sort(key=lambda x: x[key], reverse=reverse)

def calculate_average():  # * ממוצע
    return sum(s["score"] for s in scores) / len(scores) if scores else 0

def edit_score_data(cur_name, cur_game, new_name, new_game, new_score):  # * עדכון רשומה
    for s in scores:
        if s["name"] == cur_name and s["game"] == cur_game:
            s.update({"name": new_name, "game": new_game, "score": float(new_score)})
            break

def get_scores():  # * החזרת הרשימה לתצוגה
    return scores
