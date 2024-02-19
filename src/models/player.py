from . import db

class PlayerSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Text, unique=True, nullable=False)
    character_info = db.Column(db.Text, unique=True)