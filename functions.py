scores = []

def add_score_data(name, game, score):
    scores.append({"name": name, "game": game, "score": float(score)})

def delete_score_by_name(name):
    global scores
    scores = [s for s in scores if s["name"] != name]

def sort_scores_by_key(key):
    reverse = key == "score"
    if key in ["name", "game", "score"]:
        scores.sort(key=lambda x: x[key], reverse=reverse)

def calculate_average():
    return sum(s["score"] for s in scores) / len(scores) if scores else 0

def edit_score_data(cur_name, cur_game, new_name, new_game, new_score):
    for s in scores:
        if s["name"] == cur_name and s["game"] == cur_game:
            s.update({"name": new_name, "game": new_game, "score": float(new_score)})
            break

def get_scores():
    return scores