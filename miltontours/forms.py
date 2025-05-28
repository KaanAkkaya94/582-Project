from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, email, EqualTo
from wtforms.fields import SelectField  # Add this import

class CheckoutForm(FlaskForm):
    """Form for user checkout."""
    firstname = StringField("First Name", validators = [InputRequired()])
    surname = StringField("Surname", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired(), email()])
    phone = StringField("Contact Number", validators = [InputRequired()])
    submit = SubmitField("Send to Agent")

class NewCheckoutForm(FlaskForm):
    """Form for user checkout."""
    firstname = StringField("First Name", validators = [InputRequired()])
    surname = StringField("Surname", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired(), email()])
    phone = StringField("Contact Number", validators = [InputRequired()])
    address = StringField("Address", validators = [InputRequired()])
    city = StringField("City", validators = [InputRequired()])
    postcode = StringField("Postcode", validators = [InputRequired()])
    state = SelectField(
        " State",
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

    payment = SubmitField("Proceed to Checkout")


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[email()])
    firstname = StringField("Your first name", validators = [InputRequired()])
    surname = StringField("Your surname", validators = [InputRequired()])
    phone = StringField("Your phone number", validators = [InputRequired()])
    submit = SubmitField('Register')

class RegisterForm(FlaskForm):
    """Form for user checkout."""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    # confirm_password = PasswordField(
    #     'Confirm Password',
    #     validators=[InputRequired(), EqualTo('password', message='Passwords must be the same')]
    # )
    email = StringField("Your email", validators = [InputRequired(), email()])
    firstname = StringField("Your first name", validators = [InputRequired()])
    surname = StringField("Your surname", validators = [InputRequired()])
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
    submit = SubmitField('Register')


class orderCheckout(FlaskForm):
    """Form for user checkout."""
    paymentType = SelectField(
        "Select Payment Type",
        choices=[
            ("Debit/Credit"),
            ("Paypal"),
            ("Wise"),
            ("Bank Transfer")
           
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