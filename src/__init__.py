# import os

# from flask import Flask
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# # from src.utils.flask_admin.admin import init_admin
# from flask_admin.contrib.sqla import ModelView
# from flask_admin import Admin

# db = SQLAlchemy()
# cors = CORS()

# def create_app(config=None, script_info=None):
#     # instantiate the app
#     app = Flask(__name__)

#     # set config
#     if config:
#         app.config.from_object(config)
#     else:
#         app_settings = os.getenv("APP_SETTINGS")
#         app.config.from_object(app_settings)

#         database_url = os.getenv('DATABASE_URL')
#         if database_url is not None and database_url.startswith("postgres://"):
#             database_url = database_url.replace(
#                 "postgres://", "postgresql://", 1)
#         app.config['SQLALCHEMY_DATABASE_URI'] = database_url

#     # set up extensions
#     db.init_app(app)
#     cors.init_app(app, resources={r"*": {"origins": "*"}})

#     # Flask-Admin setup
#     # init_admin(app)
#     admin = Admin(app, name='Meyart Gallery Admin', template_mode='bootstrap3')

    
#     # Import models here to avoid circular imports
#     from src.api.artists.models import Artist
#     from src.api.artworks.models import Artwork

#     # Add administrative views here
#     admin.add_view(ModelView(Artist, db.session))
#     admin.add_view(ModelView(Artwork, db.session))
#     # register api
#     from src.api import api
#     api.init_app(app)

#     # shell context for flask cli
#     @app.shell_context_processor
#     def ctx():
#         return {"app": app, "db": db}

#     return app




import os
from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
from src.utils.flask_admin.input_form import ArtworkForm

db = SQLAlchemy()
from src.api.artworks.models import Artwork
from src.api.artists.models import Artist

cors = CORS()


class ArtworkAdmin(ModelView):
    form = ArtworkForm  # Use the custom form

    column_list = ['title', 'artist_name', 'artist_id',  'media', 'size', 'price', 'genre', 'information', 'quantity', 'date',  'url']
    column_sortable_list = ['title', 'media', 'size', 'price', 'genre', 'quantity', 'date', 'artist_id']

    def allowed_file(self, filename):
        """Check if the uploaded file is allowed based on its extension."""
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def on_model_change(self, form, model, is_created):
        """Handle file upload and update the model's URL field."""
        if 'file' in request.files:
            file = request.files['file']
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Save the file locally; you can extend this to upload to S3
                file_path = os.path.join('static/uploads', filename)
                file.save(file_path)
                # Update the model's URL field to point to the file's location
                model.url = f"/static/uploads/{filename}"
            elif not is_created:
                # If no new file is uploaded, keep the existing URL
                model.url = Artwork.query.get(model.id).url

    def create_form(self, obj=None):
        form = super(ArtworkAdmin, self).create_form(obj)
        form.artist_id.choices = [(artist.id, artist.name) for artist in Artist.query.all()]
        return form

    def edit_form(self, obj=None):
        form = super(ArtworkAdmin, self).edit_form(obj)
        form.artist_id.choices = [(artist.id, artist.name) for artist in Artist.query.all()]
        return form

def init_admin(app):
    """Initialize the Flask-Admin interface."""
    admin = Admin(app, name='Meyart Gallery Admin', template_mode='bootstrap3')

    from src.api.artists.models import Artist
    from src.api.artworks.models import Artwork

    # Add views for Artist and Artwork models
    admin.add_view(ModelView(Artist, db.session))
    admin.add_view(ArtworkAdmin(Artwork, db.session))
    
def create_app(config=None, script_info=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if config:
        app.config.from_object(config)
    else:
        app_settings = os.getenv("APP_SETTINGS")
        app.config.from_object(app_settings)

        database_url = os.getenv('DATABASE_URL')
        if database_url is not None and database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})

    # Initialize Flask-Admin
    init_admin(app)

    # Register API
    from src.api import api
    api.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
