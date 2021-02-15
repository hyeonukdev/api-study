import os
from flask import Flask, jsonify, request 
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):  # 1
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.users = {}
app.id_count = 1
app.tweets = []
app.json_encoder = CustomJSONEncoder



@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


@app.route("/sign-up", methods=["POST"])  
def sign_up():
    new_user = request.json 
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1
    return jsonify(new_user) 


@app.route("/tweet", methods=["POST"])  
def tweet():
    payload = request.json
    user_id = int(payload["id"])
    tweet = payload["tweet"]

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400

    if len(tweet) > 300:
        return "300자를 초과했습니다", 400

    app.tweets.append({"user_id": user_id, "tweet": tweet})

    return "", 200

@app.route("/follow", methods=["POST"])
def follow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["follow"])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400

    user = app.users[user_id]
    user.setdefault("follow", set()).add(user_id_to_follow)

    return jsonify(user)

@app.route("/unfollow", methods=["POST"])  # 4
def unfollow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_unfollow = int(payload["unfollow"])

    if user_id not in app.users or user_id_to_unfollow not in app.users:
        return "사용자가 존재하지 않습니다", 400

    user = app.users[user_id]

    if not user.get("follow") or len(user.get("follow")) == 0:
        return "팔로우하고 있는 사용자가 없습니다", 400

    user.setdefault("follow", set()).discard(user_id_to_unfollow)

    return jsonify(user)