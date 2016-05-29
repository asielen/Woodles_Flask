from getpass import win_getpass
import sys
from flask import current_app
from app import app, db
from app.models import User


def main():
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print("A user already exists, create another? (y/n)")
            create = input()
            if create == 'n':
                return

        email = input("Please enter an email address: ")

        password = win_getpass("Please enter a password: ")
        assert password == win_getpass('Password (again): ')

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        print('User added: {}').format(email)


if __name__ == '__main__':
    sys.exit(main())
