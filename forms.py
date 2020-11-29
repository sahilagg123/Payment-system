from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class AddUserForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = IntegerField('Phone_number',validators=[DataRequired()])
    loan_amount = IntegerField('Loan_amount', validators=[DataRequired()])
    amount_due = IntegerField('Amount_due', validators=[DataRequired()])
    interest_rate = IntegerField('Interest_rate', validators=[DataRequired()])
    due_date = StringField('Due_date',validators=[DataRequired()])
    submit = SubmitField('Submit')