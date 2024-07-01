#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(400)
def bad_request(error):
    """400 Error
    ---
    responses:
      400:
        description: a bad request was made
    """
    return make_response(jsonify({'error': str(error.description)}), 400)


@app.errorhandler(409)
def conflicting_resource(error):
    """409 Error
    ---
    responsers:
        409:
        description:resources already existed
    """
    return make_response(jsonify({'error': str(error.description)}), 409)


@app.errorhandler(500)
def server_error(error):
    """ 500 Error
    ---
    responses:
        500:
        description: internal error occured on server side 
    """
    return jsonify({'error': 'Internal Server Error'}), 500


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


app.config['SWAGGER'] = {'title': 'SpendSmart Restful API', 'uiversion': 3}

Swagger(app)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('SPENDSMART_API_HOST')
    port = environ.get('SPENDSMART_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5002'
    app.run(host=host, port=port, threaded=True, debug=True)
