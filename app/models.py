from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(1))
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    question_text = db.Column(db.String(128), unique=True)
    answer_text = db.Column(db.String(64))
    question_type_id = db.Column(db.Integer, db.ForeignKey('question_types.id'))
    question_type = db.relationship("Question_Type", back_populates="questions")
    starter_question = db.Column(db.BOOLEAN)

    @hybrid_property
    def id_string(self):
        return str(self.question_type)[0] + self.letter + str(self.id).rjust(6, "0") + "Q"

    @id_string.expression
    def id_string(cls):
        return func.concat(func.concat(
            func.concat(func.left(
                    db.select([Question_Type.type_name]).where(Question_Type.id == cls.question_type_id).limit(1).as_scalar(),
                1), cls.letter),
            func.right(func.concat('000000', cls.id), 6)), "Q")

    def __init__(self, question_text, answer_text, letter, question_type, starter_question=False):
        self.question_text = question_text
        self.answer_text = answer_text
        self.letter = letter
        self.question_type = Question_Type.query.filter_by(type_name=question_type).first()
        if self.question_type is None:
            ct = Question_Type(type_name=question_type)
            self.question_type = ct
        self.starter_question = starter_question

    def __repr__(self):
        return 'Question [ID {} <{} {}> = {}] - {} : {}'.format(self.id, self.question_type, self.starter_question,
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


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    game_card_id = db.Column(db.Integer, unique=True)
    letter = db.Column(db.String(1))
    card_type_id = db.Column(db.Integer, db.ForeignKey('card_types.id'))
    card_type = db.relationship('Card_Type', back_populates="cards")

    card_category_id = db.Column(db.Integer, db.ForeignKey('card_categories.id'))
    card_category = db.relationship('Card_Category', back_populates="cards")

    starter_question = db.relationship('Question', uselist=False, primaryjoin="and_(Card.id==Question.card_id,Question.starter_question==True)")
    standard_questions = db.relationship('Question', primaryjoin="and_(Card.id==Question.card_id,Question.starter_question==False)")

    questions = db.relationship('Question')


    @hybrid_property
    def id_string(self):
        return str(self.card_type)[0] + self.letter + str(self.id).rjust(6, "0") + "C"

    @id_string.expression
    def id_string(cls):
        """ IN SQL:
        SELECT CONCAT(CONCAT(CONCAT(LEFT((SELECT card_types.type_name FROM card_types WHERE card_types.id = cards.card_type_id),1),letter),RIGHT(CONCAT('000000',cards.id),6)),"C") as nid FROM cards;
        """
        return func.concat(func.concat(
            func.concat(func.left(
                    db.select([Card_Type.type_name]).where(Card_Type.id == cls.card_type_id).limit(1).as_scalar(), 1),
                cls.letter),
            func.right(func.concat('000000', cls.id), 6)), "C")


    def __init__(self, letter, card_type, card_category, questions, game_card_id=None):
        self.letter = letter
        ct = Card_Type.query.filter_by(type_name=card_type).first()
        if ct is None:
            ct = Card_Type(type_name=card_type)
        self.card_type = ct
        cc = Card_Category.query.filter_by(category_name=card_category).first()
        if cc is None:
            cc = Card_Category(category_name=card_category)
        self.card_category = cc
        # self.starter_question = Question(starter_question["question"], starter_question["answer"], self.letter, card_type, starter_question=True)
        for question in questions:
            self.questions.append(
                Question(question["question"], question["answer"], self.letter, card_type, question["starter_question"]))
        self.game_card_id = game_card_id

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
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    card = db.relationship("Card", backref="feedback", foreign_keys=[card_id])
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship("Question", backref="feedback", foreign_keys=[question_id])
    feedback_letter = db.Column(db.String(1))
    feedback_question = db.Column(db.String(256))
    feedback_answer = db.Column(db.String(256))
    feedback_comments = db.Column(db.String(512))



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
        """Always False, not anonymous users"""
        return False
