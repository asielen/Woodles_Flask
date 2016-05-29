from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    letter = db.Column(db.String(1))
    card = db.relationship("Card", back_populates="questions")
    question_text = db.Column(db.String(128), unique=True)
    answer_text = db.Column(db.String(64))
    question_type_id = db.Column(db.Integer, db.ForeignKey('question_types.id'))
    question_type = db.relationship("Question_Type", back_populates="questions")
    question_category_id = db.Column(db.Integer, db.ForeignKey('question_categories.id'))
    question_category = db.relationship("Question_Category", back_populates="questions")

    @hybrid_property
    def id_string(self):
        return str(self.question_type)[0] + self.letter + str(self.id).rjust(6, "0") + "Q"

    @id_string.expression
    def id_string(cls):
        return func.concat(func.concat(
            func.concat(func.left(
                db.engine.execute(
                    db.select([Question_Type.type_name]).where(Question_Type.id == cls.question_type_id)).fetchone()[0],
                1), cls.letter),
            func.right(func.concat('000000', cls.id), 6)), "Q")

    def __init__(self, question_text, answer_text, letter, question_type, question_category):
        # self.card = card
        self.question_text = question_text
        self.answer_text = answer_text
        self.letter = letter
        self.question_type = Question_Type.query.filter_by(type_name=question_type).first()
        if self.question_type is None:
            ct = Question_Type(type_name=question_type)
            self.question_type = ct
        self.question_category = Question_Category.query.filter_by(category_name=question_category).first()
        if self.question_category is None:
            cc = Question_Category(category_name=question_category)
            self.question_category = cc

    def __repr__(self):
        return 'Question [ID {} <{} {}> = {}] - {} : {}'.format(self.id, self.question_type, self.question_category,
                                                                self.id_string, self.question_text, self.answer_text)


class Question_Type(db.Model):
    """
        type:
            Purple / Orange / Custom
    """
    __tablename__ = 'question_types'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(32))
    questions = db.relationship('Question', back_populates="question_type")

    def __repr__(self):
        return self.type_name


class Question_Category(db.Model):
    """
        type: starter / standard
    """
    __tablename__ = 'question_categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(32))
    questions = db.relationship('Question', back_populates="question_category")

    def __repr__(self):
        return self.category_name


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    game_card_id = db.Column(db.Integer, unique=True)
    letter = db.Column(db.String(1))
    card_type_id = db.Column(db.Integer, db.ForeignKey('card_types.id'))
    card_type = db.relationship('Card_Type', back_populates="cards")

    card_category_id = db.Column(db.Integer, db.ForeignKey('card_categories.id'))
    card_category = db.relationship('Card_Category', back_populates="cards")

    starter_question = db.relationship('Question', back_populates='card')
    questions = db.relationship('Question', back_populates='card')

    @hybrid_property
    def id_string(self):
        return str(self.card_type)[0] + self.letter + str(self.id).rjust(6, "0") + "C"

    @id_string.expression
    def id_string(cls):
        return func.concat(func.concat(
            func.concat(func.left(
                db.engine.execute(
                    db.select([Card_Type.type_name]).where(Card_Type.id == cls.card_type_id)).fetchone()[0], 1),
                cls.letter),
            func.right(func.concat('000000', cls.id), 6)), "C")

    def __init__(self, letter, card_type, card_category, questions):
        self.letter = letter
        ct = Card_Type.query.filter_by(type_name=card_type).first()
        if ct is None:
            ct = Card_Type(type_name=card_type)
        self.card_type = ct
        cc = Card_Category.query.filter_by(category_name=card_category).first()
        if cc is None:
            cc = Card_Category(category_name=card_category)
        self.card_category = cc
        for question in questions:
            self.questions.append(
                Question(question["question"], question["answer"], self.letter, card_type, card_category))

    def __repr__(self):
        return 'Card [ID {} <{} {}> = {}] - {}'.format(self.id, self.card_type, self.card_category, self.id_string,
                                                       self.letter)


class Card_Type(db.Model):
    """
        type:
            Purple / Orange / Custom
    """
    __tablename__ = 'card_types'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(32))
    cards = db.relationship('Card', back_populates="card_type")

    def __repr__(self):
        return self.type_name


class Card_Category(db.Model):
    __tablename__ = 'card_categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(32))
    cards = db.relationship('Card', back_populates="card_category")

    def __repr__(self):
        return self.category_name


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    feedback_text = db.Column(db.String(512))
    card_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean())

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
        """All users are active"""
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        """return True if the user is logged in"""
        return self.authenticated

    def is_anonymous(self):
        """Always False, not ananymous users"""
        return False
