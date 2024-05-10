# artist/crud.py
from sqlalchemy.exc import IntegrityError
from src import db
from .models import Artist


def create_artist(name, details=None):
    """Create a new artist."""
    try:
        artist = Artist(name=name, details=details)
        db.session.add(artist)
        db.session.commit()
        return artist
    except IntegrityError:
        db.session.rollback()
        raise ValueError(f"Artist with the name '{name}' already exists.")


def read_all_artists():
    """Retrieve all artists from the database."""
    return Artist.query.all()


def read_artist(artist_id):
    """Retrieve a specific artist by their ID."""
    return Artist.query.get(artist_id)


def update_artist(artist_id, name=None, details=None):
    """Update an existing artist's information."""
    artist = Artist.query.get(artist_id)
    if not artist:
        raise ValueError(f"No artist found with ID: {artist_id}")

    if name:
        artist.name = name
    if details:
        artist.details = details

    db.session.commit()
    return artist


def delete_artist(artist_id):
    """Delete an artist from the database."""
    artist = Artist.query.get(artist_id)
    if not artist:
        raise ValueError(f"No artist found with ID: {artist_id}")

    db.session.delete(artist)
    db.session.commit()
    return f"Artist with ID {artist_id} has been deleted."
