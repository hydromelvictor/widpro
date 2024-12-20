from ..models.category import Category
from flask import Blueprint, request, jsonify, make_response, abort


category = Blueprint('category', __name__)


@category.route('/', methods=['POST'], strict_slashes=False)
def createCategory():
    if not request.get_json():
        abort(400, 'Invalid JSON')

    data = request.get_json()
    try:
        instance = Category.create(**data)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Category created successfully'
            }), 201)
    except Exception as e:
        abort(500, str(e))


@category.route('/<string:key>', methods=['GET'], strict_slashes=False)
def getCategory(key):
    try:
        instance = Category.get(id=key)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Category found'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@category.route('/', methods=['GET'], strict_slashes=False)
def getCategories():
    try:
        instance = Category.get()
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Categories found'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@category.route('/<string:key>', methods=['PUT'], strict_slashes=False)
def updateCategory(key):
    if not request.get_json():
        abort(400, 'Invalid JSON')

    data = request.get_json()
    try:
        instance = Category.update(id=key, **data)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Category updated successfully'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@category.route('/<string:key>', methods=['DELETE'], strict_slashes=False)
def deleteCategory(key):
    try:
        instance = Category.delete(id=key)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Category deleted successfully'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@category.route('/count', methods=['GET'], strict_slashes=False)
def countCategory():
    try:
        instance = Category.count()
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Categories counted successfully'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@category.route(
    '/<string:key>/attributes', methods=['POST'], strict_slashes=False)
def createAttributes(key):
    if not request.get_json():
        abort(400, 'Invalid JSON')

    if 'name' not in request.get_json():
        abort(400, 'Name is required')

    data = request.get_json()
    try:
        instance = Category.addAttributes(id=key, **data)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Attribute created successfully'
            }), 201)
    except Exception as e:
        abort(500, str(e))


@category.route(
    '/<string:key>/attributes/<string:name>',
    methods=['PUT'], strict_slashes=False
    )
def updateAttributes(key, name):
    if not request.get_json():
        abort(400, 'Invalid JSON')

    data = request.get_json()
    try:
        instance = Category.updateAttributes(id=key, name=name, **data)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Attribute updated successfully'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))


@category.route(
    '/<string:key>/attributes/<string:name>',
    methods=['DELETE'], strict_slashes=False
    )
def deleteAttributes(key, name):
    try:
        instance = Category.deleteAttrs(id=key, name=name)
        return make_response(jsonify(
            {
                'store': instance,
                'msg': 'Attribute deleted successfully'
            }
            ), 200)
    except Exception as e:
        abort(500, str(e))
