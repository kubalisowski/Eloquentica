from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember')
    submit = SubmitField('submit')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('submit')

class SearchForm(FlaskForm):
    search = StringField('search', validators=[InputRequired()])
    submit = SubmitField('submit')

class AddForm(FlaskForm):
    word = StringField('word', validators=[InputRequired()])
    definition = StringField('definition', validators=[InputRequired()])
    synonym = StringField('synonym', validators=[InputRequired()])
    submit = SubmitField('submit')

class TestForm(FlaskForm):
    test = StringField('test')