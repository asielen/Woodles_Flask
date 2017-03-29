import csv

import flask_admin as admin
from flask.ext.admin import BaseView, expose
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from wtforms import validators

import app
import system as syt
from app import db
from app.models import Card, User


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


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


# # Customized User model admin
# class UserAdmin(sqla.ModelView):
#     inline_models = (UserInfo,)


# Customized Post model admin
class PostAdmin(sqla.ModelView):
    # Visible columns in the list view
    column_exclude_list = ['text']

    # List of columns that can be sorted. For 'user' column, use User.username as
    # a column.
    column_sortable_list = ('title', ('user', 'user.username'), 'date')

    # Rename 'title' columns to 'Post Title' in list view
    column_labels = dict(title='Post Title')

    column_searchable_list = ('title', User.username, 'tags.name')

    column_filters = ('user',
                      'title',
                      'date',
                      'tags',
                      filters.FilterLike(Post.title, 'Fixed Title', options=(('test1', 'Test 1'), ('test2', 'Test 2'))))

    # Pass arguments to WTForms. In this case, change label for text field to
    # be 'Big Text' and add required() validator.
    form_args = dict(
                    text=dict(label='Big Text', validators=[validators.required()])
                )

    form_ajax_refs = {
        'user': {
            'fields': (User.username, User.email)
        },
        'tags': {
            'fields': (Tag.name,)
        }
    }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(PostAdmin, self).__init__(Post, session)


class TreeView(sqla.ModelView):
    form_excluded_columns = ['children', ]


# Create admin
admin = admin.Admin(app, name='Example: SQLAlchemy', template_mode='bootstrap3')

# Add views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(sqla.ModelView(Tag, db.session))
admin.add_view(PostAdmin(db.session))
admin.add_view(TreeView(Tree, db.session))

if __name__ == "__main__":
    test_card_import()
