from flask import Flask
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

admin = Admin(app, name='Woodles', template_mode='bootstrap3')
mail = Mail(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"



from app import views, models
