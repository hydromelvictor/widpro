#!/usr/bin/env python3
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from .category import category
from ..utils.const import UPLOAD_FOLDER

app = Flask(__name__)

app.config.from_mapping(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    # 16MB max file size
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    SECRET_KEY='secret',
    JSONIFY_PRETTYPRINT_REGULAR=True
)

cors = CORS(app, resources={r"*": {"origins": "*"}})

app.register_blueprint(category, url_prefix='/categories')


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
