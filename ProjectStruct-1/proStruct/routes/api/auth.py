from proStruct.routes.api import api_bp


@api_bp.route('/auth')
def auth():
    return '<h1>api.auth.auth</h1>'
