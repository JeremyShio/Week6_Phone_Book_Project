from app import db, login

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from config import AuthorSignature

author_info = AuthorSignature


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    contacts = db.relationship('Contact', backref = 'user', lazy = 'dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}> {author_info.alias} asking you, how's it going?! "

    def __str__(self):
        {'str_username': str(self.username),
        'str_email': str(self.email),
        'str_date_joined': str(self.date_created)}
        return f'''
Username: {self.str_username}
Email: {self.str_email}
Date Joined: {self.str_date_joined}
        '''
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(14), nullable = False, unique = True)
    address = db.Column(db.String(100), nullable = False)   # Can have people with the same address (E.g. family living in a home)
    email = db.Column(db.String(50), nullable = False, unique = True)
    relationship = db.Column(db.String(25), nullable = False)
    other = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"""
<Contact {self.id} | {self.firstname}>
Coding Apprentice here, reminding you that you're awesome!!
        """

    def __str__(self):
        {'str_contact_name': str(self.firstname) + str(self.lastname),
        'str_phone_number': str(self.phone),
        'str_address': str(self.address),
        'str_email': str(self.email),
        'str_relationship': str(self.relationship),
        'str_other': str(self.other)}
        return f'''
Contact Name: {self.str_contact_name}
Phone Number: {self.str_phone_number}
Address: {self.str_address}
Email: {self.str_email}
Relationship: {self.str_relationship}
Other: {self.str_other}
        '''

    def edit(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'firstname', 'lastname', 'phone', 'address', 'email', 'relationship', 'other'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()