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

@app.route('/admin/profiles/edit', methods=['GET', 'POST'])
def admin_profiles_edit():
    if request.method == 'POST':
        profileId = request.form.get('profileId', '')

        if not profileId:
            error = f"No profile id provided."
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

        profileToUpdate = Profile.query.filter_by(id=profileId).first()

        if not profileToUpdate:
            error = f"No profile found to edit with id = {profileId}."
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

        try:
            profileToUpdate.name = request.form.get(
                'name', profileToUpdate.name)
            profileToUpdate.num = request.form.get(
                'num', profileToUpdate.num)
            profileToUpdate.cvv = request.form.get(
                'cvv', profileToUpdate.cvv)
            profileToUpdate.expDate = request.form.get(
                'expDate', profileToUpdate.expDate)
            profileToUpdate.mName = request.form.get(
                'mName', profileToUpdate.mName)
            profileToUpdate.con = request.form.get('con', profileToUpdate.con)
            profileToUpdate.ungaBunga = request.form.get(
                'ungaBunga', False) == "yes"
            profileToUpdate.updated = datetime.now(timezone.utc)
            db.session.commit()
            return redirect(url_for('admin_profiles'))
        except Exception as e:
            db.session.rollback()
            error = f"Error writing to database file."
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

    profileId = request.args.get('profileId')

    if not profileId:
        error = f"No profile id provided."
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)

    profileToEdit = Profile.query.filter_by(id=profileId).first()

    if not profileToEdit:
        error = f"No profile found to edit with id = {profileId}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)

    return render_template('profileEdit.html', profile=profileToEdit)

@app.route('/admin/profiles/deleteButton', methods=['POST'])
def admin_profilesDeleteButton():
    try:
        profileId = request.form.get('profileId', '')

        if not profileId:
            error = f"No profile id included for deletion."
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

        profile_to_delete = Profile.query.filter_by(id=profileId).first()

        if not profile_to_delete:
            error = f"No profile found with id = {profileId}"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)
        if request.form.get('deleteStyle') == 'hard':
            db.session.delete(profile_to_delete)

            db.session.commit()

            return redirect(url_for('admin_profiles'))
        else:
            profile_to_delete.deleted = not profile_to_delete.deleted

            db.session.commit()

            return redirect(url_for('admin_profiles'))

    except Exception as e:
        db.session.rollback()
        error = f"Error writing to database file."
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)