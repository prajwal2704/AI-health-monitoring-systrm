"""
Automated Test Suite for Disease Prediction and Health Monitoring Engine
Tests multi-symptom clinical evaluation, confidence scoring, vitals monitoring, and follow-up generation.
"""
import sys
import os

# Add local path
sys.path.insert(0, os.path.dirname(__file__))

from engine.disease_predictor import DiseasePredictor
from engine.vitals_monitor import VitalsMonitor
from engine.follow_up_generator import FollowUpGenerator
from medical_response_generator import MedicalResponseGenerator

def test_disease_predictions():
    print("==================================================")
    print("Testing Clinical Disease Prediction Engine...")
    print("==================================================")
    predictor = DiseasePredictor()

    test_cases = [
        {
            "name": "Dengue Fever Profile",
            "symptoms": ["high_fever", "severe_headache", "pain_behind_eyes", "joint_pain"],
            "expected_disease": "Dengue Fever"
        },
        {
            "name": "Malaria Profile",
            "symptoms": ["high_fever", "chills", "sweating", "shivering"],
            "expected_disease": "Malaria"
        },
        {
            "name": "Type 2 Diabetes Profile",
            "symptoms": ["frequent_urination", "excessive_thirst", "unexplained_weight_loss"],
            "expected_disease": "Type 2 Diabetes Mellitus"
        },
        {
            "name": "Asthma Exacerbation Profile",
            "symptoms": ["wheezing", "shortness_of_breath", "chest_tightness"],
            "expected_disease": "Bronchial Asthma / Asthma Exacerbation"
        },
        {
            "name": "Migraine Headache Profile",
            "symptoms": ["throbbing_one_sided_headache", "sensitivity_to_light_photophobia", "nausea"],
            "expected_disease": "Migraine Headache"
        },
        {
            "name": "Acute Appendicitis Profile (Emergency)",
            "symptoms": ["sudden_pain_lower_right_abdomen", "nausea", "low_fever"],
            "expected_disease": "Acute Appendicitis"
        },
        {
            "name": "Natural Language Text Parsing (COVID-19)",
            "text": "I lost my sense of taste and smell, having dry cough and fever",
            "symptoms": [],
            "expected_disease": "COVID-19 (Coronavirus)"
        }
    ]

    passed = 0
    for tc in test_cases:
        result = predictor.predict(
            symptoms=tc.get("symptoms", []),
            text_input=tc.get("text", ""),
            age="18-64 years (Adult)"
        )
        primary = result.get("primary_diagnosis", {})
        predicted_name = primary.get("name", "Unknown")
        confidence = primary.get("confidence", 0)

        matches = (predicted_name == tc["expected_disease"])
        status = "[PASS]" if matches else "[FAIL]"
        if matches:
            passed += 1

        print(f"\nTest Case: {tc['name']}")
        if "text" in tc:
            print(f"  Input Text: '{tc['text']}'")
        else:
            print(f"  Input Symptoms: {tc['symptoms']}")
        print(f"  Result: {status} -> Predicted: '{predicted_name}' ({confidence}% confidence)")
        print(f"  Clinical Urgency: {result.get('urgency').upper()}")

    print(f"\nPrediction Tests: {passed}/{len(test_cases)} passed.")
    assert passed == len(test_cases), f"Only {passed}/{len(test_cases)} test cases passed!"

def test_vitals_monitoring():
    print("\n==================================================")
    print("Testing Health Vitals Monitoring Engine...")
    print("==================================================")
    monitor = VitalsMonitor()

    # Normal Vitals
    normal_res = monitor.analyze_vitals(
        systolic_bp=118, diastolic_bp=78,
        heart_rate=72, spo2=98,
        temperature=98.6, blood_sugar=90, sugar_type='fasting'
    )
    print(f"Normal Panel: {normal_res['overall_status']} (Risk score: {normal_res['risk_score']})")
    assert normal_res['overall_status'] == "Normal / Healthy Vitals"

    # Hypertensive Crisis + Hypoxia Emergency
    emergency_res = monitor.analyze_vitals(
        systolic_bp=190, diastolic_bp=125,
        heart_rate=128, spo2=88,
        temperature=103.5
    )
    print(f"Emergency Panel: {emergency_res['overall_status']} (Alerts: {len(emergency_res['alerts'])})")
    assert emergency_res['overall_status'] == "Critical Risk"
    assert len(emergency_res['alerts']) >= 3
    print("[PASS] Vitals Monitoring tests passed!")

def test_full_medical_response_generator():
    print("\n==================================================")
    print("Testing Medical Response Generator Integration...")
    print("==================================================")
    gen = MedicalResponseGenerator()
    resp = gen.generate_medical_response(
        symptoms="I have high fever, chills, sweating and body aches",
        age="18-64 years (Adult)",
        language="english"
    )

    assert resp['success'] is True
    res_obj = resp['response']
    pred = resp['disease_prediction']

    print(f"Primary Predicted Disease: {pred['primary_diagnosis']['name']} ({pred['primary_diagnosis']['confidence']}%)")
    print(f"Summary starts with: {res_obj['summary'][:80]}...")
    print(f"Home care has {len(res_obj['home_care'].splitlines())} points.")
    assert "Malaria" in pred['primary_diagnosis']['name'] or "Dengue" in pred['primary_diagnosis']['name']
    print("[PASS] Full Medical Response Generator tests passed!")

if __name__ == "__main__":
    test_disease_predictions()
    test_vitals_monitoring()
    test_full_medical_response_generator()
    print("\n[ALL TESTS PASSED SUCCESSFULLY!]")
