from ..models.product import Product
from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    abort
)

product = Blueprint('product', __name__)


@product.route('/', methods=['POST'], strict_slashes=False)
def createProduct():
    if not request.get_json():
        abort(400, 'Invalid JSON')

    data = request.get_json()

    try:
        instance = Product.create(**data)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Product created successfully'
            }), 201)
    except Exception as e:
        abort(500, str(e))


@product.route('/<string:key>', methods=['GET'], strict_slashes=False)
def getProduct(key):
    try:
        instance = Product.get(id=key)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Product found'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@product.route('/', methods=['GET'], strict_slashes=False)
def getProducts():
    try:
        instance = Product.get()
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Products found'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@product.route('/<string:key>', methods=['PUT'], strict_slashes=False)
def updateProduct(key):
    if not request.get_json():
        abort(400, 'Invalid JSON')

    data = request.get_json()
    try:
        instance = Product.update(id=key, **data)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Product updated successfully'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@product.route('/<string:key>', methods=['DELETE'], strict_slashes=False)
def deleteProduct(key):
    try:
        instance = Product.delete(id=key)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Product deleted successfully'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@product.route('/count', methods=['GET'], strict_slashes=False)
def countProducts():
    try:
        instance = Product.count()
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Products count'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))
