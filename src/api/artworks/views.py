from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from src.api.artworks.crud import read_artworks_with_filter, create_artwork, get_all_artworks

artworks_namespace = Namespace('artworks')

# Define the Artwork model for serialization
artwork_model = artworks_namespace.model('Artwork', {
    'id': fields.Integer(description='The unique identifier of an artwork'),
    'url': fields.String(required=True, description='URL of the artwork'),
    'title': fields.String(required=True, description='Title of the artwork'),
    'media': fields.String(description='Media used in the artwork'),
    'size': fields.String(description='Size of the artwork'),
    'price': fields.Float(description='Price of the artwork'),
    'genre': fields.String(description='Genre of the artwork'),
    'quantity': fields.Integer(description='Available quantity of the artwork'),
    'information': fields.String(description='Additional information about the artwork'),
    'artist_id': fields.Integer(required=True, description='ID of the artist who created the artwork')
})

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
            attribute_keys = ['id', 'url', 'title', 'media', 'size', 'price', 'genre', 'quantity', 'information', 'artist_id']

        # Determine if query parameters are present
        if query_params:
            filtered_artworks = read_artworks_with_filter(query_params, attribute_keys)
            return filtered_artworks, 200
        else:
            all_artworks = get_all_artworks()
            return all_artworks, 200

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

artworks_namespace.add_resource(ArtworkList, '/')
