"""
CarePulse Response Generator - Clinical Diagnostic and Conversational Engine
Integrates the Clinical Disease Predictor, Vitals Monitor, and LLM Providers.
"""
import re
import unicodedata
from typing import Dict, Any, Optional, List
from llm_providers import LLMProviderFactory
from engine.disease_predictor import DiseasePredictor
from engine.vitals_monitor import VitalsMonitor
from engine.follow_up_generator import FollowUpGenerator
import config

# Clinical and anatomical keywords used to validate medical domain relevance
CLINICAL_KEYWORDS = {
    # English keywords
    'pain', 'pains', 'paining', 'ache', 'aches', 'aching', 'sore', 'soreness', 'hurt', 'hurts', 'hurting',
    'swelling', 'swollen', 'swell', 'bleeding', 'bleed', 'bleeds', 'blood', 'bloody',
    'fever', 'fevers', 'feverish', 'temperature', 'pyrexia', 'cough', 'coughing', 'coughs', 'coughed',
    'cold', 'colds', 'chills', 'shivering', 'shiver', 'shivers', 'sweat', 'sweats', 'sweating', 'night sweats',
    'dizzy', 'dizziness', 'giddiness', 'giddy', 'vertigo', 'lightheaded', 'lightheadedness',
    'faint', 'fainting', 'nausea', 'nauseous', 'nauseated', 'vomit', 'vomiting', 'vomited', 'vomits',
    'throw up', 'throwing up', 'vomit sensation', 'vomiting sensation',
    'diarrhea', 'diarrhoea', 'motions', 'loose motion', 'loose motions', 'loose stool', 'loose stools',
    'watery stool', 'watery stools', 'motions problem', 'frequent motions', 'constipation',
    'food poisoning', 'stomach upset', 'upset stomach', 'indigestion',
    'cramp', 'cramps', 'cramping', 'burn', 'burning', 'burning sensation', 'itch', 'itching', 'itchy',
    'rash', 'rashes', 'wound', 'wounds', 'cut', 'cuts', 'bruise', 'bruises', 'pus', 'discharge',
    'fatigue', 'tired', 'tiredness', 'weak', 'weakness', 'exhaustion', 'exhausted', 'drowsy',
    'unwell', 'feeling unwell', 'not feeling well', 'not well', 'feeling sick', 'sick', 'sickness',
    'breath', 'breathing', 'breathless', 'breathlessness', 'shortness of breath', 'wheeze', 'wheezing',
    'chest', 'pressure', 'tight', 'tightness', 'chest tightness', 'spasm', 'spasms', 'stiffness', 'stiff',
    'numb', 'numbness', 'tingling', 'thirst', 'thirsty', 'appetite', 'weight', 'vision', 'blur', 'blurry',
    'hearing', 'earache', 'sleep', 'insomnia', 'infection', 'infected', 'allergy', 'allergic', 'allergies',
    'virus', 'viral', 'bacteria', 'bacterial', 'flu', 'influenza', 'phlegm', 'mucus', 'sputum',
    'sugar', 'glucose', 'bp', 'blood pressure', 'pulse', 'heart rate', 'palpitation', 'palpitations',
    'fast heartbeat', 'heart racing', 'headache', 'headaches', 'head pain', 'heavy head', 'head heaviness',
    'migraine', 'asthma', 'diabetes', 'cancer', 'covid', 'coronavirus', 'typhoid', 'malaria', 'dengue',
    'piles', 'hemorrhoids', 'sprain', 'gastric', 'gas trouble', 'gastric trouble', 'gastric problem',
    'acidity', 'heartburn', 'acid reflux', 'gerd',
    'head', 'brain', 'eye', 'eyes', 'ear', 'ears', 'nose', 'mouth', 'throat', 'neck',
    'shoulder', 'shoulders', 'heart', 'lung', 'lungs', 'rib', 'ribs', 'arm', 'arms',
    'hand', 'hands', 'finger', 'fingers', 'back', 'spine', 'abdomen', 'abdominal', 'stomach',
    'belly', 'pelvis', 'pelvic', 'hip', 'hips', 'groin', 'leg', 'legs', 'thigh', 'knee',
    'knees', 'calf', 'ankle', 'ankles', 'foot', 'feet', 'toe', 'toes', 'skin', 'urine',
    'urinating', 'urination', 'pee', 'peeing', 'stool', 'bowel', 'bone', 'bones', 'joint',
    'joints', 'muscle', 'muscles', 'nerve', 'nerves', 'vein', 'veins', 'artery', 'liver',
    'kidney', 'kidneys', 'medicine', 'medicines', 'medication', 'medications', 'drug', 'drugs',
    'pill', 'pills', 'tablet', 'tablets', 'prescription', 'treatment', 'treatments',
    'ill', 'illness', 'disease', 'diseases', 'symptom', 'symptoms', 'syndrome', 'emergency',
    'paracetamol', 'aspirin', 'ibuprofen', 'antibiotic', 'antibiotics', 'inhaler', 'insulin',

    # Kannada keywords (native script)
    'ನೋವು', 'ಉರಿ', 'ಜ್ವರ', 'ಕೆಮ್ಮು', 'ಶೀತ', 'ನೆಗಡಿ', 'ಚಳಿ', 'ನಡುಕ', 'ಬೆವರು',
    'ತಲೆಸುತ್ತು', 'ವಾಂತಿ', 'ವಾಕರಿಕೆ', 'ಬೇದಿ', 'ಅತಿಸಾರ', 'ಮಲಬದ್ಧತೆ', 'ಸೆಳೆತ', 'ತುರಿಕೆ',
    'ದದ್ದು', 'ಗಾಯ', 'ಕೀವು', 'ಸುಸ್ತು', 'ಆಯಾಸ', 'ದಣಿವು', 'ನಿಶ್ಯಕ್ತಿ', 'ಉಸಿರಾಟ',
    'ದಮ್ಮು', 'ಉಬ್ಬಸ', 'ಬಿಗಿತ', 'ಮರಗಟ್ಟುವಿಕೆ', 'ಬಾಯಾರಿಕೆ', 'ಹಸಿವು', 'ತೂಕ', 'ದೃಷ್ಟಿ',
    'ನಿದ್ದೆ', 'ಸೋಂಕು', 'ಅಲರ್ಜಿ', 'ಕಫ', 'ಲೋಳೆ', 'ತಲೆ', 'ಕಣ್ಣು', 'ಕಿವಿ', 'ಮೂಗು',
    'ಬಾಯಿ', 'ಗಂಟಲು', 'ಕುತ್ತಿಗೆ', 'ಎದೆ', 'ಹೃದಯ', 'ಶ್ವಾಸಕೋಶ', 'ತೋಳು', 'ಕೈ', 'ಬೆರಳು',
    'ಬೆನ್ನು', 'ಹೊಟ್ಟೆ', 'ಸೊಂಟ', 'ಕಾಲು', 'ಮಂಡಿ', 'ಪಾದ', 'ಚರ್ಮ', 'ರಕ್ತ', 'ಮೂತ್ರ',
    'ಮಲ', 'ಮೂಳೆ', 'ಕೀಲು', 'ಸ್ನಾಯು', 'ನರ', 'ಔಷಧ', 'ಮಾತ್ರೆ', 'ಗುಳಿಗೆ', 'ಚಿಕಿತ್ಸೆ',
    'ಆರೋಗ್ಯ', 'ರೋಗ', 'ಕಾಯಿಲೆ', 'ತುರ್ತು', 'ಹುಷಾರಿಲ್ಲ', 'ಆರಾಮ ಇಲ್ಲ', 'ಅಜೀರ್ಣ',
    'ಮೂಲವ್ಯಾಧಿ', 'ವಿಷಾಹಾರ', 'ಹೊಟ್ಟೆ ಕೆಟ್ಟಿದೆ', 'ಮೈ ಕೈ ನೋವು', 'ಮೈಕೈನೋವು', 'ತಲೆ ಭಾರ',
    'ಕಾಲಿನಲ್ಲಿ ನೋವು', 'ಕೈಯಲ್ಲಿ ನೋವು', 'ಬೆನ್ನಿನಲ್ಲಿ ನೋವು', 'ಹೊಟ್ಟೆಯಲ್ಲಿ ನೋವು', 'ಎದೆಯಲ್ಲಿ ನೋವು',
    'ಜ್ವರ ಬಂದಿದೆ', 'ಕೆಮ್ಮು ಬರ್ತಿದೆ', 'ವಾಂತಿ ಆಗ್ತಿದೆ', 'ಬೇದಿ ಆಗ್ತಿದೆ', 'ನೆಗಡಿ ಆಗಿದೆ',

    # Transliterated Kanglish keywords
    'jwara', 'jvara', 'talenovu', 'tale novu', 'thale novu', 'thalenovu', 'kemmu', 'sheetha', 'sheeta',
    'negadi', 'chali', 'vaanthi', 'vaanti', 'vanti', 'vakarike', 'bedi', 'bhedi', 'hotte novu', 'hottenovu',
    'ede novu', 'edenovu', 'susthu', 'sustu', 'ayasa', 'maikai novu', 'mai kai novu', 'maikainovu',
    'keelu novu', 'bennu novu', 'bennunovu', 'gantalu novu', 'gantlu novu', 'usirata', 'kaalu novu',
    'kalu novu', 'kalunovu', 'kaalunovu', 'mandi novu', 'mandinovu', 'kai novu', 'raktha', 'matre',
    'roga', 'hushaarilla', 'husharilla', 'arama illa', 'aarama illa',

    # Hindi keywords
    'बुखार', 'सिरदर्द', 'खांसी', 'जुकाम', 'सर्दी', 'दर्द', 'उल्टी', 'दस्त', 'कमजोरी',
    'चक्कर', 'पेट दर्द', 'सीने में दर्द', 'गले में खराश', 'बदन दर्द', 'तबीयत खराब', 'बीमार',
    'tabiyat kharab', 'bimar', 'sirdard', 'pet dard', 'dast', 'ulti', 'chakkar', 'kamzori', 'badan dard'
}

GREETING_WORDS = {
    'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening',
    'namaste', 'namaskara', 'namaskar', 'ನಮಸ್ಕಾರ', 'ಹಲೋ', 'ಹಾಯ್', 'who are you', 'help',
    'how are you', 'how do you do', 'what can you do',
    'hello doctor', 'hi doctor', 'hey doctor', 'hello doc', 'hi doc', 'good morning doctor'
}

class MedicalResponseGenerator:
    """Generates structured medical responses with integrated disease predictions"""

    def __init__(self):
        try:
            self.llm_provider = LLMProviderFactory.get_provider()
        except Exception:
            self.llm_provider = None

        self.predictor = DiseasePredictor()
        self.vitals_monitor = VitalsMonitor()
        self.follow_up_gen = FollowUpGenerator()

    def classify_clinical_input(self, text: str, symptoms_list: list = None, vitals: dict = None) -> str:
        """
        Classifies incoming input into 'clinical', 'greeting', or 'invalid'.
        Guarantees that only valid medical symptoms or clinical concerns receive diagnoses.
        """
        text_str = (text or '').strip()
        has_text = bool(text_str)
        has_symptoms = bool(symptoms_list and len(symptoms_list) > 0)
        has_vitals = bool(vitals and any(vitals.get(k) is not None for k in ['systolic_bp', 'heart_rate', 'spo2', 'temperature', 'blood_sugar']))

        if not has_text and not has_symptoms and not has_vitals:
            return 'invalid'

        # If user explicitly provided a text message, validate the text message first!
        if has_text:
            # 1. Reject pure numbers or punctuation-only inputs (e.g. "552", "12345", "!@#")
            has_letters = any(unicodedata.category(c).startswith('L') for c in text_str)
            if not has_letters:
                return 'invalid'

            # Normalize text while preserving unicode letters
            cleaned = ''.join(' ' if unicodedata.category(c).startswith(('P', 'S')) else c for c in text_str.lower())
            clean_text = ' ' + ' '.join(cleaned.split()) + ' '
            raw_clean = clean_text.strip()

            # 2. Check for polite greetings first (exact or common greeting phrases)
            greeting_patterns = [
                r'^(?:hello|hi|hey|greetings|good\s+(?:morning|afternoon|evening)|namaste|namaskara|namaskar|ಹಲೋ|ಹಾಯ್|ನಮಸ್ಕಾರ)(?:\s+(?:doctor|doc|there|assistant|carepulse|bot|ವೈದ್ಯರೇ))?[!\.\?\s]*$',
                r'^(?:who\s+are\s+you|what\s+can\s+you\s+do|how\s+are\s+you|help)[!\.\?\s]*$'
            ]
            for gp in greeting_patterns:
                if re.match(gp, raw_clean, re.IGNORECASE):
                    return 'greeting'

            for gr in sorted(GREETING_WORDS, key=len, reverse=True):
                if raw_clean == gr:
                    return 'greeting'

            # 3. Check for recognized symptoms via disease predictor
            extracted = self.predictor.extract_symptoms_from_text(text_str)
            if extracted and len(extracted) > 0:
                return 'clinical'

            # 4. Check for clinical and health vocabulary keywords
            for kw in sorted(CLINICAL_KEYWORDS, key=len, reverse=True):
                pattern = r'(?:\s|^)' + re.escape(kw.lower()) + r'(?:\s|$)'
                if re.search(pattern, clean_text, re.IGNORECASE):
                    return 'clinical'

            # If the user explicitly typed a message and it lacks medical content/symptoms:
            # It is invalid!
            return 'invalid'

        # If no text was entered, but valid symptom chips or vitals were provided
        if has_symptoms or has_vitals:
            return 'clinical'

        return 'invalid'

    def _build_invalid_input_response(self, language: str = 'english') -> Dict[str, Any]:
        """Generate clear localized notice when user inputs non-medical or invalid text"""
        lang = (language or 'english').lower()
        if lang == 'kannada':
            return {
                'summary': "ನಮೂದಿಸಿದ ಮಾಹಿತಿ ಅಮಾನ್ಯವಾಗಿದೆ (Input is not valid). ದಯವಿಟ್ಟು ಸರಿಯಾದ ಆರೋಗ್ಯ ರೋಗಲಕ್ಷಣ ಅಥವಾ ಸಮಸ್ಯೆಯನ್ನು ನಮೂದಿಸಿ (ಉದಾಹರಣೆಗೆ: 'ನನಗೆ ಜ್ವರ ಮತ್ತು ತಲೆನೋವು ಇದೆ' ಅಥವಾ 'ಕೆಮ್ಮು ಮತ್ತು ಎದೆ ನೋವು').",
                'home_care': "ಮಾನ್ಯವಾದ ರೋಗಲಕ್ಷಣಗಳನ್ನು ನಮೂದಿಸಿದಾಗ ಮಾತ್ರ ಸೂಕ್ತ ಆರೈಕೆ ಸಲಹೆಗಳನ್ನು ನೀಡಲಾಗುತ್ತದೆ. ದಯವಿಟ್ಟು ಸರಿಯಾದ ರೋಗಲಕ್ಷಣಗಳನ್ನು ತಿಳಿಸಿ.",
                'medical_attention': "ತುರ್ತು ವೈದ್ಯಕೀಯ ಪರಿಸ್ಥಿತಿಯಲ್ಲಿದ್ದರೆ ತಕ್ಷಣ 108 ಅಥವಾ 112 ಗೆ ಕರೆ ಮಾಡಿ ಆಸ್ಪತ್ರೆಗೆ ತೆರಳಿ.",
                'possible_causes': "ನಮೂದಿಸಿದ ಮಾಹಿತಿಯಲ್ಲಿ ಯಾವುದೇ ವೈದ್ಯಕೀಯ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲವಾದ್ದರಿಂದ ರೋಗನಿರ್ಣಯ ಲಭ್ಯವಿಲ್ಲ.",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': False
            }
        elif lang == 'hindi':
            return {
                'summary': "दर्ज किया गया इनपुट अमान्य है (Input is not valid)। कृपया वैध स्वास्थ्य लक्षण या समस्या दर्ज करें (जैसे: 'मुझे तेज बुखार और सिरदर्द है' या 'खांसी और सीने में दर्द')।",
                'home_care': "उचित घरेलू देखभाल केवल मान्य लक्षणों के लिए दी जाती है। कृपया अपने लक्षण स्पष्ट रूप से बताएं।",
                'medical_attention': "यदि यह एक आपातकालीन स्थिति है, तो तुरंत आपातकालीन सेवाओं (108/112) से संपर्क करें।",
                'possible_causes': "अमान्य इनपुट के कारण किसी भी रोग का मूल्यांकन नहीं किया जा सका।",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': False
            }
        elif lang == 'telugu':
            return {
                'summary': "నమోదు చేసిన సమాచారం చెల్లదు (Input is not valid). దయచేసి సరైన ఆరోగ్య లక్షణాలను నమోదు చేయండి (ఉదాహరణకు: 'నాకు తీవ్ర జ్వరం మరియు తలనొప్పి ఉంది').",
                'home_care': "సరైన లక్షణాలు తెలిపినప్పుడు మాత్రమే గృహ సంరక్షణ సూచనలు అందించబడతాయి.",
                'medical_attention': "అత్యవసర పరిస్థితి ఉంటే వెంటనే 108 లేదా 112 కి కాల్ చేయండి.",
                'possible_causes': "నమోదు చేసిన సమాచారంలో ఎటువంటి వైద్య లక్షణాలు లేనందున నిర్ధారణ సాధ్యం కాలేదు.",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': False
            }
        elif lang in ('spanish', 'español'):
            return {
                'summary': "La entrada ingresada no es válida (Input is not valid). Por favor ingrese síntomas médicos válidos (por ejemplo: 'Tengo fiebre y dolor de cabeza').",
                'home_care': "Las instrucciones de cuidado solo se generan para síntomas clínicos válidos.",
                'medical_attention': "En caso de emergencia médica, comuníquese inmediatamente con el 911 o centro de urgencias.",
                'possible_causes': "No se pudieron evaluar afecciones clínicas porque la entrada no contiene síntomas médicos válidos.",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': False
            }
        elif lang in ('french', 'français'):
            return {
                'summary': "L'entrée fournie n'est pas valide (Input is not valid). Veuillez saisir des symptômes médicaux valides (par exemple: 'J'ai de la fièvre et des maux de tête').",
                'home_care': "Les conseils de soins à domicile ne sont générés que pour des symptômes cliniques reconnus.",
                'medical_attention': "En cas d'urgence médicale, contactez immédiatement les services de secours (112 / 15).",
                'possible_causes': "Aucune affection n'a pu être évaluée car l'entrée ne correspond à aucun symptôme médical.",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': False
            }
        else:
            return {
                'summary': "Input is not valid. Please enter a valid medical symptom, health condition, or clinical description (for example: 'I have high fever and headache' or 'cough with chest pain') to receive clinical evaluation.",
                'home_care': "Home care instructions are only generated for recognized clinical symptoms. Please provide valid health symptoms.",
                'medical_attention': "If you are experiencing a medical emergency, please dial emergency services immediately (911 / 112 / 108).",
                'possible_causes': "No clinical conditions could be evaluated because the entered input was not recognized as a medical symptom or question.",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': False
            }

    def _build_greeting_response(self, language: str = 'english') -> Dict[str, Any]:
        """Generate welcoming response guiding user to enter medical symptoms"""
        lang = (language or 'english').lower()
        if lang == 'kannada':
            return {
                'summary': "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಕೇರ್‌ಪಲ್ಸ್ ಕ್ಲಿನಿಕಲ್ ಕನ್ಸಲ್ಟೆಂಟ್. ನಿಮ್ಮ ಆರೋಗ್ಯ ತಪಾಸಣೆ ಮತ್ತು ಸಲಹೆಗಾಗಿ ದಯವಿಟ್ಟು ನಿಮ್ಮ ರೋಗಲಕ್ಷಣಗಳನ್ನು ವಿವರಿಸಿ (ಉದಾಹರಣೆಗೆ: 'ನನಗೆ ಜ್ವರ ಮತ್ತು ಮೈಕೈ ನೋವು ಇದೆ').",
                'home_care': "ವೈಯಕ್ತಿಕ ಆರೈಕೆ ಸಲಹೆಗಳನ್ನು ಪಡೆಯಲು ನಿಮ್ಮ ರೋಗಲಕ್ಷಣಗಳನ್ನು ನಮೂದಿಸಿ.",
                'medical_attention': "ತೀವ್ರ ಉಸಿರಾಟದ ತೊಂದರೆ ಅಥವಾ ಎದೆ ನೋವು ಇದ್ದಲ್ಲಿ ತಕ್ಷಣ ತುರ್ತು ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ.",
                'possible_causes': "ಮೌಲ್ಯಮಾಪನಕ್ಕೆ ಸಿದ್ಧವಾಗಿದೆ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ರೋಗಲಕ್ಷಣಗಳನ್ನು ತಿಳಿಸಿ.",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': True,
                'input_type': 'greeting'
            }
        elif lang == 'hindi':
            return {
                'summary': "नमस्ते! मैं आपका केयरपल्स क्लिनिकल सहायक हूं। क्लिनिकल मूल्यांकन शुरू करने के लिए कृपया अपने लक्षण बताएं (जैसे: 'मुझे तेज बुखार और सिरदर्द है')।",
                'home_care': "लक्षण बताने पर आपको उचित घरेलू देखभाल मार्गदर्शन दिया जाएगा।",
                'medical_attention': "गंभीर लक्षणों के लिए तुरंत अस्पताल जाएं।",
                'possible_causes': "मूल्यांकन के लिए तैयार। कृपया अपने लक्षण दर्ज करें।",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': True,
                'input_type': 'greeting'
            }
        else:
            return {
                'summary': "Hello! I am your CarePulse Clinical Consultant. Please describe your health symptoms, medical concerns, or select symptoms from the list to begin clinical evaluation (for example: 'I have fever and body pain').",
                'home_care': "Describe your symptoms to receive personalized, age-appropriate home care instructions.",
                'medical_attention': "For severe symptoms such as difficulty breathing or intense chest pressure, seek emergency medical care immediately.",
                'possible_causes': "Ready to evaluate. Please enter symptoms or select from the symptoms list to begin.",
                'disclaimer': self._get_disclaimer(language),
                'is_valid': True,
                'input_type': 'greeting'
            }

    def generate_medical_response(
        self,
        symptoms: str,
        age: str,
        language: str = 'english',
        conversation_history: list = None,
        symptoms_list: list = None,
        vitals: dict = None
    ) -> Dict[str, Any]:
        """
        Generate structured clinical response with disease prediction and health guidance.
        Validates that user input is medically relevant before producing diagnoses.
        """
        # Validate input validity
        input_type = self.classify_clinical_input(symptoms, symptoms_list, vitals)

        if input_type == 'invalid':
            invalid_response = self._build_invalid_input_response(language)
            return {
                'success': False,
                'is_valid': False,
                'input_type': 'invalid',
                'error': invalid_response['summary'],
                'response': invalid_response,
                'disease_prediction': None,
                'raw_response': 'Input Validation'
            }

        if input_type == 'greeting':
            greeting_response = self._build_greeting_response(language)
            return {
                'success': True,
                'is_valid': True,
                'input_type': 'greeting',
                'response': greeting_response,
                'disease_prediction': None,
                'raw_response': 'Clinical Greeting'
            }

        # Run disease prediction engine for valid clinical input
        prediction_result = self.predictor.predict(
            symptoms=symptoms_list or [],
            age=age or 'Adult',
            text_input=symptoms or ''
        )

        # Analyze vitals if provided
        vitals_result = None
        if vitals:
            vitals_result = self.vitals_monitor.analyze_vitals(
                systolic_bp=vitals.get('systolic_bp'),
                diastolic_bp=vitals.get('diastolic_bp'),
                heart_rate=vitals.get('heart_rate'),
                spo2=vitals.get('spo2'),
                temperature=vitals.get('temperature'),
                temp_unit=vitals.get('temp_unit', 'F'),
                blood_sugar=vitals.get('blood_sugar'),
                sugar_type=vitals.get('sugar_type', 'random')
            )

        # Generate follow-up questions
        follow_ups = []
        if prediction_result.get('success'):
            follow_ups = self.follow_up_gen.generate_questions(
                prediction_result.get('all_predictions', []),
                prediction_result.get('active_symptom_tokens', [])
            )

        # 1. If a valid live LLM provider is available, use it with enriched clinical context
        if self.llm_provider and self.llm_provider.is_available():
            try:
                primary = prediction_result.get('primary_diagnosis', {})
                clinical_context = (
                    f"Clinical Disease Engine Prediction:\n"
                    f"- Primary Diagnosis: {primary.get('name')} (Confidence: {primary.get('confidence')}%)\n"
                    f"- Matched Symptoms: {', '.join(primary.get('matched_symptoms', []))}\n"
                    f"- Urgency Level: {prediction_result.get('urgency')}\n"
                )
                if vitals_result and vitals_result.get('has_data'):
                    clinical_context += f"- Vitals Status: {vitals_result.get('overall_status')}\n"

                user_prompt = f"""Patient Age Group: {age}
Patient Symptoms: {symptoms}

{clinical_context}

Please provide medical guidance in the following structured format:
(A) Brief Summary of the Symptoms & Primary Clinical Assessment
(B) Home Care Recommendations (age-appropriate)
(C) When to Seek Medical Attention & Red Flags
(D) Possible Causes & Differential Diagnosis"""

                if conversation_history:
                    history_context = "\nPrevious conversation context:\n"
                    for msg in conversation_history[-4:]:
                        history_context += f"{msg.get('role')}: {msg.get('content')}\n"
                    user_prompt = history_context + "\n" + user_prompt

                system_prompt = self.get_system_prompt(language)
                raw_response = self.llm_provider.generate_response(prompt=user_prompt, system_prompt=system_prompt)
                structured = self._parse_response(raw_response)

                structured['disclaimer'] = self._get_disclaimer(language)
                structured['disease_prediction'] = prediction_result
                structured['follow_up_questions'] = follow_ups
                if vitals_result:
                    structured['vitals_analysis'] = vitals_result

                structured['is_valid'] = True
                structured['input_type'] = 'clinical'

                return {
                    'success': True,
                    'is_valid': True,
                    'input_type': 'clinical',
                    'response': structured,
                    'disease_prediction': prediction_result,
                    'raw_response': raw_response
                }
            except Exception as e:
                print(f"Notice: Live LLM call failed ({e}). Using Clinical Knowledge Engine.")

        # 2. Local Clinical Knowledge Engine (Offline Mode)
        structured_response = self._build_clinical_response(
            prediction_result=prediction_result,
            vitals_result=vitals_result,
            symptoms=symptoms,
            age=age,
            language=language,
            follow_ups=follow_ups
        )
        structured_response['is_valid'] = True
        structured_response['input_type'] = 'clinical'

        return {
            'success': True,
            'is_valid': True,
            'input_type': 'clinical',
            'response': structured_response,
            'disease_prediction': prediction_result,
            'raw_response': 'Clinical Knowledge Engine'
        }

    def _build_clinical_response(
        self,
        prediction_result: Dict[str, Any],
        vitals_result: Optional[Dict[str, Any]],
        symptoms: str,
        age: str,
        language: str = 'english',
        follow_ups: list = None
    ) -> Dict[str, Any]:
        """Build structured patient-friendly clinical response from prediction engine"""
        primary = prediction_result.get('primary_diagnosis') or {}
        differentials = prediction_result.get('differential_diagnoses', [])
        urgency = prediction_result.get('urgency', 'mild')
        emergency_flags = prediction_result.get('emergency_flags', [])

        has_primary = bool(primary.get('name'))
        dis_name = primary.get('name', 'General Symptom Evaluation')
        confidence = primary.get('confidence', 0.0)
        matched = primary.get('matched_symptoms', [])

        # Section A: Summary & Assessment
        matched_str = ", ".join(matched) if matched else (symptoms or 'Reported symptoms')
        if has_primary:
            summary = (
                f"CLINICAL ASSESSMENT FOR {str(age).upper()} PATIENT:\n"
                f"Based on reported symptoms ({matched_str}), the primary suspected condition is "
                f"**{dis_name}** with a calculated **{confidence}% clinical match**."
            )
        else:
            summary = (
                f"CLINICAL ASSESSMENT FOR {str(age).upper()} PATIENT:\n"
                f"Based on reported symptoms ({matched_str}), no single condition reached primary diagnostic certainty. "
                f"A general clinical evaluation is recommended."
            )

        if differentials:
            diff_names = [f"{d['name']} ({d['confidence']}%)" for d in differentials[:2]]
            summary += f"\nDifferential considerations include: {', '.join(diff_names)}."

        if vitals_result and vitals_result.get('has_data'):
            summary += f"\nVitals Status: {vitals_result.get('overall_status')}."

        # Section B: Home Care
        home_care_list = primary.get('home_care', [
            "Maintain generous fluid intake with oral rehydration salts, broths, and clean water.",
            "Ensure complete physical rest to support immune function.",
            "Keep ambient room temperature comfortable and well-ventilated."
        ])
        home_care = "\n".join([f"• {item}" if not item.startswith("•") else item for item in home_care_list])

        # Add Age-Specific Safety Notes
        age_lower = str(age).lower()
        if "infant" in age_lower or "0-2" in age_lower:
            home_care += "\n• [PEDIATRIC SAFETY] Never administer honey to infants under 12 months (infantile botulism risk). Do NOT administer adult medications."
        elif "child" in age_lower or "2-12" in age_lower:
            home_care += "\n• [PEDIATRIC SAFETY] Never administer aspirin to children or teenagers due to Reye's syndrome risk."
        elif "senior" in age_lower or "65+" in age_lower:
            home_care += "\n• [SENIOR CARE] Ensure fall prevention, adequate hydration, and review interactions with ongoing chronic medications."

        # Section C: When to Seek Medical Attention & Red Flags
        medical_attention = f"URGENCY LEVEL: {urgency.upper()}\n"

        if emergency_flags:
            medical_attention += "\n".join(emergency_flags) + "\n\n"

        red_flags = primary.get('red_flags', [])
        if red_flags:
            medical_attention += "Watch for the following Warning Signs:\n"
            for rf in red_flags:
                medical_attention += f"• {rf}\n"

        when_doc = primary.get('when_to_see_doctor', 'Consult a doctor if symptoms persist past 48-72 hours or intensify.')
        medical_attention += f"\nClinical Recommendation: {when_doc}"

        if vitals_result and vitals_result.get('alerts'):
            medical_attention += "\n\nVitals Alerts:\n" + "\n".join(vitals_result['alerts'])

        # Section D: Possible Causes & Detailed Background
        possible_causes = (
            f"Primary Pathophysiology: {primary.get('description', 'Acute symptomatic manifestation.')}\n\n"
            f"Recommended Tests / Confirmation: Consult a physician for formal clinical verification "
            f"and diagnostic confirmation."
        )

        # Multi-language translation support
        lang_lower = language.lower()
        if lang_lower in ('spanish', 'español'):
            summary = (
                f"EVALUACIÓN CLÍNICA PARA PACIENTE ({str(age).upper()}):\n"
                f"Basado en los síntomas informados ({matched_str}), la afección primaria sospechada es "
                f"**{dis_name}** con un **{confidence}% de coincidencia clínica**."
            )
            home_care = (
                "• Mantenga una hidratación abundante con sales de rehidratación oral y agua potable.\n"
                "• Descanse completamente para apoyar la recuperación inmunitaria.\n"
                "• Mantenga un ambiente ventilado y una temperatura ambiente confortable."
            )
            medical_attention = (
                f"NIVEL DE URGENCIA: {urgency.upper()}\n"
                "Busque atención médica de emergencia si experimenta dificultad para respirar, dolor torácico severo o fiebre persistente alta."
            )
            possible_causes = (
                f"Causa primaria sospechada: {dis_name}.\n"
                f"Consulte a un médico colegiado para confirmación diagnóstica y prescripción formal."
            )
        elif lang_lower in ('french', 'français'):
            summary = (
                f"ÉVALUATION CLINIQUE DU PATIENT ({str(age).upper()}):\n"
                f"D'après les symptômes signalés ({matched_str}), l'affection principale suspectée est "
                f"**{dis_name}** avec une **concordance clinique de {confidence}%**."
            )
            home_care = (
                "• Maintenir une hydratation abondante avec des solutions de réhydratation orale et de l'eau.\n"
                "• Observer un repos physique complet pour favoriser la guérison.\n"
                "• Veiller à un environnement bien aéré à température tempérée."
            )
            medical_attention = (
                f"NIVEAU D'URGENCE: {urgency.upper()}\n"
                "Consultez immédiatement un service d'urgence en cas de détresse respiratoire ou de douleur thoracique aiguë."
            )
            possible_causes = (
                f"Pathologie suspectée: {dis_name}.\n"
                f"Consultez un médecin pour confirmer le diagnostic et recevoir un traitement adapté."
            )
        elif lang_lower == 'hindi':
            if has_primary:
                summary = f"लक्षणों का नैदानिक मूल्यांकन: '{matched_str}' ({age} के लिए)। संभावित स्थिति: **{dis_name}** ({confidence}% मिलान)।"
            else:
                summary = f"लक्षणों का नैदानिक मूल्यांकन: '{matched_str}' ({age} के लिए)। किसी एक विशिष्ट रोग का पूर्ण मिलान नहीं मिला। सामान्य चिकित्सकीय परामर्श की सलाह दी जाती है।"
            home_care = "• पर्याप्त मात्रा में ओआरएस, सूप और पानी पिएं।\n• पूर्ण शारीरिक आराम करें।\n• डॉक्टर के परामर्श के बिना कोई नई दवा न लें।"
            medical_attention = f"गंभीरता स्तर: {urgency.upper()}\nयदि सांस लेने में कठिनाई, तेज बुखार या तीव्र दर्द हो तो तुरंत अस्पताल जाएं।"
            possible_causes = f"संभावित कारण: {dis_name}। सटीक निदान के लिए रक्त परीक्षण या डॉक्टर से परामर्श आवश्यक है।"
        elif lang_lower == 'telugu':
            if has_primary:
                summary = f"లక్షణాల విశ్లేషణ: '{matched_str}' ({age} కొరకు). ప్రాథమిక రోగ నిర్ధారణ: **{dis_name}** ({confidence}% సరిపోలిక)."
            else:
                summary = f"లక్షణాల విశ్లేషణ: '{matched_str}' ({age} కొరకు). నిర్దిష్ట వ్యాధి నిర్ధారణ కాలేదు. సాధారణ వైద్య పరీక్ష అవసరం."
            home_care = "• తగినంత ఓఆర్‌ఎస్ మరియు ద్రవపదార్థాలు తీసుకోండి.\n• సరైన విశ్రాంతి తీసుకోండి.\n• వైద్యుని సలహా లేకుండా మందులు వాడవద్దు."
            medical_attention = f"తీవ్రత స్థాయి: {urgency.upper()}\nశ్వాస తీసుకోవడంలో ఇబ్బంది లేదా అధిక జ్వరం ఉంటే వెంటనే ఆసుపత్రిని సంప్రదించండి."
            possible_causes = f"సంభావ్య కారణం: {dis_name}. ఖచ్చితమైన నిర్ధారణ కోసం వైద్యుడిని సంప్రదించండి."
        elif lang_lower == 'kannada':
            if has_primary:
                summary = f"ರೋಗಲಕ್ಷಣಗಳ ವೈದ್ಯಕೀಯ ಮೌಲ್ಯಮಾಪನ: '{matched_str}' ({age} ರೋಗಿಗೆ). ಪ್ರಾಥಮಿಕ ಶಂಕಿತ ರೋಗ: **{dis_name}** ({confidence}% ಹೊಂದಾಣಿಕೆ)."
            else:
                summary = f"ರೋಗಲಕ್ಷಣಗಳ ವೈದ್ಯಕೀಯ ಮೌಲ್ಯಮಾಪನ: '{matched_str}' ({age} ರೋಗಿಗೆ). ಯಾವುದೇ ನಿರ್ದಿಷ್ಟ ಕಾಯಿಲೆಯೊಂದಿಗೆ ಪೂರ್ಣ ಹೊಂದಾಣಿಕೆ ಕಂಡುಬಂದಿಲ್ಲ. ವೈದ್ಯಕೀಯ ತಪಾಸಣೆ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ."
            home_care = "• ಸಾಕಷ್ಟು ಓಆರ್‌ಎಸ್, ಸೂಪ್ ಮತ್ತು ಶುದ್ಧ ನೀರನ್ನು ಸೇವಿಸಿ ನಿರ್ಜಲೀಕರಣ ತಪ್ಪಿಸಿ.\n• ರೋಗನಿರೋಧಕ ಶಕ್ತಿ ಹೆಚ್ಚಿಸಲು ಸಂಪೂರ್ಣ ದೈಹಿಕ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ.\n• ವೈದ್ಯರ ಸಲಹೆಯಿಲ್ಲದೆ ಯಾವುದೇ ಆಂಟಿಬಯೋಟಿಕ್ ಅಥವಾ ಔಷಧಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಬೇಡಿ."
            medical_attention = f"ತುರ್ತು ಮಟ್ಟ: {urgency.upper()}\nಉಸಿರಾಟದ ತೊಂದರೆ, ತೀವ್ರ ಜ್ವರ ಅಥವಾ ಅತಿಯಾದ ಎದೆ ನೋವು ಕಂಡುಬಂದರೆ ತಕ್ಷಣ ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ."
            possible_causes = f"ಸಾಧ್ಯವಿರುವ ಕಾರಣ: {dis_name}.\nಖಚಿತವಾದ ರೋಗನಿರ್ಣಯಕ್ಕಾಗಿ ನೋಂದಾಯಿತ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ ರಕ್ತ ಪರೀಕ್ಷೆ ಮಾಡಿಸಿಕೊಳ್ಳಿ."

        return {
            'summary': summary,
            'home_care': home_care,
            'medical_attention': medical_attention,
            'possible_causes': possible_causes,
            'disclaimer': self._get_disclaimer(language),
            'disease_prediction': prediction_result,
            'follow_up_questions': follow_ups or [],
            'vitals_analysis': vitals_result
        }

    def get_system_prompt(self, language: str = 'english') -> str:
        """Get system prompt in appropriate language"""
        return f"""You are CarePulse, an advanced clinical medical health assistant.
Provide evidence-based medical information, differential disease predictions, and home care advice in {language}.
Always format responses into:
(A) Brief Summary of the Symptoms & Primary Clinical Assessment
(B) Home Care Recommendations
(C) When to Seek Medical Attention & Red Flags
(D) Possible Causes & Differential Diagnosis
Emphasize patient safety and always include age-appropriate guidance."""

    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse LLM response into structured format"""
        structured = {
            'summary': '',
            'home_care': '',
            'medical_attention': '',
            'possible_causes': ''
        }

        sections = {
            'summary': ['(A)', 'Brief Summary', 'Summary of the Symptoms'],
            'home_care': ['(B)', 'Home Care', 'Home Care Recommendations'],
            'medical_attention': ['(C)', 'When to Seek Medical Attention', 'Seek Medical Attention'],
            'possible_causes': ['(D)', 'Possible Causes', 'Causes']
        }

        lines = response.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line_upper = line.upper()
            found_section = False
            for section_name, markers in sections.items():
                for marker in markers:
                    if marker.upper() in line_upper:
                        if current_section:
                            structured[current_section] = '\n'.join(current_content).strip()
                        current_section = section_name
                        current_content = [line]
                        found_section = True
                        break
                if found_section:
                    break

            if not found_section and current_section:
                current_content.append(line)

        if current_section:
            structured[current_section] = '\n'.join(current_content).strip()

        if not any(structured.values()):
            structured['summary'] = response

        return structured

    def _get_disclaimer(self, language: str = 'english') -> str:
        """Get medical safety disclaimer"""
        disclaimers = {
            'english': "IMPORTANT DISCLAIMER: This assessment is generated for educational and informational purposes only and does not replace a formal doctor's diagnosis. If you are experiencing severe symptoms or a medical emergency, call your local emergency services (911 / 108 / 112) immediately.",
            'kannada': "ಪ್ರಮುಖ ಹಕ್ಕುತ್ಯಾಗ: ಈ ಮೌಲ್ಯಮಾಪನವು ಕೇವಲ ಶೈಕ್ಷಣಿಕ ಮತ್ತು ಮಾಹಿತಿ ಉದ್ದೇಶಗಳಿಗಾಗಿ ಮಾತ್ರವಾಗಿದ್ದು, ವೈದ್ಯರ ಔಪಚಾರಿಕ ರೋಗನಿರ್ಣಯವನ್ನು ಬದಲಾಯಿಸುವುದಿಲ್ಲ. ತುರ್ತು ಪರಿಸ್ಥಿತಿಯಲ್ಲಿ ತಕ್ಷಣವೇ ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ (108 / 112).",
            'spanish': "AVISO IMPORTANTE: Esta evaluación se genera únicamente con fines educativos e informativos y no reemplaza el diagnóstico de un médico. Si presenta una emergencia, llame de inmediato a los servicios médicos.",
            'french': "AVERTISSEMENT IMPORTANT: Cette évaluation est fournie à titre informatif et ne remplace pas une consultation médicale formelle. En cas d'urgence, contactez les services de secours.",
            'hindi': "महत्वपूर्ण अस्वीकरण: यह मूल्यांकन केवल शैक्षिक और सूचनात्मक उद्देश्यों के लिए है और डॉक्टर के निदान का स्थान नहीं लेता है। आपात स्थिति में तुरंत अस्पताल जाएं।",
            'telugu': "ముఖ్యమైన నిరాకరణ: ఈ సమాచారం కేవలం అవగాహన కొరకు మాత్రమే మరియు వైద్యుని అధికారిక రోగ నిర్ధారణను భర్తీ చేయదు. అత్యవసర పరిస్థితుల్లో వెంటనే వైద్యుడిని సంప్రదించండి.",
            'tamil': "முக்கியமான மறுப்பு: இந்த தகவல் தகவல் நோக்கங்களுக்காக மட்டுமே. சரியான மருத்துவ மதிப்பீட்டிற்கு மருத்துவரை அணுகவும்.",
            'bengali': "গুরুত্বপূর্ণ দাবিত্যাগ: এই তথ্য শুধুমাত্র তথ্যের উদ্দেশ্যে এবং চিকিৎসকের বিকল্প নয়।",
            'marathi': "महत्त्वाचे नकार: ही माहिती केवळ माहितीच्या हेतूसाठी आहे. गंभीर लक्षणांसाठी त्वरित डॉक्टरांशी संपर्क साधा."
        }
        return disclaimers.get(language.lower(), disclaimers['english'])

    def translate_messages(self, messages: list, target_language: str) -> list:
        """Translate conversation messages"""
        if not messages:
            return []
        # Return original messages if LLM is unconfigured
        if not self.llm_provider or not self.llm_provider.is_available():
            return [m.get('content', '') for m in messages]

        try:
            conversation_text = ''
            for i, m in enumerate(messages):
                conversation_text += f"INDEX:{i} ROLE:{m.get('role', 'user')}\n{m.get('content', '')}\n---\n"

            user_prompt = f"Target Language: {target_language}\n\nConversation:\n{conversation_text}\n\nReturn strict JSON array of translated texts with indices."
            response = self.llm_provider.generate_response(prompt=user_prompt)

            import json, re
            m = re.search(r"(\[\s*\{.*\}\s*\])", response, re.S)
            if m:
                parsed = json.loads(m.group(1))
                translated = [None] * len(messages)
                for item in parsed:
                    translated[int(item.get('index'))] = item.get('content', '')
                return [translated[i] or messages[i].get('content', '') for i in range(len(messages))]
        except Exception:
            pass
        return [m.get('content', '') for m in messages]
