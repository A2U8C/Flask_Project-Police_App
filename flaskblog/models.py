from datetime import datetime
from flaskblog import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    complainants = db.relationship('Complaint', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complainant = db.Column(db.String(100), nullable=False)
    compph = db.Column(db.String, nullable=False)   
    victim=db.Column(db.String, nullable=False)
    victph=db.Column(db.String, nullable=False)
    doc=db.Column(db.String,nullable=False)
    accused=db.Column(db.String,nullable=False)
    description=db.Column(db.Text,nullable=False)
    sections=db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    compadd=db.Column(db.String,nullable=False)
    victadd=db.Column(db.String,nullable=False)
    def __repr__(self):
         return f"Complaint('{self.user_id}', '{self.complainant}')"

