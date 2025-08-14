scores = []

def _to_float(x):
    try:
        return float(x)
    except Exception:
        return 0.0

def add_score_data(name, game, score):
    scores.append({"name": name, "game": game, "score": _to_float(score)})

def delete_score_by_name(name):
    global scores
    scores = [s for s in scores if s.get("name","") != name]

def sort_scores_by_key(key):
    if key not in {"name","game","score"}:
        return
    reverse = (key == "score")
    def k(s):
        v = s.get(key, 0 if key=="score" else "")
        return _to_float(v) if key=="score" else str(v)
    scores.sort(key=k, reverse=reverse)

def calculate_average():
    return round(sum(_to_float(s.get("score",0)) for s in scores) / len(scores), 2) if scores else 0

def edit_score_data(cur_name, cur_game, new_name, new_game, new_score):
    for s in scores:
        if s.get("name")==cur_name and s.get("game")==cur_game:
            s["name"]=new_name
            s["game"]=new_game
            s["score"]=_to_float(new_score)
            return True
    return False

def get_scores():
    return list(scores)
