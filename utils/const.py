import path


BASEDIR = path.dirname(path.abspath(__file__))
UPLOAD_FOLDER = path.join(BASEDIR, 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
