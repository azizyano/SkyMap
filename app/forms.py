# forms.py

from wtforms import Form, StringField, SelectField, validators

class SkyMapSearchForm(Form):
    choices = [('skylink', 'skylink'),
               ('location', 'location')]
    select = SelectField('Search:', choices=choices)
    search = StringField('')