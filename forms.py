from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    """Form for registering user"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    email = StringField("email", validators=[Email()])
    first_name = StringField("first_name", validators=[InputRequired()])
    last_name = StringField("last_name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logining in user"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for submitting feedback"""

    title = StringField("title", validators=[InputRequired()])
    content = StringField("content", validators=[InputRequired()])