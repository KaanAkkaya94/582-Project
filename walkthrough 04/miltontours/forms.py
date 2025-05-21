from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, email, EqualTo
from wtforms.fields import SelectField  # Add this import

class CheckoutForm(FlaskForm):
    """Form for user checkout."""
    firstname = StringField("Your first name", validators = [InputRequired()])
    surname = StringField("Your surname", validators = [InputRequired()])
    email = StringField("Your email", validators = [InputRequired(), email()])
    phone = StringField("Your phone number", validators = [InputRequired()])
    submit = SubmitField("Send to Agent")

class NewCheckoutForm(FlaskForm):
    """Form for user checkout."""
    firstname = StringField("Your first name", validators = [InputRequired()])
    surname = StringField("Your surname", validators = [InputRequired()])
    email = StringField("Your email", validators = [InputRequired(), email()])
    phone = StringField("Your phone number", validators = [InputRequired()])
    address = StringField("Your address", validators = [InputRequired()])
    city = StringField("Your city", validators = [InputRequired()])
    postcode = StringField("Your postcode", validators = [InputRequired()])
    state = SelectField(
        "Your state",
        choices=[
            ("QLD", "Queensland"),
            ("NSW", "New South Wales"),
            ("VIC", "Victoria"),
            ("TAS", "Tasmania"),
            ("SA", "South Australia"),
            ("WA", "Western Australia"),
            ("NT", "Northern Territory"),
            ("ACT", "Australian Capital Territory"),
        ],
        validators=[InputRequired()],
    )
    delivery = SelectField(
        "Delivery method",
        choices=[
            ("Normal Delivery"),
            ("Express Delivery"),
            ("Eco Friendly Delivery"),
            ("Store Pickup"),
        ],
        validators=[InputRequired()],
    )
    payment = SubmitField("Pay Now")


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Form for user registry."""
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired(), email()])
    firstname = StringField("Your first name", validators = [InputRequired()])
    surname = StringField("Your surname", validators = [InputRequired()])
    phone = StringField("Your phone number", validators = [InputRequired()])
    submit = SubmitField("Make Account")

