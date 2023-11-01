from flask_login import UserMixin, LoginManager, current_user

from server import app

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, _id):
        self.id = _id


user = User('admin')

users = {}


@login_manager.user_loader
def load_user(_id: str):
    try:
        return users[_id]
    except KeyError:
        users[_id] = User(_id)
        return users[_id]


def is_authenticated():
    return current_user.__dict__.get('id') == 'admin'
