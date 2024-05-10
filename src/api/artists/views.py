from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from src.api.artists.crud import create_artist, read_artist, read_all_artists, update_artist, delete_artist

artists_namespace = Namespace('artists')

artist_model = artists_namespace.model('Artist', {
    'name': fields.String(required=True, description='Name of the artist'),
    'details': fields.String(description='Details about the artist')
})

artist_input_model = artists_namespace.model('ArtistInput', {
    'name': fields.String(required=True, description='Name of the artist'),
    'details': fields.String(description='Details about the artist')
})

class ArtistList(Resource):
    @artists_namespace.marshal_list_with(artist_model)
    def get(self):
        """Returns all artists."""
        artists = read_all_artists()
        return artists

    @artists_namespace.expect(artist_input_model, validate=True)
    @artists_namespace.marshal_with(artist_model, code=201)
    def post(self):
        """Creates a new artist."""
        data = request.get_json()
        try:
            artist = create_artist(name=data['name'], details=data.get('details'))
            return artist, 201
        except ValueError as e:
            artists_namespace.abort(400, str(e))

class ArtistResource(Resource):
    @artists_namespace.marshal_with(artist_model)
    def get(self, artist_id):
        """Returns a single artist by their ID."""
        artist = read_artist(artist_id)
        if artist is not None:
            return artist
        artists_namespace.abort(404, "Artist not found")

    @artists_namespace.expect(artist_input_model, validate=True)
    @artists_namespace.marshal_with(artist_model)
    def put(self, artist_id):
        """Updates an artist's information."""
        data = request.get_json()
        try:
            artist = update_artist(artist_id, name=data.get('name'), details=data.get('details'))
            return artist
        except ValueError as e:
            artists_namespace.abort(404, str(e))

    @artists_namespace.response(200, 'Artist deleted')
    def delete(self, artist_id):
        """Deletes an artist."""
        try:
            message = delete_artist(artist_id)
            return {"message": message}
        except ValueError as e:
            artists_namespace.abort(404, str(e))
        

# Adding resources to the namespace
artists_namespace.add_resource(ArtistList, '/')
artists_namespace.add_resource(ArtistResource, '/<int:artist_id>')
