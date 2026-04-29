from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import db, User, PatientRecord
from utils import predict_risk, get_advice
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_super_secret_bioscan_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bioscan.db'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please login to analyze patient data.', 'warning')
            return redirect(url_for('login'))
            
        try:
            p_name = request.form['patient_name']
            p_email = request.form['patient_email']
            pregnancies = int(request.form['pregnancies'])
            glucose = float(request.form['glucose'])
            bp = float(request.form['blood_pressure'])
            skin = float(request.form['skin_thickness'])
            insulin = float(request.form['insulin'])
            bmi = float(request.form['bmi'])
            pedigree = float(request.form['pedigree_function'])
            age = int(request.form['age'])
            
            features = [pregnancies, glucose, bp, skin, insulin, bmi, pedigree, age]
            risk_level = predict_risk(features)
            advice = get_advice(risk_level)
            
            # Save record
            record = PatientRecord(
                user_id=current_user.id,
                patient_name=p_name,
                patient_email=p_email,
                pregnancies=pregnancies,
                glucose=glucose,
                blood_pressure=bp,
                skin_thickness=skin,
                insulin=insulin,
                bmi=bmi,
                pedigree_function=pedigree,
                age=age,
                risk_level=risk_level
            )
            db.session.add(record)
            db.session.commit()
            
            return render_template('index.html', risk_level=risk_level, advice=advice, original_data=request.form)
            
        except Exception as e:
            flash('Error in inputs. Please enter valid numbers.', 'danger')
            return render_template('index.html')
            
    return render_template('index.html', risk_level=None)

@app.route('/database')
@login_required
def database():
    search = request.args.get('search', '')
    if search:
        records = PatientRecord.query.filter(
            (PatientRecord.user_id == current_user.id) &
            ((PatientRecord.patient_name.ilike(f'%{search}%')) | (PatientRecord.patient_email.ilike(f'%{search}%')))
        ).all()
    else:
        records = PatientRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('database.html', records=records, search=search)

@app.route('/delete_record/<int:record_id>')
@login_required
def delete_record(record_id):
    record = PatientRecord.query.get_or_404(record_id)
    if record.user_id == current_user.id:
        db.session.delete(record)
        db.session.commit()
        flash('Record deleted successfully.', 'success')
    return redirect(url_for('database'))



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/hybrid_model')
def hybrid_model():
    return render_template('hybrid_model.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for reaching out! Your secure message has been received by our technical team.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'danger')
            return redirect(url_for('signup'))
            
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(full_name=full_name, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
