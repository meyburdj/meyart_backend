from src import db
from src.api.artists.models import Artist
from sqlalchemy.ext.hybrid import hybrid_property


class Artwork(db.Model):
    __tablename__="artworks"

    id=db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    url = db.Column(
        db.String,
        unique=True,
        nullable=False
    )

    title = db.Column(
        db.String,
        unique=True,
        nullable=False
    )

    media = db.Column(
        db.String,
        unique=False,
        nullable=True
    )

    size = db.Column(
        db.String,
        unique=False,
        nullable=True
    )

    price = db.Column(
        db.Numeric,
        unique=False,
        nullable=True
    )

    genre = db.Column(
        db.String,
        unique=False,
        nullable=False,
        default='Misc'
    )

    information = db.Column(
        db.String,
        unique=False,
        nullable=True,
    )

    quantity = db.Column(
        db.Integer,
        unique=False,
        nullable=False,
        default=1
    )

    date=db.Column(
        db.Integer
    )

    artist_id=db.Column(
        db.Integer,
        db.ForeignKey('artists.id'),
        nullable=False
    )

    @property
    def artist_name(self):
        artist = Artist.query.get(self.artist_id)
        return artist.name if artist else 'Unknown'

    def __init__(self, url, title, media, size, price, genre, quantity, information, artist_id, date):
        self.url=url
        self.title=title
        self.media=media
        self.size=size
        self.price=price
        self.genre=genre
        self.quantity=quantity
        self.information=information
        self.artist_id=artist_id
        self.date=date



