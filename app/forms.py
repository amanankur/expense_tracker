__author__ = 'amanankur'

from flask.ext.wtf import Form
from wtforms import StringField, TextField, SubmitField,BooleanField, TextAreaField, SelectField, PasswordField, validators, ValidationError
from wtforms.validators import DataRequired, Length
from .models import User



class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class AddExpenseForm(Form):
    description = StringField('description')
    type = StringField('type')
    price = StringField('price')
    account_type = SelectField(u'Account Name List')
    acc_name = StringField('acc_name')
    currency = SelectField(u'Currency List')
    key = TextField("key")
    fields = SelectField(u'fields')
    submit = SubmitField("search")

class SignupForm(Form):
    nickname = TextField("User name")
    email = TextField("Email")
    password = PasswordField('Password')
    submit = SubmitField("Create account")

class SigninForm(Form):
    email = TextField("Email")
    password = PasswordField('Password')
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)

    def validate(self):

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            return False



