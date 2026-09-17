"""
Comprehensive Endpoints Verification Script
Tests guest authentication, registered authentication, session auto-recovery,
conversation chat with disease prediction, symptoms list, direct disease prediction, and vitals.
"""
import requests

def get_active_base_url():
    for p in [5005, 5000]:
        try:
            r = requests.get(f"http://localhost:{p}/health", timeout=1)
            if r.status_code == 200 and r.json().get('service') == 'CarePulse Health Platform':
                return f"http://localhost:{p}"
        except Exception:
            continue
    return "http://localhost:5000"

BASE_URL = get_active_base_url()

def test_all():
    print("==================================================")
    print("Testing All CarePulse Clinical Endpoints...")
    print("==================================================")
    passed = 0
    total = 0

    # 1. Health check
    total += 1
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200 and r.json().get('status') == 'healthy'
    assert r.json().get('service') == 'CarePulse Health Platform'
    print(f"[{total}] Health Check: PASS (Service: {r.json().get('service')})")
    passed += 1

    # 2. Guest Authentication
    total += 1
    r = requests.post(f"{BASE_URL}/api/auth/guest")
    assert r.status_code == 200 and r.json().get('success') is True
    guest_token = r.json().get('session_token')
    print(f"[{total}] Guest Login: PASS (Token: {guest_token[:15]}...)")
    passed += 1

    # 3. Chat with Guest Token (Simulating the user's exact issue from the image!)
    total += 1
    headers_guest = {"Authorization": f"Bearer {guest_token}", "Content-Type": "application/json"}
    r = requests.post(
        f"{BASE_URL}/api/conversation/new/chat",
        headers=headers_guest,
        json={"message": "I have high fever, chills, and shivering"}
    )
    res_data = r.json()
    assert r.status_code == 200 and res_data.get('success') is True
    pred = res_data.get('disease_prediction')
    pred_name = pred['primary_diagnosis']['name'] if pred else 'N/A'
    print(f"[{total}] Guest Chat with Fever & Chills: PASS -> Predicted: '{pred_name}' (Status: {r.status_code})")
    assert "Malaria" in pred_name or "Dengue" in pred_name or "Fever" in pred_name
    passed += 1

    # 4. Chat with null conversation id (Auto-healing test)
    total += 1
    r = requests.post(
        f"{BASE_URL}/api/conversation/null/chat",
        headers={"Authorization": "Bearer guest_random_token_123"},
        json={"message": "fever"}
    )
    res_data = r.json()
    assert r.status_code == 200 and res_data.get('success') is True
    print(f"[{total}] Self-Healing Chat with null ID: PASS -> Response received without blocking")
    passed += 1

    # 5. Symptoms list endpoint
    total += 1
    r = requests.get(f"{BASE_URL}/api/symptoms-list")
    assert r.status_code == 200 and len(r.json().get('categories', {})) >= 5
    print(f"[{total}] Symptoms List API: PASS ({len(r.json()['categories'])} categories)")
    passed += 1

    # 6. Direct Disease Prediction endpoint
    total += 1
    r = requests.post(f"{BASE_URL}/api/predict-disease", json={
        "symptoms": ["wheezing", "shortness_of_breath", "chest_tightness"],
        "age": "18-64 years (Adult)"
    })
    res_data = r.json()
    assert r.status_code == 200 and res_data.get('success') is True
    pred_name = res_data['prediction']['primary_diagnosis']['name']
    confidence = res_data['prediction']['primary_diagnosis']['confidence']
    print(f"[{total}] Direct Disease Predictor API: PASS -> Predicted: '{pred_name}' ({confidence}%)")
    assert "Asthma" in pred_name
    passed += 1

    # 7. Vitals Monitoring endpoint
    total += 1
    r = requests.post(f"{BASE_URL}/api/vitals/analyze", json={
        "systolic_bp": 135,
        "diastolic_bp": 85,
        "heart_rate": 78,
        "spo2": 97
    })
    res_data = r.json()
    assert r.status_code == 200 and res_data.get('success') is True
    vitals_status = res_data['analysis']['overall_status']
    print(f"[{total}] Vitals Evaluation API: PASS -> Status: '{vitals_status}'")
    passed += 1

    print("\n==================================================")
    print(f"ALL ENDPOINT TESTS PASSED: {passed}/{total} SUCCESS")
    print("==================================================")

if __name__ == "__main__":
    test_all()
