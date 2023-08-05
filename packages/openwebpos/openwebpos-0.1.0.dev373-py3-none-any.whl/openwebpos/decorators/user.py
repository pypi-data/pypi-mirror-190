from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


# Decorator to check if user has role
def role_required(*role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('route.login'))
            if current_user.role.name not in role:
                # TODO: ADD custom error page for unauthorized users.
                return redirect(url_for('route.login'))
            # if not current_user.has_role(role):
            #     return redirect(url_for('route.index'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Decorator to check if role has permission
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('route.login'))
            if not current_user.role.has_permission(permission):
                return redirect(url_for('route.index'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
