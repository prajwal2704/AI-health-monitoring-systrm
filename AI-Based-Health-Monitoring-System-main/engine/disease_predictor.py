"""
Clinical Disease Predictor Engine
Infers medical conditions based on multi-symptom input and free-text analysis.
Calculates weighted match confidence, classifies clinical urgency, and generates differential diagnoses.
"""
import re
from typing import List, Dict, Any, Tuple
from .disease_database import DISEASE_DATABASE, SYMPTOM_CATEGORIES, SYMPTOM_SYNONYMS

class DiseasePredictor:
    """Multi-symptom diagnostic inference engine"""

    PRIMARY_WEIGHT = 3.0
    SECONDARY_WEIGHT = 1.2
    CONFIDENCE_THRESHOLD = 0.20  # Minimum 20% match to be considered in differential

    def __init__(self):
        self.database = DISEASE_DATABASE
        self.synonyms = SYMPTOM_SYNONYMS

    def extract_symptoms_from_text(self, text: str) -> List[str]:
        """Extract standardized symptom tokens from free-text user descriptions"""
        if not text:
            return []

        cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
        detected_tokens = set()

        # 1. Match multi-word synonyms first (longer phrases first)
        sorted_phrases = sorted(self.synonyms.keys(), key=len, reverse=True)
        for phrase in sorted_phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, cleaned_text):
                token = self.synonyms[phrase]
                detected_tokens.add(token)

        # 2. Check for exact token matches in database
        for dis_id, data in self.database.items():
            for sym in data['primary_symptoms'] + data['secondary_symptoms']:
                readable = sym.replace('_', ' ')
                if re.search(r'\b' + re.escape(readable) + r'\b', cleaned_text):
                    detected_tokens.add(sym)

        return list(detected_tokens)

    def get_readable_symptom_name(self, token: str) -> str:
        """Convert a symptom token to a user-friendly clinical display name"""
        for cat, sym_list in SYMPTOM_CATEGORIES.items():
            for tok, name in sym_list:
                if tok == token:
                    return name
        return token.replace('_', ' ').title()

    def predict(self, symptoms: List[str], age: str = 'Adult', text_input: str = '') -> Dict[str, Any]:
        """
        Run multi-symptom clinical evaluation.
        Returns top predictions, confidence percentages, urgency rating, and treatment advice.
        """
        combined_symptoms = set(symptoms or [])

        # Extract any additional symptoms from text
        if text_input:
            extracted = self.extract_symptoms_from_text(text_input)
            combined_symptoms.update(extracted)

        active_symptoms = list(combined_symptoms)

        if not active_symptoms:
            return {
                "success": False,
                "error": "No recognizable symptoms were provided.",
                "predictions": [],
                "primary_diagnosis": None,
                "urgency": "mild",
                "extracted_symptoms": []
            }

        scores: List[Dict[str, Any]] = []

        for dis_id, info in self.database.items():
            primary = info['primary_symptoms']
            secondary = info['secondary_symptoms']

            matched_primary = [s for s in primary if s in active_symptoms]
            matched_secondary = [s for s in secondary if s in active_symptoms]

            # Weighted scoring
            matched_score = (len(matched_primary) * self.PRIMARY_WEIGHT) + (len(matched_secondary) * self.SECONDARY_WEIGHT)
            total_possible = (len(primary) * self.PRIMARY_WEIGHT) + (len(secondary) * self.SECONDARY_WEIGHT)

            if total_possible == 0:
                continue

            raw_confidence = matched_score / total_possible

            # Bonus for matching multiple core primary symptoms
            if len(matched_primary) >= 2:
                raw_confidence = min(0.98, raw_confidence * 1.25)
            elif len(matched_primary) == 1 and len(matched_secondary) >= 2:
                raw_confidence = min(0.90, raw_confidence * 1.15)

            # Cap confidence gracefully between 15% and 96%
            confidence_pct = round(raw_confidence * 100, 1)

            if raw_confidence >= self.CONFIDENCE_THRESHOLD or len(matched_primary) >= 1:
                unmatched_primary = [s for s in primary if s not in active_symptoms]
                scores.append({
                    "id": dis_id,
                    "name": info['name'],
                    "category": info['category'],
                    "severity": info['severity'],
                    "confidence": confidence_pct,
                    "matched_primary_count": len(matched_primary),
                    "matched_secondary_count": len(matched_secondary),
                    "matched_symptoms": [self.get_readable_symptom_name(s) for s in (matched_primary + matched_secondary)],
                    "unmatched_symptoms_to_watch": [self.get_readable_symptom_name(s) for s in unmatched_primary[:4]],
                    "red_flags": info['red_flags'],
                    "description": info['description'],
                    "home_care": info['home_care'],
                    "medications_otc": info['medications_otc'],
                    "when_to_see_doctor": info['when_to_see_doctor']
                })

        # Sort by confidence and primary symptom matches descending
        scores.sort(key=lambda x: (x['confidence'], x['matched_primary_count']), reverse=True)

        # Build differential diagnosis
        top_predictions = scores[:3]

        if not top_predictions:
            # Fallback when symptoms are very non-specific
            top_predictions = [{
                "id": "general_viral_syndrome",
                "name": "General Acute Viral Syndrome / Fatigue",
                "category": "General Medicine",
                "severity": "mild",
                "confidence": 45.0,
                "matched_primary_count": 1,
                "matched_secondary_count": 0,
                "matched_symptoms": [self.get_readable_symptom_name(s) for s in active_symptoms[:3]],
                "unmatched_symptoms_to_watch": ["Fever > 101°F", "Shortness of breath", "Stiff neck"],
                "red_flags": ["High persistent fever", "Inability to retain fluids", "Difficulty breathing"],
                "description": "A common acute physiological response to mild viral exposure, physical exhaustion, or climatic changes.",
                "home_care": [
                    "Rest well and stay hydrated with warm water, broths, and electrolyte fluids.",
                    "Eat light, easily digestible meals and avoid strenuous exertion.",
                    "Monitor your temperature and symptom progression."
                ],
                "medications_otc": "Paracetamol for aches/fever if needed.",
                "when_to_see_doctor": "Consult a doctor if symptoms escalate or persist longer than 72 hours."
            }]

        primary_diagnosis = top_predictions[0]

        # Overall clinical urgency
        urgency = "mild"
        if any(p['severity'] == 'critical' for p in top_predictions if p['confidence'] >= 40):
            urgency = "critical"
        elif any(p['severity'] == 'high' for p in top_predictions if p['confidence'] >= 40):
            urgency = "high"
        elif any(p['severity'] == 'moderate' for p in top_predictions if p['confidence'] >= 40):
            urgency = "moderate"

        # Check for immediate critical red flags based on active symptoms
        emergency_flags = []
        if any(s in active_symptoms for s in ["chest_pressure_squeezing", "pain_radiating_to_arm_neck_jaw"]):
            urgency = "critical"
            emergency_flags.append("[URGENT] Thoracic pain or chest pressure may indicate acute coronary syndrome. Seek immediate emergency care!")
        if any(s in active_symptoms for s in ["coughing_blood"]):
            urgency = "high"
            emergency_flags.append("[URGENT] Coughing blood requires immediate pulmonary evaluation.")
        if any(s in active_symptoms for s in ["sudden_pain_lower_right_abdomen"]):
            urgency = "critical"
            emergency_flags.append("[URGENT] Severe acute lower right abdominal pain requires urgent evaluation to rule out appendicitis.")

        return {
            "success": True,
            "active_symptoms": [self.get_readable_symptom_name(s) for s in active_symptoms],
            "active_symptom_tokens": active_symptoms,
            "primary_diagnosis": primary_diagnosis,
            "differential_diagnoses": top_predictions[1:],
            "all_predictions": top_predictions,
            "urgency": urgency,
            "emergency_flags": emergency_flags,
            "age_group": age
        }
