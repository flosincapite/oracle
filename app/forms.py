import os
import re

import flask_wtf
from wtforms import SelectField, StringField, SubmitField

from app import the_app


_CODE_TO_ENGLISH_GLOTTONYM = {
    'ar': 'Arabic (Modern Standard)',
    'en_combined': 'English (Combined)',
    'en_reddit': 'English (Nasty Old Reddit)',
    'en_wiki': 'English (Wikipedia)',
    'es': 'Spanish (Castellano)',
    'fr': 'French',
    'fa': 'Persian',
    'ku': 'Kurdish (Kurmancî)',
    'tr': 'Turkish',
    'ur': 'Urdu'
}


def _populate_languages():
    languages = {}
    for fname in os.listdir(os.path.join(the_app.static_folder, 'word2vec_models')):
        if re.search(r'^\w+\.bin$', fname):
            language_code = fname.split('.')[0]
            if language_code in _CODE_TO_ENGLISH_GLOTTONYM:
                language_eng = _CODE_TO_ENGLISH_GLOTTONYM[language_code]
                languages[language_eng] = language_code
    return languages


_LANGUAGES = _populate_languages()


# TODO: Dynamically create Form classes using i18n module instead of doing this
# nonsense.
class DivinatoryFormEn(flask_wtf.FlaskForm):
    language = SelectField('Language', choices=sorted(_LANGUAGES.keys()))
    origin_word = StringField('Origin Word')
    destiny_word = StringField('Destiny Word')
    submit = SubmitField('Oracular Pronouncement')


class DivinatoryFormEs(flask_wtf.FlaskForm):
    origin_word = StringField('Palabra Origen')
    destiny_word = StringField('Palabra Destino')
    submit = SubmitField('Adivinación Fatídica')


class ConfusedPoetFormEn(flask_wtf.FlaskForm):
    corpus = StringField('Corpus')
    synonyms = StringField('Synonyms')
    number_sentences = StringField('Number of Sentences')
    submit = SubmitField('Create an AI Poetry Friend')


class ConfusedPoetFormEs(flask_wtf.FlaskForm):
    corpus = StringField('Corpus')
    synonyms = StringField('Sinónimos')
    number_sentences = StringField('Número de Oraciones')
    submit = SubmitField('Crear una IA amiga poeta')


def language_code_for(language):
    return _LANGUAGES[language]


def get_divinatory_form(i18n_code):
    if i18n_code == 'en':
        return DivinatoryFormEn()
    elif i18n_code == 'es':
        return DivinatoryFormEs()


def get_confused_poet_form(i18n_code):
    if i18n_code == 'en':
        return ConfusedPoetFormEn()
    elif i18n_code == 'es':
        return ConfusedPoetFormEs()
