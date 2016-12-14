from flask.ext.wtf import Form
from wtforms import HiddenField, TextAreaField, StringField, PasswordField, validators, SubmitField

from .models import User


class FeedbackForm(Form):
    feedback = TextAreaField('feedback')


class CardFeedback(FeedbackForm):
    card_id = HiddenField('card_id')
    letter = StringField('letter')


class QuestionFeedback(CardFeedback):
    question_id = HiddenField('question_id')
    question_text = TextAreaField('question_text')
    answer_text = TextAreaField('answer_text')

#Todo, add card form


class SignupForm(Form):
    email = StringField("Email", [validators.DataRequired("Please enter your email address."),
                                  validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True

class LoginForm(Form):
    email = StringField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField("Login")