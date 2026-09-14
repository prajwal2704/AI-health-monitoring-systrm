/**
 * Conversation Mode Detection Utility
 * Determines whether user input is medical or general conversation
 */

/**
 * Medical keywords that indicate medical consultation mode (specific symptoms, body parts, conditions)
 */
const MEDICAL_KEYWORDS = [
  // Symptoms
  'pain', 'ache', 'headache', 'fever', 'cough', 'cold', 'flu', 'nausea',
  'vomiting', 'diarrhea', 'constipation', 'rash', 'itching', 'swelling',
  'dizziness', 'fatigue', 'weakness', 'sore throat', 'chills', 'migraine',
  'stomach ache', 'chest pain', 'back pain', 'joint pain',

  // Anatomy / Areas of concern
  'stomach', 'chest', 'throat', 'lungs', 'kidney', 'liver', 'heart',
  'blood pressure', 'breathing', 'shortness of breath',

  // Conditions / Diseases
  'infection', 'inflammation', 'allergy', 'allergic', 'asthma', 'diabetes',
  'cancer', 'tumor', 'injury', 'burn', 'wound', 'fracture', 'sick', 'unwell',
  'illness', 'ailment', 'hypertension',

  // Medical Interventions & Terminology
  'medicine', 'medication', 'drug', 'prescription', 'dosage', 'pill',
  'tablet', 'treatment', 'therapy', 'symptom', 'symptoms', 'diagnosis',
  'doctor', 'physician', 'hospital', 'clinic', 'remedy'
];

/**
 * General conversation patterns that indicate friendly chat mode
 */
const FRIENDLY_PATTERNS = [
  // Greetings
  /^hi\b/i, /^hello\b/i, /^hey\b/i, /^good\s+(morning|afternoon|evening|day|night)/i,
  /^howdy\b/i, /^greetings\b/i, /^salutations\b/i,

  // Polite inquiries
  /^how\s+are\s+you/i, /^what'?s\s+up/i, /^how\s+have\s+you\s+been/i,
  /^how\s+do\s+you\s+do/i, /^nice\s+to\s+meet\s+you/i,

  // Friendly conversation starters
  /^tell\s+me\s+about/i, /^what\s+do\s+you\s+do/i, /^who\s+are\s+you/i,
  /^can\s+you\s+(help|tell|explain)/i, /^i\s+(need|want)\s+to\s+(know|ask)/i,

  // Casual acknowledgments
  /^thanks?\b/i, /^thank\s+you/i, /^please/i, /^sorry/i, /^excuse\s+me/i,

  // Simple questions that aren't medical
  /^what\s+is/i, /^how\s+does/i, /^can\s+you/i, /^do\s+you/i,
  /^why\s+do/i, /^when\s+will/i, /^where\s+can/i, /^which\s+is/i
];

/**
 * Check if message contains medical-related content using regex word boundaries
 * @param {string} message - User message to analyze
 * @returns {boolean} True if message appears to be medical-related
 */
const containsMedicalContent = (message) => {
  if (!message) return false;

  // Check for medical keywords with word boundaries
  const hasMedicalKeywords = MEDICAL_KEYWORDS.some(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'i');
    return regex.test(message);
  });

  // Check for medical question patterns
  const medicalQuestionPatterns = [
    /\b(what|how|why|when|where|which|should|can|do)\s+(is|are|do|does|should|can|will|would|could|may)\s+(this|that|it|symptom|pain|condition|treatment|medicine)/i,
    /\b(help|advice|suggestion|recommendation)\s+(for|with|about)\s+(pain|symptom|condition|treatment|medicine|health)/i,
    /\b(i\s+have|i'm|i\s+am|feeling|experiencing)\s+(pain|ache|fever|cough|nausea|rash|fatigue|sick|unwell)/i,
    /\b(medicine|medication|drug|pill|tablet|dosage|prescription)\s+(for|about|question)/i,
    /\b(take|use|need|want|give|recommend)\s+(medicine|medication|drug|pill|tablet|treatment)/i,
    /\b(symptom|pain|ache|fever|cough|cold|flu|infection|disease|sick|ill)\s+(of|for|with)/i
  ];

  const hasMedicalQuestion = medicalQuestionPatterns.some(pattern =>
    pattern.test(message)
  );

  return hasMedicalKeywords || hasMedicalQuestion;
};

/**
 * Check if message is friendly/general conversation
 * @param {string} message - User message to analyze
 * @returns {boolean} True if message appears to be friendly conversation
 */
const isFriendlyConversation = (message) => {
  // Check for friendly patterns
  const hasFriendlyPattern = FRIENDLY_PATTERNS.some(pattern =>
    pattern.test(message.trim())
  );

  // Check for very short messages that are likely greetings
  const isShortGreeting = message.trim().length <= 25 &&
    (/^(hi|hello|hey|sup|yo|good\s+(morning|afternoon|evening|day|night)|how\s+are\s+you[\s\?]*)$/i).test(message.trim());

  return hasFriendlyPattern || isShortGreeting;
};

/**
 * Determine the conversation mode based on user message
 * @param {string} message - User message to analyze
 * @returns {string} 'medical' or 'general'
 */
export const detectConversationMode = (message) => {
  if (!message || typeof message !== 'string') {
    return 'general';
  }

  const trimmed = message.trim();

  // Check friendly greetings FIRST
  if (isFriendlyConversation(trimmed)) {
    // If it's a greeting but also describes clear symptoms (e.g., "Hi, I have a fever")
    if (containsMedicalContent(trimmed) && trimmed.length > 20) {
      return 'medical';
    }
    return 'general';
  }

  // Then check if it contains medical content
  if (containsMedicalContent(trimmed)) {
    return 'medical';
  }

  // Common medical prefixes
  const medicalPrefixes = ['i have', 'i\'m feeling', 'i am feeling', 'suffering from'];
  if (medicalPrefixes.some(prefix => trimmed.toLowerCase().startsWith(prefix))) {
    return 'medical';
  }

  return 'general';
};

/**
 * Get response type based on conversation mode
 * @param {string} mode - Conversation mode ('medical' or 'general')
 * @returns {string} Response type for UI rendering
 */
export const getResponseType = (mode) => {
  return mode === 'medical' ? 'structured' : 'conversational';
};

