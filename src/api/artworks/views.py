from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from src.api.artworks.crud import (read_artworks_with_filter, create_artwork, 
read_all_artworks, read_artwork, read_related_artworks)

artworks_namespace = Namespace('artworks')

# Define the Artwork model for serialization
artwork_model = artworks_namespace.model('Artwork', {
    'id': fields.Integer(description='The unique identifier of an artwork'),
    'url': fields.String(required=True, description='URL of the artwork'),
    'title': fields.String(required=True, description='Title of the artwork'),
    'media': fields.String(description='Media used in the artwork'),
    'size': fields.String(description='Size of the artwork'),
    'date': fields.Integer(description='Date when the artwork was produced'),
    'price': fields.Float(description='Price of the artwork'),
    'genre': fields.String(description='Genre of the artwork'),
    'quantity': fields.Integer(description='Available quantity of the artwork'),
    'information': fields.String(description='Additional information about the artwork'),
    'artist_id': fields.Integer(required=True, description='ID of the artist who created the artwork'),
    'artist_name': fields.String(description='Name of the artist')
})

class Artwork(Resource):
    @artworks_namespace.marshal_with(artwork_model)
    def get(self, id):
        artwork = read_artwork(id)
        if artwork:
            return artwork, 200
        else:
            artworks_namespace.abort(404, f"Artwork with id {id} not found")

class ArtworkList(Resource):
    @artworks_namespace.marshal_list_with(artwork_model)
    def get(self):
        """Returns artworks. If query parameters are provided, filters based on those parameters. Otherwise, returns all artworks."""
        query_params = request.args.to_dict()
        attributes = query_params.pop('attributes', None)

        # Check for the 'attributes' parameter
        if attributes:
            attribute_keys = attributes.split(',')
        else:
            attribute_keys = ['id', 'url', 'date', 'title', 'media', 'size', 'price', 'genre', 'quantity', 'information', 'artist_id', 'artist_name']

        # Determine if query parameters are present
        if query_params:
            filtered_artworks = read_artworks_with_filter(query_params, attribute_keys)
            return filtered_artworks, 200
        else:
            filtered_artworks = read_artworks_with_filter({}, attribute_keys)
            return filtered_artworks, 200

    @artworks_namespace.expect(artwork_model, validate=True)
    @artworks_namespace.marshal_with(artwork_model, code=201)
    def post(self):
        """Creates a new artwork."""
        data = request.get_json()
        try:
            artwork = create_artwork(**data)
            return artwork, 201
        except ValueError as e:
            artworks_namespace.abort(400, str(e))
        except Exception as e:
            artworks_namespace.abort(500, str(e))

class ArtworkListRelated(Resource):
    @artworks_namespace.marshal_list_with(artwork_model)
    def get(self, id):
        """Returns artworks that are related to a single artwork. Related artworks
         first pull from same artist, then same genre, then randomly select."""
        
        related_artworks = read_related_artworks(id)
        print('related_artworks', related_artworks[0])
        return related_artworks, 200

artworks_namespace.add_resource(Artwork, '/<int:id>')
artworks_namespace.add_resource(ArtworkList, '/')
artworks_namespace.add_resource(ArtworkListRelated, '/<int:id>/related')

