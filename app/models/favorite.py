from datetime import datetime, timezone

from app.extensions import db


class Favorite(db.Model):

    __tablename__ = "favorites"

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
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship(
        "User",
        back_populates="favorites"
    )

    tool = db.relationship(
        "Tool",
        back_populates="favorites"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "tool_id",
            name="unique_user_tool_favorite"
        ),
    )

    def __repr__(self):
        return (
            f"<Favorite user={self.user_id} "
            f"tool={self.tool_id}>"
        )