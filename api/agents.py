import json

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


def handler(request):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(AGENTS)
    }

application = handler
app = handler
