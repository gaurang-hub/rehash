from rehash import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    occupation = db.Column(db.String(60), nullable=False)
    countFiles = db.Column(db.Integer, default=0)
    files = db.relationship('UserFiles', backref='User', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}') "

class UserFiles(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filePath = db.Column(db.String(120), nullable=False)