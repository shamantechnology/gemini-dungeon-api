from . import db
from sqlalchemy.sql import func

class PlayerSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Text, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<PlayerSession {self.session_id}>"