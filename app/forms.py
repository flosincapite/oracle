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


class DivinatoryForm(flask_wtf.FlaskForm):
    language = SelectField('Language', choices=sorted(_LANGUAGES.keys()))
    origin_word = StringField('Origin Word')
    destiny_word = StringField('Destiny Word')
    submit = SubmitField('Oracular Pronouncement')


def language_code_for(language):
    return _LANGUAGES[language]


class ConfusedPoetForm(flask_wtf.FlaskForm):
    corpus = StringField('Enter Text')
    synonyms = StringField('Enter Synonym Sets')
    submit = SubmitField('Create a Confused Poetry Robot Friend')
