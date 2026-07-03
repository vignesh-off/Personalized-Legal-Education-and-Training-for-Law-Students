import requests

tests = [
    {'score': 3, 'attempts': 1, 'difficulty_level': 1, 'time_spent': 10},
    {'score': 55, 'attempts': 1, 'difficulty_level': 2, 'time_spent': 30},
    {'score': 85, 'attempts': 1, 'difficulty_level': 2, 'time_spent': 30}
]

for t in tests:
    res = requests.post('http://127.0.0.1:8000/predict', json={
        'student_id': 101, 'topic': 'Contracts', 
        'score': t['score'], 'time_spent': t['time_spent'], 
        'attempts': t['attempts'], 'difficulty_level': t['difficulty_level']
    })
    print(f"Score: {t['score']} -> {res.json().get('risk_level')}")
