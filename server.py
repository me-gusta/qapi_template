from os import urandom

import jinja2
from flask import Flask
# from flask_login import LoginManager
from flask_cors import CORS
from flask_wtf import CSRFProtect
from website.qapi.queries import clear_cache
from website.export.load_from_dump import import_entities

app = Flask(__name__)
app.secret_key = urandom(12).hex()

cors = CORS(app)

csrf = CSRFProtect()
csrf.init_app(app)

try:
    from debug import DEBUG
except ImportError:
    import_entities()


from website.routes import *
from website.admin_routes import *