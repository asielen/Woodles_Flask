from flask import abort, render_template, redirect, url_for, request, flash, session
from app import app, db
from flask.ext.admin import Admin, BaseView, expose

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


