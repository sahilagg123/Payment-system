from flask import Flask, render_template,url_for,flash,redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import AddUserForm
from flask_ngrok import run_with_ngrok



app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = '1a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# two decorators, same function

class User(db.Model):
    Phone_number = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Integer, nullable=False)
    Loan_Amount = db.Column(db.Integer, nullable=False)
    Amount_due = db.Column(db.Integer, nullable=False)
    Interest_rate = db.Column(db.Integer, nullable=False)
    Due_date = db.Column(db.String, nullable=False)

@app.route('/')

@app.route('/index', methods=['GET','POST'])
def index():
    form = AddUserForm()
    if form.is_submitted():
        #save the data
        newuser = User(Phone_number=form.phone_number.data, Name=form.name.data,Loan_Amount=form.loan_amount.data,Amount_due=form.amount_due.data,Interest_rate=form.interest_rate.data,Due_date=form.due_date.data )
        db.session.add(newuser)
        db.session.commit()
        print('save the data')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)



@app.route('/tests/endpoint1', methods=['GET','POST'])
def my_test_endpoint1():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    import razorpay
    print('hi')

    client = razorpay.Client(auth=("rzp_test_bDLEtiKzqV7Um2", "OQCBfl1rSit4te5QEX415Izr"))


    client.set_app_details({"title": "Danjo", "version": "1.8.17"})

    print(input_json)

    phone_number=int(input_json['phone_number'])
    # find the phone number and get the amount to be paid
    #
    record = User.query.filter_by(Phone_number=phone_number).first()
    print(record.Name)
    amount = record.Amount_due
    DATA = {

        "type": "link",
        "amount": amount*100,
        "currency": "INR",
        "description": "EMI"
    }

    a = client.invoice.create(data=DATA)
    print(a['short_url'])
    print(a['id'])
    obj={
        "link": a['short_url']
    }
    return jsonify(obj)


#11/11/2011

@app.route('/tests/endpoint2', methods=['GET','POST'])
def my_test_endpoint2():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'


    print(input_json)

    phone_number=int(input_json['phone_number'])
    # find the phone number and get the amount to be paid
    #
    record = User.query.filter_by(Phone_number=phone_number).first()
    print(record.Name)
    amount = record.Amount_due
    due_date = record.Due_date


    obj={
        "amount": amount,
        "due_date":due_date
    }
    return jsonify(obj)

if __name__ == '__main__':
    app.run()