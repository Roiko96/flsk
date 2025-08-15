# functions.py

from typing import List, Dict, Optional

def _coerce_score(v) -> float:
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return 0.0

def sort_scores_by_key(data: List[Dict], key: str, reverse: bool = False) -> None:
    if key not in {"name", "game", "score"}:
        return
    if key == "score":
        data.sort(key=lambda x: _coerce_score(x.get("score", 0.0)), reverse=reverse)
    else:
        data.sort(key=lambda x: (x.get(key) or ""), reverse=reverse)

def add_score(data: List[Dict], name: str, game: str, score) -> None:
    data.append({"name": name.strip(), "game": game.strip(), "score": _coerce_score(score)})

def delete_score_by_name(data: List[Dict], name: str, game: Optional[str] = None) -> int:
    name = name.strip()
    game_key = game.strip() if isinstance(game, str) else None
    deleted = 0
    for i in range(len(data) - 1, -1, -1):
        row = data[i]
        if row.get("name") == name and (game_key is None or row.get("game") == game_key):
            data.pop(i)
            deleted += 1
    return deleted

def edit_score(data: List[Dict], current_name: str, current_game: str,
               new_name: Optional[str] = None, new_game: Optional[str] = None,
               new_score: Optional[str] = None) -> bool:
    idx = None
    for i, row in enumerate(data):
        if row.get("name") == current_name and row.get("game") == current_game:
            idx = i
            break
    if idx is None: return False
    if new_name: data[idx]["name"] = new_name.strip()
    if new_game: data[idx]["game"] = new_game.strip()
    if new_score and str(new_score).strip() != "": data[idx]["score"] = _coerce_score(new_score)
    return True

def calc_average(data: List[Dict]) -> float:
    if not data: return 0.0
    total = sum(_coerce_score(x.get("score", 0.0)) for x in data)
    return round(total / len(data), 2)
