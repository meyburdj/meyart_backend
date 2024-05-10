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
    # Create and commit the CatGroup to ensure it has an ID
    artist = Artist(
        name='Pablo Picasso'
    )
    db.session.add(artist)
    db.session.commit()

    # Now the artist has an ID, we can create works and reference it
    artworks = [
        Artwork(url='https://cdn.discordapp.com/attachments/1233394404681846784/1233394465876607107/file-3eA7SfA07SCszv41sFrmQi1X.png?ex=662cef9c&is=662b9e1c&hm=290860919dce31050289b0519a7b4bc0691bdb31ae619ef0a9ec0065b074bb65&', 
            genre='Cuban', price=500, media='sculpture', description="this is a work of art", artist=artist.id),
        Artwork(url='https://cdn.discordapp.com/attachments/1233394404681846784/1233394465876607107/file-3eA7SfA07SCszv41sFrmQi1X.png?ex=662cef9c&is=662b9e1c&hm=290860919dce31050289b0519a7b4bc0691bdb31ae619ef0a9ec0065b074bb65&', 
            genre='Cuban', price=500, media='sculpture', description="this is a work of art", artist=artist.id),
        Artwork(url='https://cdn.discordapp.com/attachments/1233394404681846784/1233394465876607107/file-3eA7SfA07SCszv41sFrmQi1X.png?ex=662cef9c&is=662b9e1c&hm=290860919dce31050289b0519a7b4bc0691bdb31ae619ef0a9ec0065b074bb65&', 
            genre='Cuban', price=500, media='sculpture', description="this is a work of art", artist=artist.id),
        Artwork(url='https://cdn.discordapp.com/attachments/1233394404681846784/1233394465876607107/file-3eA7SfA07SCszv41sFrmQi1X.png?ex=662cef9c&is=662b9e1c&hm=290860919dce31050289b0519a7b4bc0691bdb31ae619ef0a9ec0065b074bb65&', 
            genre='Cuban', price=500, media='sculpture', description="this is a work of art", artist=artist.id),
       
    ]
    db.session.add_all(artworks)
    db.session.commit()
    
    click.echo(f"Added artowrks to database under artist ID {artist.id}.")

if __name__ == "__main__":
    cli()
    app.run(threaded=True)

