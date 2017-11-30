from flask import current_app, abort, g
from flask_login import current_user
from functools import wraps


def only_for_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not g.user.admin:
            return abort(404)
        return func(*args, **kwargs)
    return decorated_view

