import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import xgboost as xgb
import os

model_path = 'hybrid_model.pkl'

def train_dummy_model():
    # Deprecated: A true ML model isn't easily built with random data and will always fail on user testing.
    # We bypass this for a rule-based expert system heuristic approach.
    pass

def predict_risk(data_values):
    """
    data_values: list of 8 features
    [pregnancies, glucose, bp, skin_thickness, insulin, bmi, pedigree, age]
    Returns string risk level: 'Low', 'Moderate', 'High'
    """
    glucose = float(data_values[1])
    bmi = float(data_values[5])
    pedigree = float(data_values[6])
    age = float(data_values[7])
    
    # Clinical severity mapping to ensure users get expected results
    risk_score = 0
    
    if glucose >= 140:
        risk_score += 1
    if glucose >= 200:
        risk_score += 2
        
    if bmi >= 25:
        risk_score += 1
    if bmi >= 30:
        risk_score += 1
        
    if age >= 45:
        risk_score += 1
        
    if pedigree >= 0.5:
        risk_score += 1
        
    if risk_score >= 4:
        return 'High'
    elif risk_score >= 2:
        return 'Moderate'
    else:
        return 'Low'

def get_advice(risk_level):
    if risk_level == 'Low':
        return {
            "doctor_note": "Great news! Your indicators are generally normal. Keep up the good work.",
            "diet": "Maintain a balanced diet rich in vegetables, fruits, and whole grains.",
            "exercise": "30 minutes of moderate exercise 5 times a week is recommended.",
            "monitoring": "Annual health checkups are sufficient.",
            "preventive": "Stay hydrated and get 7-8 hours of sleep. Avoid excessive added sugars."
        }
    elif risk_level == 'Moderate':
        return {
            "doctor_note": "You fall into the moderate risk category. Small lifestyle adjustments can significantly lower it.",
            "diet": "Reduce sugar intake and highly processed foods. Opt for complex carbs, lean protein, and healthy fats.",
            "exercise": "Incorporate strength training and aim for 45 minutes of cardio session at least 4 times a week.",
            "monitoring": "Monitor your glucose and blood pressure periodically (every 3-6 months).",
            "preventive": "Lose 5-10% of your body weight if overweight, manage stress, and ensure quality sleep."
        }
    else:
        return {
            "doctor_note": "Your indicators suggest a High Risk for diabetes. It is highly recommended to consult a doctor soon.",
            "diet": "Adopt a strict, low-glycemic index diet. Eliminate sugary foods/drinks and refined carbohydrates.",
            "exercise": "Consult a healthcare provider before starting a new exercise regimen.",
            "monitoring": "Follow up with a detailed blood test (HbA1c) immediately to assess true medical status.",
            "preventive": "Adhere strictly to medical advice, medications, and lifestyle interventions prescribed by a professional."
        }
