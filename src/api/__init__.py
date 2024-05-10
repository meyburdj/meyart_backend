from flask_restx import Api

from src.api.ping import ping_namespace
from src.api.artworks.views import artworks_namespace
from src.api.artists.views import artists_namespace

api = Api(version="1.0", title="Users API", doc="/doc")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(artworks_namespace, path="/artworks")
api.add_namespace(artists_namespace, path="/artists")
