from flask import redirect
from flask_login import current_user

default_logged_in_view = '/honks'


def logout_required(route_func):
    def decorated_route_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(default_logged_in_view)
        return route_func(*args, **kwargs)
    decorated_route_func.__name__ = route_func.__name__
    return decorated_route_func
