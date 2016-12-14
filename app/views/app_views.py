from flask import render_template, redirect, url_for, session
from sqlalchemy.sql import func

from app import app
from app.models import Card


@app.route('/')
def index():
    return render_template('index.html')

# Game Views
@app.route('/c/<string:card_id>')
def card(card_id):
    current_card = Card.query.filter(Card.id_string == card_id).first()
    if 'cards' in session:
        if card_id not in session['cards']:
            session['cards'] = session['cards']+","+card_id
    else:
        session['cards'] = card_id
    return render_template('card-template.html', card=current_card)

# Game Views
@app.route('/id/<string:card_id>')
def card_id(card_id):
    current_card = Card.query.get(card_id)
    return redirect(url_for('card', card_id=current_card.id_string))


@app.route('/c/random')
def random_card():
    row = None
    lu_try = 0
    CARDS_TO_TRY = 10 #number of random cards to try before giving up
    while not row and lu_try < CARDS_TO_TRY:
        lu_try += 1
        row = Card.query.order_by(func.random()).first()
        if 'cards' not in session or lu_try >= CARDS_TO_TRY: break
        if lu_try < 50 and row.id_string in session['cards']:
            row = None
    return redirect(url_for('card', card_id=row.id_string))


if __name__ == '__main__':
    app.run()
