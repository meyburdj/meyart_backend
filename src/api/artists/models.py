from src import db

class Artist(db.Model):
    __tablename__='artists'

    id=db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String,
        index=True,
        unique=True,
        nullable=False
    )

    details = db.Column(
        db.String,
        unique=False,
        nullable=True
    )

    artworks = db.relationship('Artwork', backref='artist', lazy=True)

    def __init__(self, name, details):
        self.name=name
        self.details=details