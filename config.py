import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://app:1qazxsw23edc@127.0.0.1:3306/woodles"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY  = 'EE$yqYfWQWsK5g*Fnu5^4!XQ5bg^z9j!A7$W845QNv&9rHmvXASkVj*dWtXG'