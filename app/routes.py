import csv
import datetime
import flask
import io
import os
import tempfile

from app import the_app
from app import forms
from src.traverse_word2vec import Oracle, OracularError


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
    language_eng = flask.request.form['language']
    language = forms.language_code_for(language_eng)
    first = flask.request.form['origin_word']
    last = flask.request.form['destiny_word']
    model_file = os.path.join(
            the_app.static_folder, 'word2vec_models', f'{language}.bin')
    try:
        the_oracle = Oracle.from_binary(model_file)
        terms = the_oracle.traverse(first, last)
        error_message = None
    except OracularError as e:
        terms = []
        error_message = e.args[0]
    return flask.render_template(
            'pronouncement.html', language=language, terms=terms,
            error_message=error_message)


@the_app.route('/oracle/synonyms/<language>/<term>', methods=['GET'])
def synonyms(language, term):
    model_file = os.path.join(
            the_app.static_folder, 'word2vec_models', f'{language}.bin')
    try:
        the_oracle = Oracle.from_binary(model_file)
        synonyms = the_oracle.synonyms_for(term)
        error_message = None
    except OracularError as e:
        synonyms = []
        error_message = e.args[0]
    return flask.render_template(
            'synonyms.html', language=language, term=term, synonyms=synonyms,
            error_message=error_message)


@the_app.route('/oracle', methods=['GET', 'POST'])
def oracle():
    form = forms.DivinatoryForm()
    if form.validate_on_submit():
        return _get_oracular_pronouncement()
    else:
        return flask.render_template('oracle.html', form=form)
