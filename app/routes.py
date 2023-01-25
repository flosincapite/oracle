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
from src.confused_predictive_model import model as confused_model
from src.confused_predictive_model import textnorm


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
            error_message=error_message,
            back_link="/oracle",
            back_link_message="Consult the Oracle Again")


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
        return flask.render_template(
                'oracle.html', form=form, page_title="LANGUAGE GARBAGE ORACLE",
                persona_name="THE ORACLE")


def _ebru_file(color, shape):
    return flask.url_for('static', filename=f'ebru_{color}_{shape}.png')


_EBRU_COLORS = ['blue', 'pink']
def _random_color():
    return random.choice(_EBRU_COLORS)


@the_app.route('/proverb', methods=['GET', 'POST'])
def proverb():
    button = _ebru_file(_random_color(), 'circle')
    return flask.render_template(
            'proverb.html', button=button, endpoint='/proverb/result')


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
            button=button, endpoint='/proverb')


@the_app.route('/proverb/result', methods=['GET', 'POST'])
def proverb_result():
    return _get_proverb_result()


def _get_poetic_confusion():
    the_text = flask.request.form['corpus']
    synonyms = flask.request.form['synonyms']
    synonym_sets = [
            set([token.strip().lower() for token in synonym.split(',')])
            for synonym in synonyms.split(';')
            if synonym.strip()]
    sentences = []
    number_sentences = int(flask.request.form.get('number_sentences', '5'))
    number_sentences = max(number_sentences, 1)
    try:
        corpus = textnorm.generate_normalized_sentences(the_text.strip())
        model = confused_model.Model.from_sentence_generator(
                corpus, synonym_sets)
        for _ in range(number_sentences):
            sentences.append(' '.join(model.generate_sentence()[2:]))
        error_message = None
    except confused_model.VaticError as e:
        terms = []
        error_message = e.args[0]

    return flask.render_template(
            'babbling.html', sentences=sentences, error_message=error_message,
            back_link="/confused-poet",
            back_link_message="Consult the Confused Poet Again")


@the_app.route('/confused-poet', methods=['GET', 'POST'])
def confused_poet():
    form = forms.ConfusedPoetForm()
    if form.validate_on_submit():
        return _get_poetic_confusion()
    else:
        return flask.render_template(
                'confused-poet.html', form=form,
                page_title="CONFUSED POET", persona_name="THE CONFUSED POET")
