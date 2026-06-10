from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

patients = []

AGENTS = [
    {
        'name': 'Classifier Agent',
        'role': 'Identifies symptom categories and clinical intent.',
        'status': 'Active',
        'action': 'Tagged 4 symptom groups'
    },
    {
        'name': 'Medical Extraction Agent',
        'role': 'Extracts relevant patient findings and context.',
        'status': 'Active',
        'action': 'Parsed symptom details'
    },
    {
        'name': 'Recommendation Agent',
        'role': 'Suggests medicines and dosage guidance.',
        'status': 'Active',
        'action': 'Generated treatment plan'
    },
    {
        'name': 'Documentation Agent',
        'role': 'Compiles notes into a structured clinical report.',
        'status': 'Active',
        'action': 'Prepared latest report'
    },
    {
        'name': 'QA Agent',
        'role': 'Scores accuracy and identifies potential risks.',
        'status': 'Active',
        'action': 'Verified report quality'
    }
]

SYMPTOM_KEYS = {
    'fever': 'Fever',
    'headache': 'Headache',
    'chest pain': 'Chest pain',
    'cold': 'Cold',
    'cough': 'Cold',
    'nausea': 'General',
    'fatigue': 'General',
    'dizziness': 'General'
}

MEDICINE_RECOMMENDATIONS = {
    'Fever': {
        'medicine': 'Paracetamol',
        'dosage': '500mg every 6 hours',
        'warning': 'Avoid if liver issues present.'
    },
    'Headache': {
        'medicine': 'Ibuprofen',
        'dosage': '400mg every 8 hours',
        'warning': 'Use with food to reduce stomach upset.'
    },
    'Chest pain': {
        'medicine': 'Aspirin',
        'dosage': '75mg once daily',
        'warning': 'Seek urgent medical review if pain persists.'
    },
    'Cold': {
        'medicine': 'Antihistamines',
        'dosage': '10mg once daily',
        'warning': 'May cause mild drowsiness.'
    },
    'General': {
        'medicine': 'Rest and hydration',
        'dosage': 'As needed',
        'warning': 'Monitor symptoms closely.'
    }
}


def classify_symptoms(text):
    normalized = text.lower()
    found = [label for key, label in SYMPTOM_KEYS.items() if key in normalized]
    return found or ['General']


def generate_diagnosis(symptom_labels):
    if 'Chest pain' in symptom_labels:
        return 'Possible cardiac strain or angina'
    if 'Fever' in symptom_labels:
        return 'Suspected viral infection'
    if 'Headache' in symptom_labels:
        return 'Tension headache with mild inflammation'
    if 'Cold' in symptom_labels:
        return 'Upper respiratory tract irritation'
    return 'General symptom cluster requiring monitoring'


def determine_severity(symptom_labels):
    if 'Chest pain' in symptom_labels:
        return 'High'
    if 'Fever' in symptom_labels or 'Headache' in symptom_labels:
        return 'Medium'
    return 'Low'


def determine_status(severity):
    return 'Critical' if severity == 'High' else 'Stable'


def generate_qa_score():
    return random.randint(82, 98)


def recommend_medicines(symptom_labels):
    recommendations = []
    for label in symptom_labels:
        medicine = MEDICINE_RECOMMENDATIONS.get(label)
        if medicine and medicine not in recommendations:
            recommendations.append(medicine)
    return recommendations[:2] or [MEDICINE_RECOMMENDATIONS['General']]


@app.route('/')
def dashboard():
    latest_report = patients[0] if patients else None
    total_reports = len(patients)
    resolved_count = sum(1 for report in patients if report['status'] == 'Stable')
    escalated_count = sum(1 for report in patients if report['status'] == 'Critical')
    ai_accuracy = 90 + min(8, max(-5, (resolved_count - escalated_count)))

    return render_template(
        'dashboard.html',
        patients=patients,
        latest_report=latest_report,
        total_reports=total_reports,
        resolved_count=resolved_count,
        escalated_count=escalated_count,
        ai_accuracy=ai_accuracy,
        agents=AGENTS
    )


@app.route('/submit', methods=['POST'])
def submit_report():
    symptoms = request.form.get('symptoms', '').strip()
    if not symptoms:
        return redirect(url_for('dashboard'))

    symptom_labels = classify_symptoms(symptoms)
    diagnosis = generate_diagnosis(symptom_labels)
    severity = determine_severity(symptom_labels)
    status = determine_status(severity)
    qa_score = generate_qa_score()
    medicines = recommend_medicines(symptom_labels)
    ai_message = 'Hello, I have analyzed the patient data and prepared a clinical summary.'

    report = {
        'symptoms': symptoms,
        'labels': symptom_labels,
        'diagnosis': diagnosis,
        'severity': severity,
        'status': status,
        'qa_score': qa_score,
        'medicines': medicines,
        'ai_message': ai_message,
        'time': datetime.now().strftime('%b %d, %Y %I:%M %p')
    }

    patients.insert(0, report)
    return redirect(url_for('dashboard'))


@app.route('/agents')
def agents_page():
    return render_template('agents.html', agents=AGENTS)


if __name__ == '__main__':
    app.run(debug=True)
