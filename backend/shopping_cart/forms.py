from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, message="Quantity must be at least 1")])
    submit = SubmitField('Add to Cart')

class RemoveFromCartForm(FlaskForm):
    submit = SubmitField('Remove')

class ClearCartForm(FlaskForm):
    submit = SubmitField('Clear Cart')
