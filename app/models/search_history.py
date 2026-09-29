from datetime import datetime, timezone

from app.extensions import db


class SearchHistory(db.Model):

    __tablename__ = "search_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    tool_id = db.Column(
        db.Integer,
        db.ForeignKey("tools.id"),
        nullable=True
    )

    search_query = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship(
        "User",
        back_populates="search_history"
    )

    tool = db.relationship(
        "Tool",
        back_populates="search_history"
    )

    def __repr__(self):
        return f"<SearchHistory {self.search_query}>"