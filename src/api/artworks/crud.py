# artworks/crud.py
from sqlalchemy.exc import IntegrityError
from src import db
from .models import Artwork
from sqlalchemy.orm import load_only
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func
from ..artists.models import Artist


def create_artwork(url, title, media, size, price, genre, quantity, information, artist_id):
    """Create a new artwork."""
    try:
        artwork = Artwork(
            url=url,
            title=title,
            media=media,
            size=size,
            price=price,
            genre=genre,
            quantity=quantity,
            information=information,
            artist_id=artist_id
        )
        db.session.add(artwork)
        db.session.commit()
        return artwork
    except IntegrityError:
        db.session.rollback()
        raise ValueError(f"Artwork with the title '{title}' or URL '{url}' already exists.")


def read_all_artworks():
    """Retrieve all artworks from the database."""
    return Artwork.query.options(joinedload(Artwork.artist)).all()


def read_artwork(artwork_id):
    """Retrieve a specific artwork by its ID."""
    artwork = db.session.query(
        Artwork.id,
        Artwork.url,
        Artwork.title,
        Artwork.media,
        Artwork.size,
        Artwork.price,
        Artwork.genre,
        Artwork.quantity,
        Artwork.information,
        Artwork.artist_id,
        Artwork.date,
        Artist.name.label('artist_name')
    ).join(Artist).filter(Artwork.id == artwork_id).first()

    return artwork



def read_artworks_with_filter(filters, attributes):
    """
    Retrieves artworks based on filtering criteria and specified attributes.
    
    :param filters: Dictionary with filtering criteria 
        (e.g., {'genre': 'Cubism', 'price': 500}).
    :param attributes: List of attributes to include in the returned dictionaries 
        (e.g., ['id', 'url', 'title', 'media', 'price']).
    :return: List of dictionaries containing specified attributes of artworks 
    that match the filtering criteria.
    """
    # Start constructing the query
    query = db.session.query(Artwork).join(Artist)
    print('im ')
    # Dynamically add filters to the query
    for key, value in filters.items():
        if hasattr(Artwork, key):
            if isinstance(value, str) and ',' in value:
                # If the value is a comma-separated string, split it into a list
                values = value.split(',')
                query = query.filter(getattr(Artwork, key).in_(values))
            else:
                query = query.filter(getattr(Artwork, key) == value)
    
    # Dynamically set only the requested columns if attributes are specified
    if attributes:
        selected_columns = []
        for attr in attributes:
            if attr == 'artist_name':
                selected_columns.append(Artist.name.label('artist_name'))
            elif hasattr(Artwork, attr):
                selected_columns.append(getattr(Artwork, attr))

        query = query.with_entities(*selected_columns)

    # Execute the query and fetch results
    artworks = query.all()

    return artworks

def read_related_artworks(artwork_id):
    """
    Retrieves three related artworks based on the artist and genre of the given artwork.
    If there are fewer than three artworks by the same artist, fill the remaining spots with artworks from the same genre.
    If there are still fewer than three artworks, fill the remaining spots with random artworks.
    """

    artwork = read_artwork(artwork_id)
    if not artwork:
        return []

    related_artworks = []

    base_query = db.session.query(
        Artwork.id,
        Artwork.url,
        Artwork.title,
        Artwork.media,
        Artwork.price,
        Artwork.genre,
        Artwork.artist_id,
        Artwork.date,
        Artist.name.label('artist_name')
    ).join(Artist)

    # Find other artworks by the same artist
    artist_artworks = base_query.filter(
        Artwork.artist_id == artwork.artist_id, Artwork.id != artwork_id).limit(3).all()
    related_artworks.extend(artist_artworks)

    # If fewer than 3, find artworks by the same genre
    if len(related_artworks) < 3:
        genre_artworks = base_query.filter(
            Artwork.genre == artwork.genre, Artwork.id != artwork_id, Artwork.artist_id != artwork.artist_id).limit(3 - len(related_artworks)).all()
        related_artworks.extend(genre_artworks)

    # If still fewer than 3, fill with random artworks
    if len(related_artworks) < 3:
        random_artworks = base_query.filter(
            Artwork.id != artwork_id, Artwork.artist_id != artwork.artist_id).order_by(func.random()).limit(3 - len(related_artworks)).all()
        related_artworks.extend(random_artworks)

    return related_artworks



def update_artwork(artwork_id, **kwargs):
    """Update an existing artwork's information."""
    artwork = Artwork.query.get(artwork_id)
    if not artwork:
        raise ValueError(f"No artwork found with ID: {artwork_id}")

    # Update fields dynamically from kwargs
    for key, value in kwargs.items():
        if hasattr(artwork, key):
            setattr(artwork, key, value)

    db.session.commit()
    return artwork


def delete_artwork(artwork_id):
    """Delete an artwork from the database."""
    artwork = Artwork.query.get(artwork_id)
    if not artwork:
        raise ValueError(f"No artwork found with ID: {artwork_id}")

    db.session.delete(artwork)
    db.session.commit()
    return f"Artwork with ID {artwork_id} has been deleted."
