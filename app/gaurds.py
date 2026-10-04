from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def block_demo(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if current_user.is_demo:
            flash("The Demo account is read-only. Register to try it yourself.")
            return redirect(url_for("index"))

        return view(*args, **kwargs)

    return wrapped_view