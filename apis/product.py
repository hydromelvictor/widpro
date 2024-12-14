from ..models.product import Product
from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    abort,
    send_from_directory
)
from werkzeug.utils import secure_filename
from ..utils.utils import allowed_file
from ..utils.const import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


product = Blueprint('product', __name__)


@product.route('/', methods=['POST'], strict_slashes=False)
def createProduct():
    if not request.get_json():
        abort(400, 'Invalid JSON')

    if 'name' not in request.get_json():
        abort(400, 'Name is required')

    data = request.get_json()
    if 'image' in request.files:
        abort(400, 'Image is required')

    image = request.files['image']
    if image.filename == '':
        abort(400, 'Image is required')

    if image and allowed_file(image.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(image.filename)
        image.save(f'{UPLOAD_FOLDER}/{filename}')
        data['image'] = send_from_directory(UPLOAD_FOLDER, filename)
    instance = Product.create(**data)
    return make_response(jsonify(
        {
            'store': instance,
            'msg': 'Product created successfully'
        }), 201)
