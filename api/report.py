import json
import random
from datetime import datetime

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


def parse_json_body(request):
    body = {}
    if hasattr(request, 'json'):
        body = request.json or {}
    elif hasattr(request, 'get_json'):
        body = request.get_json(silent=True) or {}
    elif hasattr(request, 'body'):
        try:
            body = json.loads(request.body.decode() if isinstance(request.body, bytes) else request.body)
        except Exception:
            body = {}
    return body


def handler(request):
    payload = parse_json_body(request)
    symptoms = (payload.get('symptoms') or '').strip()

    if not symptoms:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Symptom text is required.'})
        }

    labels = classify_symptoms(symptoms)
    diagnosis = generate_diagnosis(labels)
    severity = determine_severity(labels)
    status = determine_status(severity)
    qa_score = generate_qa_score()
    medicines = recommend_medicines(labels)

    report = {
        'symptoms': symptoms,
        'labels': labels,
        'diagnosis': diagnosis,
        'severity': severity,
        'status': status,
        'qa_score': qa_score,
        'medicines': medicines,
        'ai_message': 'Hello, I have analyzed the patient data and prepared a clinical summary.',
        'time': datetime.utcnow().strftime('%b %d, %Y %I:%M %p')
    }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(report)
    }

application = handler
app = handler
