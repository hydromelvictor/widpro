#!/usr/bin/env python3
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from .category import category
from .product import product
from ..utils.const import UPLOAD_FOLDER
from dotenv import load_dotenv

import os


load_dotenv()

app = Flask(__name__)

app.config.from_mapping(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    # 5MB max file size
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    ENV=os.environ.get('ENV'),
    DEBUG=True if os.environ.get('DEBUG') == 1 else False,
    FLASK_RUN_PORT=os.environ.get('FLASK_RUN_PORT'),
    FLASK_RUN_HOST=os.environ.get('FLASK_RUN_HOST'),
    FLASK_APP=os.environ.get('FLASK_APP'),
    JSONIFY_PRETTYPRINT_REGULAR=True
)

cors = CORS(app, resources={r"*": {"origins": "*"}})

app.register_blueprint(category, url_prefix='/categories')
app.register_blueprint(product, url_prefix='/products')


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({'error': err}), 404)


@app.errorhandler(400)
def bad_request(err):
    return make_response(jsonify({'error': err}), 400)


@app.errorhandler(401)
def unauthorized(err):
    return make_response(jsonify({'error': err}), 401)


@app.errorhandler(403)
def forbidden(err):
    return make_response(jsonify({'error': err}), 403)


@app.errorhandler(Exception)
def internal_server_error(err):
    return make_response(jsonify({'error': err}), 500)
