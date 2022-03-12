from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
# from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '968331509722a24aaca4a6ab62dea0cd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Gaurang1@localhost/rehashDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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