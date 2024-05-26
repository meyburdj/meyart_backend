import click
from flask import Flask
from flask.cli import FlaskGroup
from src import create_app, db
from src.api.artists.models import Artist
from src.api.artworks.models import Artwork

app = create_app()
cli = FlaskGroup(create_app=lambda: app)

@cli.command('recreate_db')
def recreate_db():
    """Drops and recreates the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Database recreated!")

@cli.command('seed_artists_and_works')
def seed_artists_and_works():
    """Seeds the database with artists and their works."""
    # Artists
    artist1 = Artist(name="Bearden, Romare")
    artist2 = Artist(name="Toby, Mark")
    artist3 = Artist(name="Steckel, Anita")
    artist4 = Artist(name="Youngerman, Jack")

    db.session.add_all([artist1, artist2, artist3, artist4])
    db.session.commit()

    # Artworks
    artworks = [
        Artwork(url="https://i.ibb.co/1dsq3Fg/sm-Bearden20220912-114438.jpg",
                title="Black Enterprise",
                media="print",
                size="100x100 cm",
                price=1200,
                genre="American",
                information="An important piece from the artist's later period.",
                quantity=1,
                date=1977,
                artist_id=artist1.id),
        Artwork(url="https://i.ibb.co/9sKWq10/med-Bearden-Dancer20220927-122720-1.jpg",
                title="European",
                media="painting",
                size="90x90 cm",
                price=1500,
                genre="Modernism",
                information="Captures the dynamic movement of a dancer.",
                quantity=1,
                date=1985,
                artist_id=artist1.id),
        Artwork(url="https://i.ibb.co/48PSfqt/med-Tobey-Grand-Parade.jpg",
                title="Grand Parade",
                media="sculpture",
                size="80x80 cm",
                price=1000,
                genre="Latin American",
                information="A vibrant and colorful abstraction.",
                quantity=1,
                date=105,
                artist_id=artist2.id),
        Artwork(url="https://i.ibb.co/sPn0tVm/med-Steckel20220919-142503-1.jpg",
                title="Giant Horse",
                media="mixed-media",
                size="200x200 cm",
                price=2000,
                genre="Asian",
                information="A massive sculpture dominating the space it occupies.",
                quantity=1,
                date=1032,
                artist_id=artist3.id),
        Artwork(url="https://i.ibb.co/vqzgwQs/med-Youngerman-galaxy-Apple-Green19-75-20221003-122224.jpg",
                title="Galaxy: Apple Green",
                media="photography",
                size="95x95 cm",
                price=1100,
                genre="Contemporary",
                information="An expressive piece evoking the cosmos.",
                quantity=1,
                date=2013,
                artist_id=artist4.id)
    ]

    db.session.add_all(artworks)
    db.session.commit()
    
    click.echo("Database seeded with initial artists and artworks.")

if __name__ == "__main__":
    cli()
    app.run(threaded=True)

