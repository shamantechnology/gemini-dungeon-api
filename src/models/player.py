from . import db
from sqlalchemy.sql import func

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # add user id when user model and login is created
    first_name = db.Column(db.String(512), nullable=False)
    last_name = db.Column(db.String(512), nullable=False)
    char_class = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(40), nullable=False)
    alignment = db.Column(db.String(2), nullable=False, default="LG")
    level = db.Column(db.Integer, nullable=False, default=1)
    hit_points = db.Column(db.Integer, nullable=False, default=5)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False, default=18)
    gender = db.Column(db.String(8), nullable=False, default="Male")
    background = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Player {self.first_name} {self.last_name} [lvl {self.level}]>"

