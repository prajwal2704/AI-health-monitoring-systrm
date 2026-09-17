"""
CarePulse Medical Spelling Corrector Engine
Intelligently detects and corrects typos and spelling mistakes in patient queries,
mapping colloquial and misspelled words to canonical medical vocabulary.
"""
import re
import difflib
import unicodedata
from typing import List, Tuple, Dict, Any, Optional

# High-frequency phrase-level typo corrections
PHRASE_CORRECTIONS: Dict[str, str] = {
    r'\b(?:los|lose|loos)\s+(?:motion|motions|moton|montion|montions)\b': 'loose motions',
    r'\b(?:stomac|stomech|stomache)\s+(?:ache|ake|pain)\b': 'stomach ache',
    r'\b(?:chedt|chet|chst)\s+(?:pain|tightness|presure|pressure)\b': 'chest pain',
    r'\bshortnes\s+of\s+breath\b': 'shortness of breath',
    r'\bshortness\s+of\s+breth\b': 'shortness of breath',
    r'\b(?:food|fod)\s+(?:poisioning|posioning|poisonin)\b': 'food poisoning',
    r'\b(?:runy|runi)\s+nose\b': 'runny nose',
    r'\b(?:sore|sor)\s+(?:throte|throt)\b': 'sore throat',
    r'\b(?:blod|bld)\s+(?:presure|pressure)\b': 'blood pressure',
    r'\b(?:blod|bld)\s+(?:suger|sugar)\b': 'blood sugar',
    r'\b(?:hart|hrt)\s+(?:burn|born)\b': 'heartburn',
    r'\b(?:hart|hrt)\s+(?:attack|atak)\b': 'heart attack',
    r'\b(?:hart|hrt)\s+(?:racing|rate|beat)\b': 'heart racing',
    r'\b(?:urin|urination)\s+(?:burn|burning|burnin)\b': 'burning urination',
    r'\b(?:water|watry|watter)\s+(?:diarhea|stool|stools)\b': 'watery diarrhea',
    r'\b(?:breathing|breathin)\s+(?:troble|truble|difficuty|difficulty)\b': 'breathing trouble',
    r'\b(?:loss|los)\s+of\s+(?:apetite|appetit|appitite)\b': 'loss of appetite',
    r'\b(?:loss|los)\s+of\s+(?:taste|tast)\b': 'loss of taste',
    r'\b(?:loss|los)\s+of\s+(?:smell|smel)\b': 'loss of smell',
    r'\b(?:muscl|muscel|musle)\s+pain\b': 'muscle pain',
    r'\b(?:jont|jointt)\s+pain\b': 'joint pain'
}

# High-frequency single-word typo dictionary (O(1) instant lookup)
EXACT_WORD_CORRECTIONS: Dict[str, str] = {
    # Digestive / Gastric
    'vommiting': 'vomiting', 'vommit': 'vomit', 'vomitted': 'vomited', 'vomitingg': 'vomiting',
    'vometing': 'vomiting', 'vomet': 'vomit', 'vomting': 'vomiting',
    'diareha': 'diarrhea', 'diarhea': 'diarrhea', 'diarrhoea': 'diarrhea', 'dirhea': 'diarrhea',
    'diaria': 'diarrhea', 'diahrea': 'diarrhea', 'diarreah': 'diarrhea', 'diarrea': 'diarrhea',
    'nause': 'nausea', 'nausia': 'nausea', 'nauseous': 'nausea', 'nauseated': 'nausea', 'nusea': 'nausea',
    'stomache': 'stomach', 'stomac': 'stomach', 'stomech': 'stomach', 'stomack': 'stomach', 'stomic': 'stomach',
    'hartburn': 'heartburn', 'heartborn': 'heartburn', 'acidy': 'acidity', 'acidty': 'acidity',
    'constipaton': 'constipation', 'constipasion': 'constipation',

    # Respiratory / ENT
    'cogh': 'cough', 'cuogh': 'cough', 'coug': 'cough', 'coughh': 'cough', 'cauf': 'cough', 'couf': 'cough',
    'caugh': 'cough', 'caughing': 'coughing', 'coughin': 'coughing',
    'throate': 'throat', 'throte': 'throat', 'throt': 'throat',
    'snezing': 'sneezing', 'sneazing': 'sneezing', 'sneze': 'sneezing', 'sneez': 'sneezing',
    'brethless': 'breathless', 'brethlessness': 'breathlessness', 'breathles': 'breathless',
    'breathlesness': 'breathlessness', 'breathingg': 'breathing', 'breathin': 'breathing',
    'whezing': 'wheezing', 'weezing': 'wheezing', 'wheez': 'wheezing', 'weez': 'wheezing',
    'phlegm': 'phlegm', 'flegm': 'phlegm', 'plegm': 'phlegm', 'sputum': 'sputum',

    # Pain / Neurological / General
    'hedache': 'headache', 'headche': 'headache', 'headake': 'headache', 'hedake': 'headache',
    'headac': 'headache', 'headacke': 'headache', 'headaches': 'headache',
    'fevr': 'fever', 'feever': 'fever', 'feve': 'fever', 'feverr': 'fever', 'fevar': 'fever',
    'feverishh': 'feverish',
    'chils': 'chills', 'chil': 'chills', 'chillss': 'chills',
    'shiverring': 'shivering', 'shiverin': 'shivering', 'shivring': 'shivering', 'shevering': 'shivering',
    'dizzines': 'dizziness', 'dizzyness': 'dizziness', 'dizines': 'dizziness', 'dizzy': 'dizziness',
    'giddines': 'giddiness', 'giddy': 'giddiness', 'giddyness': 'giddiness',
    'tierd': 'tired', 'tierdness': 'tiredness', 'tird': 'tired', 'tirdness': 'tiredness',
    'fatig': 'fatigue', 'fatuige': 'fatigue', 'fatige': 'fatigue', 'fatiuge': 'fatigue',
    'weakeness': 'weakness', 'wekness': 'weakness', 'weaknes': 'weakness',
    'sweling': 'swelling', 'swellng': 'swelling', 'swolen': 'swollen',
    'iching': 'itching', 'itchin': 'itching', 'itchy': 'itching',
    'sholder': 'shoulder', 'sholders': 'shoulders',
    'muscel': 'muscle', 'muscels': 'muscles', 'musle': 'muscle',
    'presure': 'pressure', 'pressur': 'pressure', 'pressuer': 'pressure',
    'appetit': 'appetite', 'apetite': 'appetite', 'appitite': 'appetite',
    'infeccion': 'infection', 'infestion': 'infection', 'infecton': 'infection', 'inffection': 'infection',
    'temprature': 'temperature', 'temparature': 'temperature', 'temprater': 'temperature',
    'alergy': 'allergy', 'alergies': 'allergies', 'alerigic': 'allergic',
    'palpitationn': 'palpitation', 'palpitations': 'palpitation', 'palpitaton': 'palpitation',

    # Regional (Kanglish / Hindi / Indian English common spellings)
    'talenov': 'talenovu', 'talenovv': 'talenovu', 'thale nov': 'thale novu',
    'hotenov': 'hottenovu', 'hottenov': 'hottenovu', 'hotte nov': 'hotte novu',
    'edenov': 'edenovu', 'ede nov': 'ede novu',
    'sust': 'sustu', 'susthu': 'sustu', 'aayas': 'ayasa',
    'kemu': 'kemmu', 'sheta': 'sheeta', 'shetha': 'sheeta',
    'vaanth': 'vaanthi', 'vaant': 'vaanti',
    'buxar': 'bukhar', 'bukhar': 'bukhar', 'sirdard': 'sirdard', 'petdard': 'pet dard',
    'ultii': 'ulti', 'dastt': 'dast', 'kamjori': 'kamzori'
}

# English stop words that should NEVER be spell-corrected into medical terms
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your', 'yours', 'he', 'she', 'it',
    'they', 'them', 'have', 'had', 'has', 'having', 'am', 'is', 'are', 'was', 'were', 'been',
    'being', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
    'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
    'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
    'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
    'will', 'just', 'should', 'now', 'days', 'day', 'hours', 'hour', 'since', 'yesterday', 'today',
    'morning', 'night', 'evening', 'severe', 'mild', 'high', 'low', 'lot', 'much', 'feeling',
    'feel', 'getting', 'got', 'bad', 'terrible', 'extremely', 'really', 'also', 'doctor', 'help',
    'please', 'tell', 'what', 'give', 'medicine', 'tablet', 'tablets', 'test', 'need', 'take',
    'taken', 'taking', 'like', 'seems', 'started', 'starts', 'ago', 'last', 'past', 'always',
    'eat', 'eating', 'eaten', 'eats', 'drink', 'drinking', 'drinks', 'drank', 'food', 'water',
    'meal', 'meals', 'sleep', 'sleeping', 'slept', 'walk', 'walking', 'walked', 'run', 'running',
    'sitting', 'standing', 'lying', 'wake', 'woke', 'waking', 'went', 'go', 'going', 'time',
    'times', 'come', 'came', 'coming', 'think', 'thought', 'know', 'known', 'look', 'looking',
    'make', 'making', 'made', 'body', 'mind', 'feel', 'feels', 'felt'
}


class MedicalSpellCorrector:
    """Intelligent medical typo detection and correction engine"""

    def __init__(self):
        self.phrase_patterns = [(re.compile(pat, re.IGNORECASE), repl) for pat, repl in PHRASE_CORRECTIONS.items()]
        self.exact_word_map = EXACT_WORD_CORRECTIONS
        self.stopwords = STOPWORDS
        self._medical_vocabulary = self._build_vocabulary()

    def _build_vocabulary(self) -> List[str]:
        """Compile comprehensive list of single-word medical tokens for fuzzy matching"""
        vocab = set()
        try:
            from .disease_database import SYMPTOM_SYNONYMS, SYMPTOM_CATEGORIES
            for syn in SYMPTOM_SYNONYMS.keys():
                for word in syn.lower().split():
                    if len(word) >= 4 and word.isalpha() and word not in self.stopwords:
                        vocab.add(word)

            for cat, sym_list in SYMPTOM_CATEGORIES.items():
                for tok, display_name in sym_list:
                    for word in tok.lower().split('_'):
                        if len(word) >= 4 and word.isalpha() and word not in self.stopwords:
                            vocab.add(word)
                    for word in display_name.lower().split():
                        if len(word) >= 4 and word.isalpha() and word not in self.stopwords:
                            vocab.add(word)
        except Exception:
            pass

        # Fallback core clinical vocabulary
        core_medical = [
            'fever', 'headache', 'cough', 'cold', 'vomiting', 'nausea', 'diarrhea',
            'stomach', 'pain', 'chest', 'throat', 'chills', 'shivering', 'dizziness',
            'fatigue', 'tiredness', 'weakness', 'breathlessness', 'sweating', 'swelling',
            'itching', 'burning', 'urination', 'sneezing', 'infection', 'pressure',
            'joint', 'muscle', 'cramps', 'acidity', 'motions', 'wheezing', 'shortness',
            'appetite', 'weight', 'migraine', 'asthma', 'diabetes', 'flu', 'phlegm',
            'heartburn', 'palpitation', 'stiffness', 'numbness', 'blurry', 'allergic',
            'talenovu', 'hottenovu', 'edenovu', 'sheeta', 'kemmu', 'vaanti', 'sustu',
            'bukhar', 'sirdard', 'ulti', 'dast', 'kamzori'
        ]
        for w in core_medical:
            vocab.add(w)

        return sorted(list(vocab))

    def correct_text(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Correct spelling mistakes and typos in input text.
        Returns:
            corrected_text (str): Sanitized and corrected text string.
            corrections (List[Dict[str, str]]): List of applied corrections [{'original': '...', 'corrected': '...'}].
        """
        if not text or not isinstance(text, str):
            return text or '', []

        working_text = text
        corrections: List[Dict[str, str]] = []
        applied_originals = set()

        # Step 1: Phrase-level pattern replacements (e.g. 'los motions' -> 'loose motions')
        for regex, replacement in self.phrase_patterns:
            matches = list(regex.finditer(working_text))
            for match in matches:
                matched_str = match.group(0)
                if matched_str.lower() != replacement.lower():
                    corrections.append({
                        'original': matched_str,
                        'corrected': replacement
                    })
                    applied_originals.add(matched_str.lower())
                    working_text = regex.sub(replacement, working_text, count=1)

        # Step 2: Word-level corrections
        words = re.findall(r'\b[a-zA-Z]+\b', working_text)
        for word in words:
            word_lower = word.lower()

            # Skip if already part of an applied phrase correction
            if any(word_lower in orig for orig in applied_originals):
                continue

            # Skip common stopwords and very short words
            if word_lower in self.stopwords or len(word_lower) < 3:
                continue

            target_correction: Optional[str] = None

            # 2a. Exact high-frequency typo dictionary lookup
            if word_lower in self.exact_word_map:
                candidate = self.exact_word_map[word_lower]
                if candidate.lower() != word_lower:
                    target_correction = candidate

            # 2b. Dynamic fuzzy matching for words length >= 4 not in medical vocabulary
            elif len(word_lower) >= 4 and word_lower not in self._medical_vocabulary:
                close_matches = difflib.get_close_matches(
                    word_lower,
                    self._medical_vocabulary,
                    n=1,
                    cutoff=0.76
                )
                if close_matches:
                    candidate = close_matches[0]
                    if candidate != word_lower and abs(len(candidate) - len(word_lower)) <= 2:
                        target_correction = candidate

            if target_correction:
                # Maintain original capitalization pattern (title or lower)
                if word.istitle():
                    corrected_word = target_correction.title()
                elif word.isupper():
                    corrected_word = target_correction.upper()
                else:
                    corrected_word = target_correction.lower()

                corrections.append({
                    'original': word,
                    'corrected': corrected_word
                })
                applied_originals.add(word_lower)

                # Replace the exact word with word boundary
                pattern = r'\b' + re.escape(word) + r'\b'
                working_text = re.sub(pattern, corrected_word, working_text, count=1)

        return working_text, corrections


# Singleton global instance
spell_corrector = MedicalSpellCorrector()
