
import csv
import os

from flask import flash, request, redirect, url_for
# from flask.ext.admin import BaseView, expose
# from flask_admin.contrib.sqla import filters
# from wtforms import validators
from flask.ext.security import login_required, current_user
from flask_admin.contrib import sqla
from werkzeug.utils import secure_filename

import system as syt
from app import app, admin, db
from app.models import Question, Question_Type, Card, Card_Category, Card_Type, Feedback, Session, User

admin.add_view(sqla.ModelView(Question, db.session))
admin.add_view(sqla.ModelView(Question_Type, db.session))
admin.add_view(sqla.ModelView(Card, db.session))
admin.add_view(sqla.ModelView(Card_Type, db.session))
admin.add_view(sqla.ModelView(Card_Category, db.session))
admin.add_view(sqla.ModelView(Feedback, db.session))
admin.add_view(sqla.ModelView(Session, db.session))
#admin.add_view(sqla.ModelView(Session_Player, db.session))
admin.add_view(sqla.ModelView(User, db.session))

class UserAdmin(sqla.ModelView):
    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)
    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True
    def is_accessible(self):
        return current_user.has_role('admin')

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/import', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('admin.index'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def import_card_csv(csv_file):
    if csv_file is not None and csv_file != 0:
        with open(csv_file, newline='', encoding='utf-8') as cf:
            creader = csv.reader(cf)
            header = 0

            for row in creader:
                if header == 0:
                    header = 1
                    continue
                questions = []
                questions.append({"question": row[3], "answer": row[4], "starter_question":True})
                for q, a in pairwise(row[5:]):
                    questions.append({"question": q, "answer": a, "starter_question":False})
                new_card = Card(game_card_id=row[0], card_type=row[1], letter=row[2],
                                questions=questions, card_category="original")
                db.session.add(new_card)
            db.session.commit()


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def test_card_import():
    csv_dir = './card_files/'

    def _load(file):
        return syt.make_dir('{}{}'.format(csv_dir, file))

    choices = syt.Load_Menu.find_saveFiles(csv_dir, '.csv')
    csv_file = syt.Load_Menu(name="- Load csv file -", function=_load, choices=choices).run()
    print(csv_file)
    import_card_csv(csv_file)


if __name__ == "__main__":
    test_card_import()
