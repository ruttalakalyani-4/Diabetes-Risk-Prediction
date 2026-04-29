from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_name = db.Column(db.String(150), nullable=False)
    patient_email = db.Column(db.String(150), nullable=False)
    pregnancies = db.Column(db.Integer, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.Float, nullable=False)
    skin_thickness = db.Column(db.Float, nullable=False)
    insulin = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    pedigree_function = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False) # Low, Moderate, High
    date_of_test = db.Column(db.DateTime, default=datetime.utcnow)


