from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    """Form for registering user"""

    username = StringField("username", validators=[InputRequired()])
    password = StringField("password", validators=[InputRequired()])
    email = StringField("email", validators=[Email()])
    first_name = StringField("first_name", validators=[InputRequired()])
    last_name = StringField("last_name", validators=[InputRequired()])

