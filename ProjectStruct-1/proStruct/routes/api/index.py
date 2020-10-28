from proStruct.routes.api import api_bp


@api_bp.route('/index')
def index():
    return '<h1>api.index.index</h1>'
