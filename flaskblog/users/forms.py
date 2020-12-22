
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user
from flaskblog.models import User
import email_validator




class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])

    email = StringField("Email", validators=[DataRequired(), Email() ])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8,max = 50)])
             
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        existing_username = User.query.filter_by(username = username.data).first()
        if existing_username:
            raise ValidationError("Username exists")

    def validate_email(self,email):
        existing_email = User.query.filter_by(email = email.data).first()
        if existing_email:
            raise ValidationError("Email belongs to another account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()] )

    password = PasswordField("Password", validators=[DataRequired()])
    
    remember = BooleanField("Remeber Me")

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])

    about = TextAreaField("About", validators=[DataRequired(), Length(min=1 ,max =300) ])

    picture = FileField("Update Profile Picture", validators = [FileAllowed(["jpg","png","jpeg","bmp"])])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if current_user.username != username.data:
            existing_username = User.query.filter_by(username = username.data).first()
            if existing_username:
                raise ValidationError("Username exists")

    def validate_email(self,email):
        if current_user.email != email.data:
            existing_email = User.query.filter_by(email = email.data).first()
            if existing_email:
                raise ValidationError("Email belongs to another account")

class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=50)])

    confirm_password = PasswordField("Confirim Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Change Password")


class RequestResetForm(FlaskForm):

    email = StringField("Email", validators = [DataRequired(), Email()])

    submit = SubmitField("Continue")

    def email_validator(self,email):
        existing_email = User.query.filter_by(email = email).first()

        if existing_email is None:
            raise ValidationError("Email doesn't belong to any account")