from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, BooleanField, DecimalField, FileField, IntegerField, HiddenField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, Required
from wtforms import ValidationError

class LoginForm(FlaskForm):
    username = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login_submit = SubmitField("Log In")

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    register_submit = SubmitField("Sign Up")

class ProjectFileForm(FlaskForm):
    subject = SelectField("Subject", choices = [("", ""), ("Chemistry", "Chemistry"), ("Energy and Transport","Energy and Transport"), ("Food Technology","Food Technology"),
    ("Food Technology","Food Technology"), ("Engineering","Engineering"), ("Technology","Technology"), ("Enviromental Science","Enviromental Science"), ("Biology and Biotechnology","Biology and Biotechnology")])
    file = FileField("Upload File")

class SelectSubjectForm(FlaskForm):
    subject = SelectField("Subject", choices = [("", ""), ("Chemistry", "Chemistry"), ("Energy and Transport","Energy and Transport"), ("Food Technology","Food Technology"),
    ("Food Technology","Food Technology"), ("Engineering","Engineering"), ("Technology","Technology"), ("Enviromental Science","Enviromental Science"), ("Biology and Biotechnology","Biology and Biotechnology")])
    subject_submit = SubmitField("Choose Subject")

class AddScoresForm(FlaskForm):
    score = DecimalField("Score", validators=[DataRequired()])
    score_submit = SubmitField("Add Score")
    project_id = HiddenField("ID", validators=[DataRequired()])
