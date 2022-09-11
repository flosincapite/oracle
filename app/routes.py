import csv
import datetime
import flask
import io
import json
import os
import random
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


@the_app.route('/roemancer', methods=['GET', 'POST'])
def roemancer():
    return flask.render_template('roemancer.html')


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


def _ebru_file(color, shape):
    return flask.url_for('static', filename=f'ebru_{color}_{shape}.png')


_EBRU_COLORS = ['blue', 'pink']
def _random_color():
    return random.choice(_EBRU_COLORS)


@the_app.route('/proverb', methods=['GET', 'POST'])
def proverb():
    button = _ebru_file(_random_color(), 'circle')
    return flask.render_template('proverb.html', button=button)


_PROVERBS = []
with open(os.path.join(the_app.static_folder, 'proverbs.json'), 'r') as inp:
    proverbs = json.load(inp)
    for proverb in proverbs:
        _PROVERBS.append(proverb.split('\n'))


def _get_proverb_result():
    # Populate list of proverbs, but only once.
    proverb = random.choice(_PROVERBS)
    background = _ebru_file(_random_color(), 'rectangle')
    button = _ebru_file(_random_color(), 'circle')
    return flask.render_template(
            'one-proverb.html', lines=proverb, background=background,
            button=button)


@the_app.route('/proverb/result', methods=['GET', 'POST'])
def proverb_result():
    return _get_proverb_result()
