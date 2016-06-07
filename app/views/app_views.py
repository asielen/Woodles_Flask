from flask import render_template, redirect, url_for
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
    return render_template('card-template.html', card=current_card)

# Game Views
@app.route('/id/<string:card_id>')
def card_id(card_id):
    current_card = Card.query.get(card_id)
    return redirect(url_for('card', card_id=current_card.id_string))


@app.route('/c/random')
def random_card():
    # rand = random.randrange(1, Card.query.count())
    row = Card.query.order_by(func.random()).first()
    return redirect(url_for('card', card_id=row.id_string))


if __name__ == '__main__':
    app.run()
