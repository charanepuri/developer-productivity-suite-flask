from datetime import datetime, timezone

from app.extensions import db


class Tool(db.Model):

    __tablename__ = "tools"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    slug = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
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

    category = db.relationship(
        "Category",
        back_populates="tools"
    )

    favorites = db.relationship(
        "Favorite",
        back_populates="tool",
        cascade="all, delete-orphan"
    )

    search_history = db.relationship(
        "SearchHistory",
        back_populates="tool",
        cascade="all, delete-orphan"
    )

    saved_results = db.relationship(
        "SavedResult",
        back_populates="tool",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tool {self.name}>"