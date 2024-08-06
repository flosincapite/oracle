import csv
import datetime
import flask
import io
import json
import os
import random
import re
import tempfile

from app import the_app
from app import forms
from src.confused_predictive_model import model as confused_model
from src.confused_predictive_model import textnorm
from src.i18n import internationalize as _i18n
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


def _get_oracular_pronouncement(i18n_code):
    _i = lambda label: _i18n(i18n_code, label)
    # TODO: Add language selector back in (app/templates/oracle-en.html).
    language_eng = flask.request.form['language']
    language = forms.language_code_for(language_eng)
    model_file_name = f'{language}.bin'
    first = flask.request.form['origin_word']
    last = flask.request.form['destiny_word']
    # model_file_name = f'{i18n_code}.bin'
    model_file = os.path.join(
            the_app.static_folder, 'word2vec_models', model_file_name)
    try:
        the_oracle = Oracle.from_binary(model_file)
        terms = the_oracle.traverse(first, last)
        error_message = None
    except OracularError as e:
        terms = []
        error_message = e.args[0]
    return flask.render_template(
            'pronouncement.html',
            # language=language,
            i18n_code=i18n_code,
            language=i18n_code,
            terms=terms,
            error_message=error_message,
            oracle_walked_in_words=_i("ORACLE_WALKED_WORDS"),
            back_link=f"/{i18n_code}/oracle",
            back_link_message=_i("CONSULT_ORACLE_AGAIN"))


@the_app.route(
        '/<i18n_code>/oracle/synonyms/<language>/<term>', methods=['GET'])
def synonyms(i18n_code, language, term):
    _i = lambda label: _i18n(i18n_code, label)
    # TODO: Fix this hack; figure out why whole URL is included.
    # TODO: Consult app/templates/synonyms-en.html.
    if re.search(r'oracle', term):
        term = term.split('/')[-1]
    model_file = os.path.join(
            the_app.static_folder, 'word2vec_models', f'{language}.bin')
    try:
        the_oracle = Oracle.from_binary(model_file)
        the_synonyms = the_oracle.synonyms_for(term)
        error_message = None
    except OracularError as e:
        the_synonyms = []
        error_message = e.args[0]
    return flask.render_template(
            'synonyms.html',
            i18n_code=i18n_code,
            language=language,
            term=term,
            oracle_loiters=_i("ORACLE_LOITERS"),
            the_synonyms=the_synonyms,
            error_message=error_message)


@the_app.route('/<i18n_code>/oracle', methods=['GET', 'POST'])
def oracle(i18n_code):
    # TODO: Add language selector back in (app/templates/oracle-en.html).
    _i = lambda label: _i18n(i18n_code, label)
    form = forms.get_divinatory_form(i18n_code)
    if form.validate_on_submit():
        return _get_oracular_pronouncement(i18n_code)
    else:
        return flask.render_template(
                'oracle.html', form=form,
                page_title=_i("LANGUAGE_GARBAGE_ORACLE_TITLE"),
                persona_name=_i("ORACLE_PERSONA_NAME"),
                oracle_smells=_i("ORACLE_SMELLS"),
                origin_suggestion=_i("ORIGIN_WORD_SUGGESTION"),
                destiny_suggestion=_i("DESTINY_WORD_SUGGESTION"),
                get_it=_i("GET_AN"))


# This is a legacy endpoint that defaults to i18n:en.
@the_app.route('/oracle', methods=['GET', 'POST'])
def oracle_legacy():
    return oracle('en')


def _get_text_traversal(language, origin_word, destiny_word, text):
    # TODO: Add language selector back in (app/templates/oracle-en.html).
    language_code = forms.language_code_for(language)
    model_file_name = f'{language_code}.bin'

    model_file = os.path.join(
            the_app.static_folder, 'word2vec_models', model_file_name)
    try:
        the_oracle = Oracle.from_binary(model_file)
        sentences = list(the_oracle.traverse_text(origin_word, destiny_word, text))
        error_message = None
    except OracularError as e:
        sentences = []
        error_message = e.args[0]

    return {
        'sentences': sentences,
        'error_message': error_message,
        'language': language_code
    }


@the_app.route('/api/traverse-text', methods=['POST'])
def traverse_text_api():
    parameters = flask.request.json
    return flask.jsonify(_get_text_traversal(**parameters))


@the_app.route('/<i18n_code>/traverse-text', methods=['GET', 'POST'])
def traverse_text(i18n_code):
    # TODO: Add language selector back in (app/templates/oracle-en.html).
    _i = lambda label: _i18n(i18n_code, label)
    form = forms.get_text_traversal_form(i18n_code)
    if form.validate_on_submit():
        language = flask.request.form['language']
        origin_word = flask.request.form['origin_word']
        destiny_word = flask.request.form['destiny_word']
        text = flask.request.form['text']
        text_traversal = _get_text_traversal(
                language, origin_word, destiny_word, text)
        return flask.render_template(
                'slipped-text.html',
                # language=language,
                i18n_code=i18n_code,
                language=text_traversal['language'],
                sentences=text_traversal['sentences'],
                error_message=text_traversal['error_message'],
                oracle_walked_in_words=_i("ORACLE_WALKED_WORDS"),
                back_link=f"/{i18n_code}/traverse-text",
                back_link_message=_i("CONSULT_ORACLE_AGAIN"))
    else:
        print(form)
        return flask.render_template(
                'traverse-text.html', form=form,
                page_title=_i("LANGUAGE_GARBAGE_ORACLE_TITLE"),
                persona_name=_i("ORACLE_PERSONA_NAME"),
                oracle_smells=_i("ORACLE_SMELLS"),
                # i18n_code=i18n_code,
                origin_suggestion=_i("ORIGIN_WORD_SUGGESTION"),
                destiny_suggestion=_i("DESTINY_WORD_SUGGESTION"),
                get_it=_i("GET_AN"))


# This is a legacy endpoint that defaults to i18n:en.
# TODO: Figure out why en/en gets doubled when attempting to do this properly.
# Currently, "legacy" endpoints are saving lives.
@the_app.route('/traverse-text', methods=['GET', 'POST'])
def traverse_text_legacy():
    return traverse_text('en')


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


def _get_poetic_confusion(corpus, synonyms, number_sentences=None):
    synonym_sets = [
            set([token.strip().lower() for token in synonym.split(',')])
            for synonym in synonyms.split(';')
            if synonym.strip()]
    sentences = []
    if number_sentences is None:
        number_sentences = 5
    number_sentences = int(number_sentences)
    number_sentences = max(number_sentences, 1)
    try:
        corpus = textnorm.generate_normalized_sentences(corpus.strip())
        model = confused_model.Model.from_sentence_generator(
                corpus, synonym_sets)
        for _ in range(number_sentences):
            sentences.append(' '.join(model.generate_sentence()[2:]))
        error_message = None
    except confused_model.VaticError as e:
        error_message = e.args[0]

    return {
        'sentences': sentences,
        'error_message': error_message
    }


@the_app.route('/api/confused-poet', methods=['POST'])
def confused_poet_api():
    parameters = flask.request.json
    return flask.jsonify(_get_poetic_confusion(**parameters))


@the_app.route('/<i18n_code>/confused-poet', methods=['GET', 'POST'])
def confused_poet(i18n_code):
    _i = lambda label: _i18n(i18n_code, label)
    form = forms.get_confused_poet_form(i18n_code)
    if form.validate_on_submit():
        corpus = flask.request.form['corpus']
        synonyms = flask.request.form['synonyms']
        try:
            number_sentences = flask.request.form.get('number_sentences', 5)
        except:
            number_sentences = None
        poetic_confusion = _get_poetic_confusion(corpus, synonyms, number_sentences)
        return flask.render_template(
                'babbling.html',
                sentences=poetic_confusion['sentences'],
                error_message=poetic_confusion['error_message'],
                back_link=f"/{i18n_code}/confused-poet",
                back_link_message=_i("CONSULT_POET_AGAIN"))
    else:
        return flask.render_template(
                'confused-poet.html', form=form,
                page_title=_i("CONFUSED_POET_TITLE"),
                persona_name=_i("CONFUSED_POET_PERSONA_NAME"),
                corpus_suggestion=_i("CONFUSED_POET_CORPUS_SUGGESTION"),
                synonym_suggestion=_i("CONFUSED_POET_SYNONYM_SUGGESTION"),
                get_it=_i("GET_AN"))
