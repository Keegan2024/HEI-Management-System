from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
username = StringField('Username', validators=[DataRequired()])
password = PasswordField('Password', validators=[DataRequired()])
submit = SubmitField('Login')


class ChildForm(FlaskForm):
mother_name = StringField('Mother Name', validators=[DataRequired()])
art_number = StringField('ART Number', validators=[Optional()])
village = StringField('Village', validators=[Optional()])
child_name = StringField('Child Name', validators=[DataRequired()])
dob = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
submit = SubmitField('Register Child')
