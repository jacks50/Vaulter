from flask import (Blueprint)

bp = Blueprint('vaulture', __name__, url_prefix='/vaulture')

@bp.get('/file/<filename>')
def vaulturefile_get(filename):
    pass

@bp.post('/file')
def vaulturefile_post():
    pass

@bp.put('/file')
def vaulturefile_create():
    pass

@bp.get('/admin')
def vaulturefile_admin():
    pass