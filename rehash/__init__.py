from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
# from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
login_manager = LoginManager()
db = SQLAlchemy(app)
# db.init_app(app)
# migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 469
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from rehash import routes