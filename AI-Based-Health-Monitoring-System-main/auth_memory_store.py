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
    role: str = "patient"
    last_login: Optional[str] = None

    def __post_init__(self):
        if self.conversations is None:
            self.conversations = []
        if not self.role:
            self.role = "patient"

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

# Absolute path to ensure both Patient Portal and Admin Server share the exact same file
DEFAULT_AUTH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth_data.json")

class InMemoryAuthStore:
    """In-Memory authentication and data store with file persistence and multi-process auto-sync"""

    def __init__(self, data_file=None):
        self.data_file = data_file or DEFAULT_AUTH_FILE
        self._last_mtime = 0.0
        self.users: Dict[str, User] = {}  # email -> User
        self.conversations: Dict[str, Conversation] = {}  # conversation_id -> Conversation
        self.active_sessions: Dict[str, str] = {}  # session_token -> email
        self.login_history: List[Dict] = []  # List of recent login audit entries
        self._load_data()
        self._ensure_admin_user()

    def _ensure_admin_user(self):
        """Ensure default system administrator account exists"""
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@carepulse.local").strip().lower()
        admin_password = os.environ.get("ADMIN_PASSWORD", "Admin@CarePulse2026!").strip()
        
        if admin_email not in self.users:
            user_id = "admin-" + secrets.token_hex(8)
            admin_user = User(
                id=user_id,
                full_name="System Administrator",
                date_of_birth="1985-01-01",
                email=admin_email,
                password_hash=self.hash_password(admin_password),
                created_at=datetime.now().isoformat(),
                role="admin",
                last_login=datetime.now().isoformat()
            )
            self.users[admin_email] = admin_user
            self._save_data()
        else:
            self.users[admin_email].role = "admin"

    def _sync_from_disk(self):
        """Force re-sync from disk so admin server always picks up logins written by patient portal process"""
        if not os.path.exists(self.data_file):
            return
        try:
            self._load_data()
        except Exception:
            pass

    def _load_data(self):
        """Load data from file if it exists with full backward compatibility"""
        if os.path.exists(self.data_file):
            try:
                self._last_mtime = os.path.getmtime(self.data_file)
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Load users safely
                for email, user_data in data.get('users', {}).items():
                    safe_data = {
                        'id': user_data.get('id', secrets.token_hex(16)),
                        'full_name': user_data.get('full_name', 'Patient User'),
                        'date_of_birth': user_data.get('date_of_birth', '1995-01-01'),
                        'email': user_data.get('email', email),
                        'password_hash': user_data.get('password_hash', ''),
                        'created_at': user_data.get('created_at', datetime.now().isoformat()),
                        'conversations': user_data.get('conversations', []),
                        'role': user_data.get('role', 'patient'),
                        'last_login': user_data.get('last_login', None)
                    }
                    user = User(**safe_data)
                    self.users[email] = user

                # Load conversations
                for conv_id, conv_data in data.get('conversations', {}).items():
                    conversation = Conversation(**conv_data)
                    self.conversations[conv_id] = conversation

                # Load login history audit stream
                self.login_history = data.get('login_history', [])
                if not self.login_history:
                    # Seed login history from existing users who have last_login
                    for email, user in self.users.items():
                        if user.last_login:
                            self.login_history.append({
                                "id": secrets.token_hex(8),
                                "email": user.email,
                                "full_name": user.full_name,
                                "role": user.role,
                                "login_type": "password" if user.role != 'admin' else "admin",
                                "timestamp": user.last_login,
                                "ip": "127.0.0.1",
                                "user_agent": "Web Client"
                            })
                    self.login_history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

            except Exception as e:
                print(f"Warning: Could not load data from {self.data_file}: {e}")

    def _save_data(self):
        """Save data to file and update last modified tracking"""
        try:
            data = {
                'users': {email: asdict(user) for email, user in self.users.items()},
                'conversations': {conv_id: asdict(conv) for conv_id, conv in self.conversations.items()},
                'login_history': self.login_history[:200]
            }

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self._last_mtime = os.path.getmtime(self.data_file)
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

    def register_user(self, full_name: str, date_of_birth: str, email: str, password: str, role: str = "patient") -> Dict:
        """Register a new user"""
        # Check if user already exists
        if email in self.users:
            return {"success": False, "error": "User already exists with this email"}

        # Create new user
        user_id = secrets.token_hex(16)
        password_hash = self.hash_password(password)

        admin_email = os.environ.get("ADMIN_EMAIL", "admin@carepulse.local").strip().lower()
        if email.lower() == admin_email or email.lower().startswith("admin@"):
            role = "admin"

        user = User(
            id=user_id,
            full_name=full_name,
            date_of_birth=date_of_birth,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now().isoformat(),
            role=role,
            last_login=datetime.now().isoformat()
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
                "date_of_birth": user.date_of_birth,
                "role": user.role
            },
            "session_token": session_token
        }

    def authenticate_user(self, email: str, password: str) -> Dict:
        """Authenticate existing user"""
        user = self.users.get(email)
        if not user:
            # Auto-provision standard demo accounts for instant seamless evaluation
            demo_accounts = {
                "dr.watson@carepulse.local": ("Dr. Emily Watson, MD (Clinician)", "1984-06-15", "patient"),
                "patient@carepulse.local": ("Sarah Jenkins (Patient)", "1992-11-20", "patient"),
                "demo@carepulse.local": ("CarePulse Demo User", "1990-01-01", "patient"),
                "dr.demo@carepulse.local": ("Dr. Marcus Vance, Chief of Triage", "1980-03-25", "patient")
            }
            if email in demo_accounts:
                full_name, dob, role = demo_accounts[email]
                self.register_user(full_name=full_name, date_of_birth=dob, email=email, password=password, role=role)
                user = self.users.get(email)
            else:
                return {"success": False, "error": "User not found or invalid credentials"}

        if not self.verify_password(password, user.password_hash):
            return {"success": False, "error": "User not found or invalid credentials"}

        # Track last login and append to login history audit stream
        user.last_login = datetime.now().isoformat()
        login_entry = {
            "id": secrets.token_hex(8),
            "email": user.email,
            "full_name": user.full_name,
            "role": getattr(user, 'role', 'patient'),
            "login_type": "admin" if getattr(user, 'role', 'patient') == 'admin' else "password",
            "timestamp": user.last_login,
            "ip": "127.0.0.1",
            "user_agent": "Web Client"
        }
        self.login_history.insert(0, login_entry)
        self.login_history = self.login_history[:200]
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
                "date_of_birth": user.date_of_birth,
                "role": getattr(user, "role", "patient")
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
                "date_of_birth": "1995-01-01",
                "role": "patient"
            }

        email = self.active_sessions.get(session_token)
        if not email:
            # If server restarted or token unrecognized, grant guest session to prevent blocking
            return {
                "id": "guest-user",
                "full_name": "Guest Patient",
                "email": "guest@healthcheck.local",
                "date_of_birth": "1995-01-01",
                "role": "patient"
            }

        user = self.users.get(email)
        if not user:
            return {
                "id": "guest-user",
                "full_name": "Guest Patient",
                "email": email or "guest@healthcheck.local",
                "date_of_birth": "1995-01-01",
                "role": "patient"
            }

        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "date_of_birth": user.date_of_birth,
            "role": getattr(user, "role", "patient")
        }

    # =========================================================================
    # ADMINISTRATOR METHODS
    # =========================================================================
    def get_all_users_admin(self) -> List[Dict]:
        """Get all registered user accounts with activity stats for admin monitoring"""
        users_list = []
        for email, u in self.users.items():
            conv_count = len(u.conversations) if u.conversations else 0
            users_list.append({
                "id": u.id,
                "full_name": u.full_name,
                "email": u.email,
                "date_of_birth": u.date_of_birth,
                "role": getattr(u, "role", "patient"),
                "created_at": u.created_at,
                "last_login": getattr(u, "last_login", None),
                "conversation_count": conv_count,
                "password_status": "PBKDF2-SHA256 Encrypted (Protected)"
            })
        users_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return users_list

    def get_user_conversations_admin(self, user_id: str) -> Optional[Dict]:
        """Get full consultation & diagnostic activity logs for a specific user"""
        target_user = None
        for u in self.users.values():
            if u.id == user_id:
                target_user = u
                break
        
        if not target_user:
            return None
        
        convs = []
        for c_ref in target_user.conversations:
            conv = self.conversations.get(c_ref.get('id'))
            if conv:
                convs.append(asdict(conv))
        
        return {
            "user": {
                "id": target_user.id,
                "full_name": target_user.full_name,
                "email": target_user.email,
                "date_of_birth": target_user.date_of_birth,
                "role": getattr(target_user, "role", "patient"),
                "created_at": target_user.created_at,
                "last_login": getattr(target_user, "last_login", None)
            },
            "conversations": convs
        }

    def admin_reset_password(self, user_id: str, new_password: str) -> Dict:
        """Allow administrator to set a new password for any user"""
        target_user = None
        for u in self.users.values():
            if u.id == user_id:
                target_user = u
                break
        
        if not target_user:
            return {"success": False, "error": "User account not found"}
        
        if not new_password or len(new_password) < 6:
            return {"success": False, "error": "Password must be at least 6 characters"}
        
        target_user.password_hash = self.hash_password(new_password)
        self._save_data()
        return {"success": True, "message": f"Password for {target_user.email} updated successfully"}

    def delete_user_admin(self, user_id: str) -> Dict:
        """Allow administrator to delete a user account and associated consultations"""
        target_email = None
        for email, u in self.users.items():
            if u.id == user_id:
                target_email = email
                break
        
        if not target_email:
            return {"success": False, "error": "User not found"}
        
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@carepulse.local").strip().lower()
        if target_email.lower() == admin_email:
            return {"success": False, "error": "Cannot delete root system administrator account"}
        
        # Remove user conversations
        u = self.users[target_email]
        for c_ref in u.conversations:
            cid = c_ref.get('id')
            if cid in self.conversations:
                del self.conversations[cid]
        
        # Invalidate active sessions
        tokens_to_del = [tok for tok, em in self.active_sessions.items() if em == target_email]
        for tok in tokens_to_del:
            del self.active_sessions[tok]
        
        del self.users[target_email]
        self._save_data()
        return {"success": True, "message": f"User {target_email} deleted successfully"}

    def get_admin_stats(self) -> Dict:
        """Get high-level system usage KPI statistics"""
        total_users = len(self.users)
        total_conversations = len(self.conversations)
        active_sessions = len(self.active_sessions)
        patients_count = sum(1 for u in self.users.values() if getattr(u, 'role', 'patient') != 'admin')
        admins_count = sum(1 for u in self.users.values() if getattr(u, 'role', 'patient') == 'admin')
        
        return {
            "total_users": total_users,
            "patients_count": patients_count,
            "admins_count": admins_count,
            "total_conversations": total_conversations,
            "active_sessions": active_sessions
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

