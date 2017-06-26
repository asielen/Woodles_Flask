from urllib.parse import parse_qs

from flask import url_for, render_template, request
from flask.ext.login import login_required
from werkzeug.utils import redirect

from app import app
from app.forms import QuestionFeedback, CardFeedback, FeedbackForm
from app.models import Question, Card


@app.route('/submit-feedback', methods=['Get', 'Post'])  # ?card= &question=
def submit_feedback():
    query_string = parse_qs(request.query_string)
    current_card = current_question = None
    if b'question' in query_string:
        current_question = Question.query.filter(
            Question.id_string == str(query_string[b'question'][0], encoding='utf-8')).first()
    if b'card' in query_string:
        current_card = Card.query.filter(Card.id_string == str(query_string[b'card'][0], encoding='utf-8')).first()
    if current_question is not None:
        form = QuestionFeedback(csrf_enabled=False, obj=current_question, question_id=current_question.id)
    elif current_card is not None:
        form = CardFeedback(csrf_enabled=False, obj=current_card)
    else:
        form = FeedbackForm(csrf_enabled=False)

    # Form submit
    if form.validate_on_submit():
        if current_card is not None:
            return redirect('/thanks-for-feedback?card={}'.format(current_card.id_string))
        else:
            return redirect(url_for('index'))

    return render_template('feedback-template.html', form=form, card=current_card, question=current_question)


@app.route('/thanks-for-feedback')  # ?card=
def thanks_feedback():
    query_string = parse_qs(request.query_string)
    current_card = None
    if b'card' in query_string:
        current_card = Card.query.filter(Card.id_string == str(query_string[b'card'][0], encoding='utf-8')).first()
    return render_template('feedback-thanks-template.html', card=current_card)


# @app.route('/sign-up', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#
#     if form.validate_on_submit():
#         newuser = User(email=form.email.data, password=form.password.data)
#         db.session.add(newuser)
#         db.session.commit()
#         login_user(newuser)
#         return redirect(url_for("import_cards"))
#
#     return render_template('signup-template.html', form=form)


@app.route('/import-cards')
@login_required
def import_cards():
    return render_template('<p>Secret Page</p>')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first_or_404()
#         if user.is_correct_password(form.password.data):
#             user.authenticated = True
#             db.session.add(user)
#             db.session.commit()
#             login_user(user, remember=True)
#             print("Successfull Login")
#             return redirect(url_for('index'))
#         else:
#             return redirect(url_for('login'))
#
#     return render_template('signup-template.html', form=form)
#
#
# @app.route('/logout', methods=["GET"])
# @login_required
# def logout():
#     # user = current_user
#     user.authenticated = False
#     db.session.add(user)
#     db.session.commit()
#     logout_user()
#     return redirect(url_for('index'))
#
#
# @app.login_manager.user_loader
# def user_loader(userid):
#     return app.models.User.get(userid).first()
