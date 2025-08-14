scores = []

def _to_float(x):
    try: return float(x)
    except Exception: return 0.0

def add_score_data(name, game, score):
    scores.append({"name": name, "game": game, "score": _to_float(score)})

def delete_score_by_name(name, game=None):
    global scores
    name = name.strip()
    if game:
        g = game.strip()
        scores = [s for s in scores if not (s.get("name")==name and s.get("game")==g)]
    else:
        scores = [s for s in scores if s.get("name") != name]

def _key_fn(key):
    return (lambda s: _to_float(s.get("score", 0))) if key=="score" else (lambda s: str(s.get(key,"")))

def sort_scores_by_key(key, reverse=False):
    if key in {"name","game","score"}:
        scores.sort(key=_key_fn(key), reverse=reverse)

def get_sorted_scores(key, reverse=False):
    if key not in {"name","game","score"}:
        return get_scores()
    return sorted(get_scores(), key=_key_fn(key), reverse=reverse)

def calculate_average():
    return round(sum(_to_float(s.get("score",0)) for s in scores)/len(scores), 2) if scores else 0

def edit_score_data(cur_name, cur_game, new_name=None, new_game=None, new_score=None):
    for s in scores:
        if s.get("name")==cur_name and s.get("game")==cur_game:
            if new_name: s["name"]=new_name
            if new_game: s["game"]=new_game
            if new_score is not None: s["score"]=_to_float(new_score)
            return True
    return False

def get_scores():
    return list(scores)