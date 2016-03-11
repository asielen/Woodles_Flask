from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/c/<int:card_id>')
def card(card_id):
    return 'Viewing Card: {}'.format(card_id)

@app.route('/c/random')
def card():
    return 'Random Card!: {}'.format('RANDOM')

if __name__ == '__main__':
    app.run()
