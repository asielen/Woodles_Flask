import csv

from flask.ext.admin import BaseView, expose

import system as syt
from app import db
from app.models import Card


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


if __name__ == "__main__":
    test_card_import()
