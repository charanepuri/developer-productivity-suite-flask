from datetime import datetime, timezone

from app.extensions import db


class SavedResult(db.Model):

    __tablename__ = "saved_results"

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

    title = db.Column(
        db.String(150),
        nullable=False
    )

    input_data = db.Column(
        db.Text,
        nullable=True
    )

    result_data = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship(
        "User",
        back_populates="saved_results"
    )

    tool = db.relationship(
        "Tool",
        back_populates="saved_results"
    )

    def __repr__(self):
        return f"<SavedResult {self.title}>"