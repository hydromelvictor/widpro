from ..models.category import Category
from flask import Blueprint, request, jsonify, make_response, abort


category = Blueprint('category', __name__)


@category.route('/', methods=['POST'], strict_slashes=False)
def createCategory():
    if not request.get_json():
        abort(400, 'Invalid JSON')

    if 'name' not in request.get_json():
        abort(400, 'Name is required')

    data = request.get_json()
    instance = Category.create(**data)
    return make_response(jsonify(
        {
            'store': instance,
            'msg': 'Category created successfully'
        }), 201)


@category.route('/<string:key>', methods=['GET'], strict_slashes=False)
def getCategory(key):
    try:
        instance = Category.findOne(key)
        return make_response(jsonify(instance), 200)
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, str(e))


@category.route('/', methods=['GET'], strict_slashes=False)
def getCategories():
    try:
        instance = Category.find()
        return make_response(jsonify(instance), 200)
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, str(e))


@category.route('/<string:key>', methods=['PUT'], strict_slashes=False)
def updateCategory(key):
    if not request.get_json():
        abort(400, 'Invalid JSON')

    data = request.get_json()
    try:
        instance = Category.update(key, **data)
        return make_response(jsonify(instance), 200)
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, str(e))


@category.route('/<string:key>', methods=['DELETE'], strict_slashes=False)
def deleteCategory(key):
    try:
        instance = Category.delete(key)
        return make_response(jsonify(instance), 200)
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, str(e))


@category.route(
    '<string:key>/attribute', methods=['POST'], strict_slashes=False)
def createAttribute(key):
    if not request.get_json():
        abort(400, 'Invalid JSON')

    if 'name' not in request.get_json():
        abort(400, 'Name is required')

    data = request.get_json()
    try:
        instance = Category.createAttribute(key, **data)
        return make_response(jsonify(instance), 201)
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, str(e))


@category.route(
    '/<string:key>/attribute/<string:attr>',
    methods=['PUT'], strict_slashes=False)
def updateAttribute(key, attr):
    if not request.get_json():
        abort(400, 'Invalid JSON')

    data = request.get_json()
    try:
        instance = Category.updateAttribute(key, attr, **data)
        return make_response(jsonify(instance), 200)
    except ValueError as e:
        abort(404, str(e))

    except Exception as e:
        abort(500, str(e))
