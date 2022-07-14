import csv
import datetime
import flask
import io
import tempfile

from app import the_app
from app import forms
from src.traverse_word2vec import Oracle


@the_app.route('/', methods=['GET', 'POST'])
@the_app.route('/index', methods=['GET', 'POST'])
def index():
    return flask.render_template('index.html')


@the_app.route('/segwayad', methods=['GET', 'POST'])
def segwayad():
    return flask.render_template('segwayad.html')


@the_app.route('/sexrobot', methods=['GET', 'POST'])
def sexrobot():
    return flask.render_template('sexrobot.html')


def _get_oracular_pronouncement():
    # TODO: flask.send_file can accept a BytesIO, but that doesn't work with
    # uWSGI. Find a workaround. Writing a file here sucks.
    # TODO: Call word2vec here.
    pass


@the_app.route('/oracle', methods=['GET', 'POST'])
def oracle():
    form = forms.DivinatoryForm()
    if form.validate_on_submit():
        return _get_oracular_pronouncement()
    else:
        return flask.render_template('oracle.html', form=form)
