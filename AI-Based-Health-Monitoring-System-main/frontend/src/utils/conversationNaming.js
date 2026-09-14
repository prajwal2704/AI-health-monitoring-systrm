/**
 * Intelligent conversation naming utility
 * Generates unique, descriptive titles for conversations
 */

/**
 * Generate a conversation title from messages
 * @param {Array} messages - Array of message objects
 * @param {string} age - User's age group
 * @returns {string} Generated title
 */
export const generateConversationTitle = (messages, age = null) => {
  if (!messages || messages.length === 0) {
    return 'New Conversation';
  }

  // Get the first user message
  const firstUserMessage = messages.find((msg) => msg.role === 'user');
  if (!firstUserMessage) {
    return 'New Conversation';
  }

  const userText = firstUserMessage.content.toLowerCase().trim();

  // Extract key medical terms and symptoms
  const medicalKeywords = {
    fever: 'Fever',
    headache: 'Headache',
    cough: 'Cough',
    pain: 'Pain',
    cold: 'Cold',
    flu: 'Flu',
    stomach: 'Stomach',
    nausea: 'Nausea',
    dizziness: 'Dizziness',
    fatigue: 'Fatigue',
    rash: 'Rash',
    allergy: 'Allergy',
    infection: 'Infection',
    medicine: 'Medicine',
    medication: 'Medication',
    prescription: 'Prescription',
    dosage: 'Dosage',
    symptom: 'Symptoms',
    diagnosis: 'Diagnosis',
    treatment: 'Treatment',
  };

  // Check for medical keywords
  const foundKeywords = [];
  for (const [keyword, display] of Object.entries(medicalKeywords)) {
    if (userText.includes(keyword)) {
      foundKeywords.push(display);
    }
  }

  // Generate title based on keywords
  if (foundKeywords.length > 0) {
    // Use first 2-3 keywords
    const titleKeywords = foundKeywords.slice(0, 3);
    return titleKeywords.join(' & ');
  }

  // If no keywords, analyze the message structure
  // Check for question patterns
  if (userText.includes('what') || userText.includes('how') || userText.includes('why')) {
    if (userText.includes('medicine') || userText.includes('medication')) {
      return 'Medicine Inquiry';
    }
    if (userText.includes('symptom')) {
      return 'Symptom Question';
    }
    return 'Medical Question';
  }

  // Check for greeting patterns
  if (
    userText.startsWith('hi') ||
    userText.startsWith('hello') ||
    userText.startsWith('hey')
  ) {
    return 'General Consultation';
  }

  // Extract first few meaningful words (skip common words)
  const commonWords = [
    'i',
    'have',
    'am',
    'been',
    'experiencing',
    'feeling',
    'got',
    'get',
    'the',
    'a',
    'an',
    'my',
    'me',
    'for',
    'with',
    'and',
    'or',
    'but',
  ];

  const words = userText
    .split(/\s+/)
    .filter((word) => word.length > 2 && !commonWords.includes(word))
    .slice(0, 4);

  if (words.length > 0) {
    // Capitalize first letter of each word
    const titleWords = words.map(
      (word) => word.charAt(0).toUpperCase() + word.slice(1)
    );
    return titleWords.join(' ');
  }

  // Fallback: use first 30 characters
  const fallback = firstUserMessage.content.substring(0, 30).trim();
  return fallback || 'New Conversation';
};

/**
 * Ensure conversation title is unique
 * @param {string} baseTitle - Base title to make unique
 * @param {Array} existingConversations - Array of existing conversations
 * @returns {string} Unique title
 */
export const ensureUniqueTitle = (baseTitle, existingConversations = []) => {
  if (!existingConversations || existingConversations.length === 0) {
    return baseTitle;
  }

  const existingTitles = existingConversations.map((conv) => conv.title);

  // If title is already unique, return it
  if (!existingTitles.includes(baseTitle)) {
    return baseTitle;
  }

  // Try to make it unique by adding context
  // Check if we can add age context
  const ageContext = existingConversations.find(
    (conv) => conv.title === baseTitle && conv.age
  );
  if (ageContext) {
    // Title exists with age, try without age context first
    return baseTitle;
  }

  // Add numbering if duplicate exists
  let counter = 2;
  let uniqueTitle = `${baseTitle} (${counter})`;

  while (existingTitles.includes(uniqueTitle)) {
    counter++;
    uniqueTitle = `${baseTitle} (${counter})`;
  }

  return uniqueTitle;
};

/**
 * Generate a unique conversation title
 * @param {Array} messages - Array of message objects
 * @param {Array} existingConversations - Array of existing conversations
 * @param {string} age - User's age group
 * @returns {string} Unique conversation title
 */
export const getUniqueConversationTitle = (
  messages,
  existingConversations = [],
  age = null
) => {
  const baseTitle = generateConversationTitle(messages, age);
  return ensureUniqueTitle(baseTitle, existingConversations);
};

