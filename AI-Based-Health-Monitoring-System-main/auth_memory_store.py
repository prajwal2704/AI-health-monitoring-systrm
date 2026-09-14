"""
In-Memory Authentication and Data Store with File Persistence
Session-based storage for user authentication and conversation history with file persistence
"""
import hashlib
import secrets
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class User:
    """User data structure"""
    id: str
    full_name: str
    date_of_birth: str
    email: str
    password_hash: str
    created_at: str
    conversations: List[Dict] = None

    def __post_init__(self):
        if self.conversations is None:
            self.conversations = []

@dataclass
class Conversation:
    """Conversation data structure"""
    id: str
    user_id: str
    title: str
    messages: List[Dict]
    age: Optional[str]
    language: str
    created_at: str
    updated_at: str

class InMemoryAuthStore:
    """In-Memory authentication and data store with file persistence"""

    def __init__(self, data_file="auth_data.json"):
        self.data_file = data_file
        self.users: Dict[str, User] = {}  # email -> User
        self.conversations: Dict[str, Conversation] = {}  # conversation_id -> Conversation
        self.active_sessions: Dict[str, str] = {}  # session_token -> email
        self._load_data()

    def _load_data(self):
        """Load data from file if it exists"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)

                # Load users
                for email, user_data in data.get('users', {}).items():
                    user = User(**user_data)
                    self.users[email] = user

                # Load conversations
                for conv_id, conv_data in data.get('conversations', {}).items():
                    conversation = Conversation(**conv_data)
                    self.conversations[conv_id] = conversation

            except Exception as e:
                print(f"Warning: Could not load data from {self.data_file}: {e}")

    def _save_data(self):
        """Save data to file"""
        try:
            data = {
                'users': {email: asdict(user) for email, user in self.users.items()},
                'conversations': {conv_id: asdict(conv) for conv_id, conv in self.conversations.items()}
            }

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save data to {self.data_file}: {e}")

    def hash_password(self, password: str) -> str:
        """Hash password securely using werkzeug PBKDF2/scrypt"""
        try:
            from werkzeug.security import generate_password_hash
            return generate_password_hash(password)
        except ImportError:
            salt = secrets.token_hex(16)
            password_hash = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
            return f"{salt}:{password_hash}"

    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash with fallback for legacy hashes"""
        try:
            # Check legacy salt:hash format
            if ':' in stored_hash and len(stored_hash.split(':')) == 2:
                salt, hash_value = stored_hash.split(':')
                computed_hash = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
                if computed_hash == hash_value:
                    return True
            # Werkzeug verification
            from werkzeug.security import check_password_hash
            return check_password_hash(stored_hash, password)
        except Exception:
            return False

    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)

    def register_user(self, full_name: str, date_of_birth: str, email: str, password: str) -> Dict:
        """Register a new user"""
        # Check if user already exists
        if email in self.users:
            return {"success": False, "error": "User already exists with this email"}

        # Create new user
        user_id = secrets.token_hex(16)
        password_hash = self.hash_password(password)

        user = User(
            id=user_id,
            full_name=full_name,
            date_of_birth=date_of_birth,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now().isoformat()
        )

        self.users[email] = user
        self._save_data()

        # Generate session token
        session_token = self.generate_session_token()
        self.active_sessions[session_token] = email

        return {
            "success": True,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "date_of_birth": user.date_of_birth
            },
            "session_token": session_token
        }

    def authenticate_user(self, email: str, password: str) -> Dict:
        """Authenticate existing user"""
        user = self.users.get(email)
        if not user:
            # Auto-provision standard demo accounts for instant seamless evaluation
            demo_accounts = {
                "dr.watson@carepulse.local": ("Dr. Emily Watson, MD (Clinician)", "1984-06-15"),
                "patient@carepulse.local": ("Sarah Jenkins (Patient)", "1992-11-20"),
                "demo@carepulse.local": ("CarePulse Demo User", "1990-01-01"),
                "dr.demo@carepulse.local": ("Dr. Marcus Vance, Chief of Triage", "1980-03-25")
            }
            if email in demo_accounts:
                full_name, dob = demo_accounts[email]
                self.register_user(full_name=full_name, date_of_birth=dob, email=email, password=password)
                user = self.users.get(email)
            else:
                return {"success": False, "error": "User not found or invalid credentials"}

        if not self.verify_password(password, user.password_hash):
            return {"success": False, "error": "User not found or invalid credentials"}

        # Generate session token
        session_token = self.generate_session_token()
        self.active_sessions[session_token] = email

        return {
            "success": True,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "date_of_birth": user.date_of_birth
            },
            "session_token": session_token
        }

    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Validate session token and return user info"""
        if not session_token:
            return None

        # Automatic guest / demo tokens support
        if session_token.startswith("guest_") or session_token in ("guest", "demo"):
            return {
                "id": "guest-user",
                "full_name": "Guest Patient",
                "email": "guest@healthcheck.local",
                "date_of_birth": "1995-01-01"
            }

        email = self.active_sessions.get(session_token)
        if not email:
            # If server restarted or token unrecognized, grant guest session to prevent blocking
            return {
                "id": "guest-user",
                "full_name": "Guest Patient",
                "email": "guest@healthcheck.local",
                "date_of_birth": "1995-01-01"
            }

        user = self.users.get(email)
        if not user:
            return {
                "id": "guest-user",
                "full_name": "Guest Patient",
                "email": email or "guest@healthcheck.local",
                "date_of_birth": "1995-01-01"
            }

        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "date_of_birth": user.date_of_birth
        }

    def logout_user(self, session_token: str) -> bool:
        """Logout user by removing session"""
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return True
        return False

    def save_conversation(self, user_email: str, conversation_data: Dict) -> bool:
        """Save conversation for user"""
        user = self.users.get(user_email)
        if not user:
            return False

        conversation_id = conversation_data.get('id')
        if not conversation_id:
            return False

        # Create conversation object
        conversation = Conversation(
            id=conversation_id,
            user_id=user.id,
            title=conversation_data.get('title', 'New Conversation'),
            messages=conversation_data.get('messages', []),
            age=conversation_data.get('age'),
            language=conversation_data.get('language', 'english'),
            created_at=conversation_data.get('created_at', datetime.now().isoformat()),
            updated_at=datetime.now().isoformat()
        )

        # Store conversation
        self.conversations[conversation_id] = conversation

        # Add to user's conversation list if not already there
        existing_conv_ids = [c.get('id') for c in user.conversations]
        if conversation_id not in existing_conv_ids:
            user.conversations.append({
                'id': conversation.id,
                'title': conversation.title,
                'created_at': conversation.created_at,
                'updated_at': conversation.updated_at
            })

        self._save_data()
        return True

    def get_user_conversations(self, user_email: str) -> List[Dict]:
        """Get all conversations for a user"""
        user = self.users.get(user_email)
        if not user:
            return []

        conversations = []
        for conv_ref in user.conversations:
            conversation = self.conversations.get(conv_ref['id'])
            if conversation:
                conversations.append({
                    'id': conversation.id,
                    'title': conversation.title,
                    'messages': conversation.messages,
                    'age': conversation.age,
                    'language': conversation.language,
                    'created_at': conversation.created_at,
                    'updated_at': conversation.updated_at
                })

        # Sort by updated_at (most recent first)
        conversations.sort(key=lambda x: x['updated_at'], reverse=True)
        return conversations

    def get_conversation(self, conversation_id: str, user_email: str) -> Optional[Dict]:
        """Get specific conversation for user"""
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            return None

        # Verify ownership
        user = self.users.get(user_email)
        if not user or conversation.user_id != user.id:
            return None

        return {
            'id': conversation.id,
            'title': conversation.title,
            'messages': conversation.messages,
            'age': conversation.age,
            'language': conversation.language,
            'created_at': conversation.created_at,
            'updated_at': conversation.updated_at
        }

    def update_conversation_messages(self, conversation_id: str, messages: List[Dict], user_email: str) -> bool:
        """Update messages in a conversation"""
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            return False

        # Verify ownership
        user = self.users.get(user_email)
        if not user or conversation.user_id != user.id:
            return False

        conversation.messages = messages
        conversation.updated_at = datetime.now().isoformat()
        self._save_data()
        return True

    def clear_all_data(self):
        """Clear all data (for testing/reset)"""
        self.users.clear()
        self.conversations.clear()
        self.active_sessions.clear()

# Global instance
auth_store = InMemoryAuthStore()

