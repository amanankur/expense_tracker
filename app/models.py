__author__ = 'amanankur'
from app import db
from werkzeug import generate_password_hash, check_password_hash

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acc_name = db.Column(db.String(64), index=True, unique=True)
    expenses = db.relationship('Expense', backref = 'acc', lazy ='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Account %r>' % (self.acc_name)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(140))
    price = db.Column(db.Integer)
    type = db.Column(db.String)
    acc_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return '<Expense %r>' % (self.description)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pwdhash = db.Column(db.String(54))
    accounts = db.relationship('Account', backref = 'user_name', lazy ='dynamic')

    def __init__(self, nickname, email, password):
        self.nickname = nickname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


    def __repr__(self):
        return '<User %r>' % (self.nickname)

