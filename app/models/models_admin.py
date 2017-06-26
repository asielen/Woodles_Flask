from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from app import db


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    cards = db.Column(db.String(4096))
    num_cards = db.Column(db.Integer)
    num_players = db.Column(db.Integer)
    session_id = db.Column(db.String(32))

# class Session_Player(db.Model):
#     __tablename__ = 'session_players'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
#     session = db.relationship("Session", backref="session_players", foreign_keys=[session_id])
#     score = db.Column(db.Integer)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    card = db.relationship("Card", backref="feedback", foreign_keys=[card_id])
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship("Question", backref="feedback", foreign_keys=[question_id])
    feedback_letter = db.Column(db.String(1))
    feedback_question = db.Column(db.String(256))
    feedback_answer = db.Column(db.String(256))
    feedback_comments = db.Column(db.String(512))

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean())
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, email, password):
        self.email = email.lower()
        self.password = password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_correct_password(self, password):
        return check_password_hash(self._password, password)

    def is_active(self):
        """If password has been confirmed"""
        return self.active

    def get_id(self):
        return self.id

    def is_authenticated(self):
        """return True if the user is logged in"""
        return self.authenticated

    def is_anonymous(self):
        """Always False, not anonymous users"""
        return False

# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Executes before the first request is processed.
@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='moderator', description='Moderator')

    # Create two Users for testing purposes -- unless they already exists.
    encrypted_password = generate_password_hash('password')
    if not user_datastore.get_user('admin@woodles.com'):
        user_datastore.create_user(email='admin@woodles.com', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()