"""
Diagnostic Follow-up Question Generator
Generates targeted clinical questions to distinguish between differential diagnoses.
"""
from typing import List, Dict, Any

class FollowUpGenerator:
    """Generates intelligent follow-up questions to refine differential diagnoses"""

    DISEASE_DIFFERENTIATING_QUESTIONS = {
        "dengue": [
            {"id": "pain_behind_eyes", "question": "Are you feeling deep, painful pressure behind your eyes?", "weight": 2.5},
            {"id": "skin_rash", "question": "Have you noticed any reddish spots or skin rash appearing on your arms or chest?", "weight": 2.0},
            {"id": "joint_pain", "question": "Are your joints aching severely ('breakbone' aches)?", "weight": 2.0}
        ],
        "malaria": [
            {"id": "chills", "question": "Do you experience intense shivering or teeth-chattering chills before the fever spikes?", "weight": 2.5},
            {"id": "sweating", "question": "Does the fever break with profuse sweating in repeated cycles?", "weight": 2.5}
        ],
        "typhoid": [
            {"id": "stomach_pain", "question": "Has your fever been slowly rising over several days along with continuous stomach ache?", "weight": 2.5},
            {"id": "loss_of_appetite", "question": "Have you completely lost your appetite or feel a coated tongue?", "weight": 1.8}
        ],
        "covid_19": [
            {"id": "loss_of_taste_smell", "question": "Have you experienced any loss or alteration of taste or smell?", "weight": 3.0},
            {"id": "shortness_of_breath", "question": "Do you feel out of breath after walking short distances?", "weight": 2.0}
        ],
        "pneumonia": [
            {"id": "productive_cough_with_colored_phlegm", "question": "Is your cough producing thick yellowish, greenish, or rust-colored phlegm?", "weight": 2.5},
            {"id": "sharp_chest_pain_on_breathing", "question": "Does taking a deep breath cause sharp, stabbing chest pain?", "weight": 3.0}
        ],
        "asthma": [
            {"id": "wheezing", "question": "Do you hear a whistling or wheezing sound when breathing out?", "weight": 3.0},
            {"id": "chest_tightness", "question": "Does your chest feel tight or constricted, especially at night or in cold air?", "weight": 2.5}
        ],
        "migraine": [
            {"id": "throbbing_one_sided_headache", "question": "Is the head pain throbbing and primarily located on one side of your head?", "weight": 3.0},
            {"id": "sensitivity_to_light_photophobia", "question": "Are bright lights or normal noises causing irritation or worsening the headache?", "weight": 2.5}
        ],
        "diabetes_mellitus": [
            {"id": "excessive_thirst", "question": "Are you feeling persistently thirsty and drinking unusually large amounts of water?", "weight": 3.0},
            {"id": "frequent_urination", "question": "Are you waking up multiple times during the night to urinate?", "weight": 2.8}
        ],
        "gerd_acid_reflux": [
            {"id": "heartburn_burning_chest", "question": "Do you feel a burning sensation rising up behind your breastbone after eating?", "weight": 3.0},
            {"id": "sour_taste_in_mouth", "question": "Do you get an unpleasant sour or acid taste in your mouth, especially when lying down?", "weight": 2.5}
        ],
        "appendicitis": [
            {"id": "sudden_pain_lower_right_abdomen", "question": "Is the pain concentrated in your lower right abdomen, and does coughing or walking make it sharper?", "weight": 3.5}
        ],
        "hepatitis_jaundice": [
            {"id": "yellow_eyes_skin", "question": "Have you noticed any yellowish tint in the whites of your eyes or skin?", "weight": 3.5},
            {"id": "dark_urine", "question": "Has your urine turned dark brown or tea-colored?", "weight": 3.0}
        ],
        "uti": [
            {"id": "burning_pain_with_urination_dysuria", "question": "Do you feel a sharp stinging or burning sensation while urinating?", "weight": 3.5},
            {"id": "frequent_urination", "question": "Do you feel an urgent need to urinate even when your bladder is nearly empty?", "weight": 2.5}
        ]
    }

    def generate_questions(self, predictions: List[Dict[str, Any]], active_symptoms: List[str]) -> List[Dict[str, Any]]:
        """Generate up to 3 targeted yes/no questions for the user to confirm/refine the top diagnoses"""
        questions = []
        asked_symptoms = set(active_symptoms)

        for pred in predictions[:2]:
            dis_id = pred.get("id")
            if dis_id in self.DISEASE_DIFFERENTIATING_QUESTIONS:
                candidates = self.DISEASE_DIFFERENTIATING_QUESTIONS[dis_id]
                for q in candidates:
                    if q["id"] not in asked_symptoms and len(questions) < 3:
                        questions.append({
                            "symptom_token": q["id"],
                            "disease_target": pred.get("name"),
                            "question": q["question"]
                        })
                        asked_symptoms.add(q["id"])

        return questions
