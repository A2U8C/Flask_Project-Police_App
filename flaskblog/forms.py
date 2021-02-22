from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flaskblog.models import User
from wtforms.fields.html5 import DateField
from wtforms import *
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ComplaintForm(FlaskForm):
    complainant=TextField('Complainant',validators=[DataRequired()])
    compph=TextField('Complainant\'s Phone No.',validators=[DataRequired()])
    victim=TextField('Victim',validators=[DataRequired()])
    victph=TextField('Victim\'s Phone No.',validators=[DataRequired()])
    doc=TextField("Date of Crime",validators=[DataRequired()])
    accused=TextField("Accused",validators=[DataRequired()])
    description=TextAreaField("Description",validators=[DataRequired()])
    sections=TextField("Sections of IPC",validators=[DataRequired()])
    compadd=TextField("Complainant\'s Address",validators=[DataRequired()])
    victadd=TextField("Victim\'s Address",validators=[DataRequired()])
    image=FileField(u"Evidence and Documents")
    register = SubmitField('Register')