"""
CarePulse Response Generator - Clinical Diagnostic and Conversational Engine
Integrates the Clinical Disease Predictor, Vitals Monitor, and LLM Providers.
"""
from typing import Dict, Any, Optional, List
from llm_providers import LLMProviderFactory
from engine.disease_predictor import DiseasePredictor
from engine.vitals_monitor import VitalsMonitor
from engine.follow_up_generator import FollowUpGenerator
import config

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
        """
        # Run disease prediction engine first
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

                return {
                    'success': True,
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

        return {
            'success': True,
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

        dis_name = primary.get('name', 'Acute Viral Syndrome / Non-Specific Discomfort')
        confidence = primary.get('confidence', 50.0)
        matched = primary.get('matched_symptoms', [])

        # Section A: Summary & Assessment
        matched_str = ", ".join(matched) if matched else (symptoms or 'Reported symptoms')
        summary = (
            f"CLINICAL ASSESSMENT FOR {str(age).upper()} PATIENT:\n"
            f"Based on reported symptoms ({matched_str}), the primary suspected condition is "
            f"**{dis_name}** with a calculated **{confidence}% clinical match**."
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
            summary = f"लक्षणों का नैदानिक मूल्यांकन: '{matched_str}' ({age} के लिए)। संभावित स्थिति: **{dis_name}** ({confidence}% मिलान)।"
            home_care = "• पर्याप्त मात्रा में ओआरएस, सूप और पानी पिएं।\n• पूर्ण शारीरिक आराम करें।\n• डॉक्टर के परामर्श के बिना कोई नई दवा न लें।"
            medical_attention = f"गंभीरता स्तर: {urgency.upper()}\nयदि सांस लेने में कठिनाई, तेज बुखार या तीव्र दर्द हो तो तुरंत अस्पताल जाएं।"
            possible_causes = f"संभावित कारण: {dis_name}। सटीक निदान के लिए रक्त परीक्षण या डॉक्टर से परामर्श आवश्यक है।"
        elif lang_lower == 'telugu':
            summary = f"లక్షణాల విశ్లేషణ: '{matched_str}' ({age} కొరకు). ప్రాథమిక రోగ నిర్ధారణ: **{dis_name}** ({confidence}% సరిపోలిక)."
            home_care = "• తగినంత ఓఆర్‌ఎస్ మరియు ద్రవపదార్థాలు తీసుకోండి.\n• సరైన విశ్రాంతి తీసుకోండి.\n• వైద్యుని సలహా లేకుండా మందులు వాడవద్దు."
            medical_attention = f"తీవ్రత స్థాయి: {urgency.upper()}\nశ్వాస తీసుకోవడంలో ఇబ్బంది లేదా అధిక జ్వరం ఉంటే వెంటనే ఆసుపత్రిని సంప్రదించండి."
            possible_causes = f"సంభావ్య కారణం: {dis_name}. ఖచ్చితమైన నిర్ధారణ కోసం వైద్యుడిని సంప్రదించండి."
        elif lang_lower == 'kannada':
            summary = f"ರೋಗಲಕ್ಷಣಗಳ ವೈದ್ಯಕೀಯ ಮೌಲ್ಯಮಾಪನ: '{matched_str}' ({age} ರೋಗಿಗೆ). ಪ್ರಾಥಮಿಕ ಶಂಕಿತ ರೋಗ: **{dis_name}** ({confidence}% ಹೊಂದಾಣಿಕೆ)."
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
