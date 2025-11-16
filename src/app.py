from flask import Flask, jsonify, request
from model import User
import json
import os

app = Flask(__name__)

def check_permissions(*args):
    def w1(f):
        def w2(*args, **kwargs):
            key = request.headers.get("X-Api-Key")
            if not key:
                return jsonify({"error": 401, "message": "unauthorized (api key missing)"}), 401
            for user in User.ALL:
                if user.key == key:
                    break
            else:
                return jsonify({"error": 401, "message": "unauthorized"}), 401
            request.user = user
            for needed in args:
                if not user.has_perm(needed):
                    return jsonify({"error": 403, "message": f"forbidden {needed}"}), 403
            return f(*args, **kwargs)
        w2.__name__ = f.__name__
        return w2
    return w1

@app.route("/")
def index():
    return "https://www.youtube.com/watch?v=3X-iqFRGqbc"

@app.route("/whoami")
@check_permissions()
def whoami():
    return jsonify(request.user.dump())

@app.route("/stats")
@check_permissions()
def stats():
    return jsonify({
        "checks": {
            "total": 12345,
            "german": 420,
            "banned": 69,
        },
        "cost": 1337,
    })

@app.route("/check/<username>")
@check_permissions()
def check(username):
    if username == "TheRat":
        return jsonify({
            "language": {
                "verdict": "english",
                "source": "llm",
                "reason": "Das Wort 'Rat' beschreibt den Inhalt dieses Moduls. Hihi :)",
            },
            "banned": False,
            "cooldown": 139,
            "guild": "BaaDz9",
        })
    elif username == "DieRatte":
        return jsonify({
            "language": {
                "verdict": "german",
                "source": "database",
                "reason": "Gesehen auf: deutscher-server.mc:25565",
            },
            "banned": False,
            "cooldown": 0,
            "guild": None,
        })
    elif username == "BoeserBube":
        return jsonify({
            "language": {
                "verdict": "german",
                "source": "database",
                "reason": "Verifiziert auf GooDz-Discord",
            },
            "banned": True,
            "cooldown": 0,
            "guild": None,
        })
    elif username == "arrayen":
        return jsonify({
            "language": {
                "verdict": "unknown",
                "source": "database",
                "reason": "Manueller Eintrag (Blacklist)",
            },
            "banned": False,
            "cooldown": 0,
            "guild": "GooDz4",
        })
    else:
        return jsonify({
            "error": 404,
            "message": "Spieler nicht gefunden",
        }), 404

def create_runtime():
    User.load_users()
    print(f"[GDA] Loaded {len(User.ALL)} users")
    print("[GDA] Runtime created")
