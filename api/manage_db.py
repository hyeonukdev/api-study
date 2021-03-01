from flask      import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
import bcrypt
import jwt
from datetime   import datetime, timedelta

## Default JSON encoder는 set를 JSON으로 변환할 수 없다.
## 그럼으로 커스텀 엔코더를 작성해서 set을 list로 변환하여
## JSON으로 변환 가능하게 해주어야 한다.
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

def get_user(user_id):
    user = current_app.database.execute(text("""
        SELECT 
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """), {
        'user_id' : user_id 
    }).fetchone()

    return {
        'id'      : user['id'],
        'name'    : user['name'],
        'email'   : user['email'],
        'profile' : user['profile']
    } if user else None

def get_user_id_and_password(email):
    row = current_app.database.execute(text("""    
        SELECT
            id,
            hashed_password
        FROM users
        WHERE email = :email
    """), {'email' : email}).fetchone()

    return {
        'id'              : row['id'],
        'hashed_password' : row['hashed_password']
    } if row else None

def insert_user(user):
    return current_app.database.execute(text("""
        INSERT INTO users (
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :name,
            :email,
            :profile,
            :password
        )
    """), user).lastrowid

def insert_tweet(user_tweet):
    return current_app.database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet).rowcount

def insert_follow(user_follow):
    return current_app.database.execute(text("""
        INSERT INTO users_follow_list (   
            user_id,
            follow_user_id
        ) VALUES (
            :id,
            :follow
        )
    """), user_follow).rowcount

def insert_unfollow(user_unfollow):
    return current_app.database.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow
    """), user_unfollow).rowcount

def get_timeline(user_id):
    timeline = current_app.database.execute(text("""
        SELECT 
            t.user_id,
            t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
        WHERE t.user_id = :user_id 
        OR t.user_id = ufl.follow_user_id
    """), {
        'user_id' : user_id 
    }).fetchall()

    return [{
        'user_id' : tweet['user_id'],
        'tweet'   : tweet['tweet']
    } for tweet in timeline]
