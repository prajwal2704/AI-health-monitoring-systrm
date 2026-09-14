"""
Conversation Manager - Handles chat state and flow
"""
from typing import Dict, Optional, List, Tuple
from enum import Enum
import uuid
from datetime import datetime

class ConversationState(Enum):
    """States in the conversation flow"""
    INITIAL = "initial"
    AWAITING_AGE = "awaiting_age"
    AWAITING_LANGUAGE = "awaiting_language"
    READY = "ready"
    IN_CONVERSATION = "in_conversation"

class ConversationManager:
    """Manages conversation state and history"""
    
    def __init__(self):
        self.conversations: Dict[str, Dict] = {}
    
    def create_conversation(self, user_id: str = None, conversation_id: str = None) -> str:
        """Create a new conversation session with a unique UUID"""
        conv_id = conversation_id or str(uuid.uuid4())
        
        self.conversations[conv_id] = {
            'id': conv_id,
            'user_id': user_id,
            'state': ConversationState.INITIAL,
            'age': None,
            'language': 'english',  # Default language
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        return conv_id
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation by conversation_id"""
        return self.conversations.get(conversation_id)
    
    def set_age(self, conversation_id: str, age: str) -> bool:
        """Set age for a conversation"""
        if conversation_id not in self.conversations:
            return False
        
        # Validate age
        from config import Config
        if age not in Config.AGE_GROUPS:
            return False
        
        self.conversations[conversation_id]['age'] = age
        self.conversations[conversation_id]['updated_at'] = datetime.now().isoformat()
        
        # Update state
        if self.conversations[conversation_id]['state'] in (ConversationState.AWAITING_AGE, ConversationState.INITIAL):
            if self.conversations[conversation_id]['language']:
                self.conversations[conversation_id]['state'] = ConversationState.READY
            else:
                self.conversations[conversation_id]['state'] = ConversationState.AWAITING_LANGUAGE
        
        return True
    
    def set_language(self, conversation_id: str, language: str) -> bool:
        """Set language for a conversation"""
        if conversation_id not in self.conversations:
            return False
        
        # Validate language
        from config import Config
        if language.lower() not in Config.SUPPORTED_LANGUAGES:
            return False
        
        self.conversations[conversation_id]['language'] = language.lower()
        self.conversations[conversation_id]['updated_at'] = datetime.now().isoformat()
        
        # Update state
        if self.conversations[conversation_id]['state'] in (ConversationState.AWAITING_LANGUAGE, ConversationState.INITIAL):
            if self.conversations[conversation_id]['age']:
                self.conversations[conversation_id]['state'] = ConversationState.READY
            else:
                self.conversations[conversation_id]['state'] = ConversationState.AWAITING_AGE
        
        return True

    def translate_conversation(self, conversation_id: str, target_language: str, translator) -> bool:
        """Translate all messages in a conversation to target_language using provided translator

        The translator is expected to be a callable that accepts a list of messages and a target language
        and returns a list of translated contents in the same order.
        """
        if conversation_id not in self.conversations:
            return False

        messages = self.conversations[conversation_id]['messages']
        if not messages:
            return True

        try:
            translated = translator(messages, target_language)
            # translated should be a list of strings matching messages order
            if not translated or len(translated) != len(messages):
                return False

            for i, m in enumerate(messages):
                m['content'] = translated[i]

            self.conversations[conversation_id]['updated_at'] = datetime.now().isoformat()
            return True
        except Exception:
            return False
    
    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if conversation_id not in self.conversations:
            return
        
        self.conversations[conversation_id]['messages'].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        self.conversations[conversation_id]['updated_at'] = datetime.now().isoformat()
        
        if self.conversations[conversation_id]['state'] == ConversationState.READY:
            self.conversations[conversation_id]['state'] = ConversationState.IN_CONVERSATION
    
    def can_process_symptoms(self, conversation_id: str) -> Tuple[bool, str]:
        """Check if conversation is ready to process symptoms"""
        if conversation_id not in self.conversations:
            return False, "Conversation not found"
        
        conv = self.conversations[conversation_id]
        
        if not conv['age']:
            return False, "Age selection is required before processing symptoms"
        
        if not conv['language']:
            return False, "Language selection is required"
        
        return True, "Ready"
    
    def get_conversation_history(self, conversation_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        if conversation_id not in self.conversations:
            return []
        
        messages = self.conversations[conversation_id]['messages']
        return messages[-limit:] if limit else messages
    
    def cleanup_old_conversations(self, max_age_hours: int = 24):
        """Clean up old conversations (optional maintenance)"""
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        to_remove = []
        for conv_id, conv in self.conversations.items():
            updated = datetime.fromisoformat(conv['updated_at'])
            if updated < cutoff:
                to_remove.append(conv_id)
        
        for conv_id in to_remove:
            del self.conversations[conv_id]

# Global conversation manager instance
conversation_manager = ConversationManager()

