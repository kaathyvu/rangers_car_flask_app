from flask import Flask
from .site.routes import site
from .authentication.routes import auth
from config import Config
from flask_migrate import Migrate
from .models import db as root_db, login_manager

app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(auth)

app.config.from_object(Config)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'