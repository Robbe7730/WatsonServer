from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URI"]
secret = os.environ["WATSON_SECRET"]

db = SQLAlchemy(app)

class Frame(db.Model):
    id = db.Column('frame_id', db.String, primary_key = True)
    begin_at = db.Column('begin_at', db.DateTime, nullable = False)
    end_at = db.Column('end_at', db.DateTime, nullable = False)
    project = db.Column('project', db.String, nullable = False)
    tags = db.Column('tags', db.PickleType, nullable = False)
    created_at = db.Column(
        'created_at',
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    @classmethod
    def from_dict(cls, json_dict):
        ret = cls()
        ret.id = json_dict["id"]
        ret.begin_at = datetime.fromisoformat(json_dict["begin_at"])
        ret.end_at = datetime.fromisoformat(json_dict["end_at"])
        ret.project = json_dict["project"]
        ret.tags = json_dict["tags"]
        return ret

    def to_dict(self):
        ret = {}
        ret["id"] = self.id
        ret["begin_at"] = self.begin_at.isoformat()
        ret["end_at"] = self.end_at.isoformat()
        ret["project"] = self.project
        ret["tags"] = self.tags
        return ret

def check_auth():
    token = request.headers.get("Authorization", None)
    if token == f"Token {secret}":
        return True
    return False

@app.route("/frames/", methods=["GET"])
def send_frames():
    if not check_auth():
        return '{"error": "Invalid token"}', 401
    last_sync = datetime.fromisoformat(request.args.get("last_sync", ""))

    frames = db.session.query(Frame).filter(
        Frame.created_at >= last_sync
    ).all()

    return jsonify([f.to_dict() for f in frames])

@app.route("/frames/bulk/", methods=["POST"])
def receive_frames():
    frames = request.json

    for frame in frames:
        existing_frames = db.session.query(Frame).filter_by(id=frame['id'])

        for existing_frame in existing_frames:
            db.session.remove(existing_frame)
            db.session.commit()

        f = Frame.from_dict(frame)
        db.session.add(f)
    db.session.commit()

    return "", 201

if __name__ == '__main__':
    db.create_all()
    app.run("0.0.0.0", 8080)
