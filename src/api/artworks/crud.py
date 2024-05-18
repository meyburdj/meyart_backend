# artworks/crud.py
from sqlalchemy.exc import IntegrityError
from src import db
from .models import Artwork
from sqlalchemy.orm import load_only
from sqlalchemy.orm import joinedload
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
    return Artwork.query.options(joinedload(Artwork.artist)).get(artwork_id)


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
    query = db.session.query(Artwork)
    
    # Dynamically add filters to the query
    for key, value in filters.items():
        if hasattr(Artwork, key):
            query = query.filter(getattr(Artwork, key) == value)
    
    # Dynamically set only the requested columns if attributes are specified
    if attributes:
        selected_columns = [getattr(Artwork, attr) for attr in attributes if hasattr(Artwork, attr)]
        query = db.session.query(*selected_columns)
        for key, value in filters.items():
            if hasattr(Artwork, key):
                query = query.filter(getattr(Artwork, key) == value)

    # Execute the query and fetch results
    artworks = query.all()

    return artworks



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
