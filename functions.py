import os, time
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

TABLE_NAME = os.getenv("TABLE_NAME", "game-scoreboard-scores")
REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION", "us-east-1")

_ddb = boto3.resource("dynamodb", region_name=REGION)
_table = _ddb.Table(TABLE_NAME)

def _to_decimal(x):
    try:
        return Decimal(str(float(x)))
    except Exception:
        return Decimal("0")

def _to_py(item):
    # ממיר Decimal ל-float בשביל ה-Jinja
    if "score" in item:
        try:
            item["score"] = float(item["score"])
        except Exception:
            item["score"] = 0.0
    return item

def add_score_data(name, game, score):
    _table.put_item(Item={
        "name": name, "game": game,
        "score": _to_decimal(score),
        "updated_at": int(time.time()*1000),
    })

def delete_score_by_name(name):
    # מוחק את כל המשחקים של אותו שם
    resp = _table.query(KeyConditionExpression=Key("name").eq(name))
    items = resp.get("Items", [])
    with _table.batch_writer() as bw:
        for it in items:
            bw.delete_item(Key={"name": it["name"], "game": it["game"]})

def edit_score_data(cur_name, cur_game, new_name, new_game, new_score):
    # אם מפתח השתנה – מחיקה ואז הוספה; אחרת Update
    if cur_name != new_name or cur_game != new_game:
        delete_item(cur_name, cur_game)
        add_score_data(new_name, new_game, new_score)
    else:
        _table.update_item(
            Key={"name": cur_name, "game": cur_game},
            UpdateExpression="SET #s=:s, updated_at=:t",
            ExpressionAttributeNames={"#s": "score"},
            ExpressionAttributeValues={":s": _to_decimal(new_score), ":t": int(time.time()*1000)}
        )

def delete_item(name, game):
    _table.delete_item(Key={"name": name, "game": game})

def get_scores(sort_key=None, order="asc"):
    resp = _table.scan()
    items = [_to_py(i) for i in resp.get("Items", [])]
    if sort_key in {"name", "game", "score"}:
        reverse = (order == "desc")
        # ליציבות: ממיינים בטוח גם כשחסרים שדות
        items.sort(key=lambda x: x.get(sort_key, 0 if sort_key=="score" else ""), reverse=reverse)
    return items
