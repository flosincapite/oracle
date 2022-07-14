import flask_wtf
from wtforms import SelectField, StringField, SubmitField


class DivinatoryForm(flask_wtf.FlaskForm):
    language = SelectField(
            'Language',
            choices = ['ar', 'en', 'es', 'fa', 'fr', 'ku', 'tr', 'ur'])
    origin_word = StringField('Origin Word')
    destiny_word = StringField('Destiny Word')
    submit = SubmitField('Oracular Pronouncement')
