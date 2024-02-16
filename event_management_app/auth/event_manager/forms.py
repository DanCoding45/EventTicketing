


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class EventManagerRegistrationForm(FlaskForm):
    primary_host = StringField('Host Name', validators=[DataRequired()], render_kw={"class": "form-control"})
    host_email = StringField('Host email', validators=[DataRequired()], render_kw={"class": "form-control"})
    organization_name = StringField('Organization Name', validators=[DataRequired()], render_kw={"class": "form-control"})
    organization_address = StringField('Organization Address', validators=[DataRequired()], render_kw={"class": "form-control"})
    organization_email = StringField('Organization Email Address', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})
    
    
class EventManagerLoginForm(FlaskForm):
    organization_email = StringField('Organization Email Address', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})