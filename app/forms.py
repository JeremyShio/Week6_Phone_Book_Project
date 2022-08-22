from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import InputRequired, EqualTo


class SignUpForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired()])
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField()


class LogInForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField()


class ContactForm(FlaskForm):
    firstname = StringField('First Name', validators = [InputRequired()])
    lastname = StringField('Last Name', validators = [InputRequired()])
    phone = StringField('Phone Number', validators = [InputRequired()])
    address = StringField('Home Address')
    email = StringField('Email Address')
    relationship = StringField('Relationship')
    other = StringField('Other')
    submit = SubmitField()
