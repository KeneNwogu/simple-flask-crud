from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField, IntegerField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers

def validate_nigerian_phone(form, field):
    try:
        parsed_number = phonenumbers.parse(field.data, 'NG')
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError('Invalid Nigerian phone number format')
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError('Invalid phone number')

class LevyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    burial_name = StringField('Name of Deceased', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    amount = FloatField('Amount Paid', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), validate_nigerian_phone])
    arrears = StringField('Arrears')
    signature = StringField('Signature of receiving officer', validators=[DataRequired()])
    comments = StringField('Comments')
    submit = SubmitField('Submit')