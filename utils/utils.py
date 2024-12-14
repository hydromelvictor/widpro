def allowed_file(filename, exts):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in exts
