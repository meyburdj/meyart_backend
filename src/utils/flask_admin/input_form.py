from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField
from wtforms.validators import DataRequired

class ArtworkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    media = StringField('Media')
    size = StringField('Size')
    price = StringField('Price')
    genre = StringField('Genre')
    information = StringField('Information')
    quantity = StringField('Quantity')
    date = StringField('Date')
    file = FileField('File')
    artist_id = SelectField('Artist', coerce=int)
