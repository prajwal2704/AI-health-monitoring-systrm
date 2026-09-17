"""
Flask Application - CarePulse Health Platform API with Authentication
"""
import os
import io
import csv
from datetime import datetime
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
from conversation_manager import conversation_manager, ConversationState
from medical_response_generator import MedicalResponseGenerator
from llm_providers import LLMProviderFactory
from auth_memory_store import auth_store
import config

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Authentication middleware
def require_auth(f):
    """Decorator to require authentication with automatic guest/demo fallback"""
    def wrapper(*args, **kwargs):
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '').strip() or request.args.get('token', '').strip()
        if not session_token or session_token.startswith('guest_') or session_token in ('guest', 'demo'):
            request.user = {
                'id': 'guest-user',
                'full_name': 'Guest Patient',
                'email': 'guest@healthcheck.local',
                'date_of_birth': '1995-01-01',
                'role': 'patient'
            }
            return f(*args, **kwargs)

        user = auth_store.validate_session(session_token)
        if not user:
            # Auto-recover on server restart or expired session by granting guest session
            request.user = {
                'id': 'guest-user',
                'full_name': 'Guest Patient',
                'email': 'guest@healthcheck.local',
                'date_of_birth': '1995-01-01',
                'role': 'patient'
            }
            return f(*args, **kwargs)

        # Add user to request context
        request.user = user
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def require_admin(f):
    """Decorator to require administrator authentication"""
    @require_auth
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@carepulse.local").strip().lower()
        user_email = (user.get('email') or '').strip().lower() if user else ''
        user_role = (user.get('role') or '').strip().lower() if user else ''

        if user_role == 'admin' or user_email == admin_email:
            return f(*args, **kwargs)

        return jsonify({
            'success': False,
            'error': 'Access denied: System Administrator privileges required.'
        }), 403
    wrapper.__name__ = f.__name__
    return wrapper

# Initialize medical response generator
try:
    medical_generator = MedicalResponseGenerator()
except Exception as e:
    print(f"Warning: Could not initialize medical generator: {e}")
    medical_generator = None

# Authentication Routes

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user - all fields required"""
    try:
        data = request.json or {}
        full_name = data.get('full_name', '').strip()
        date_of_birth = data.get('date_of_birth', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not full_name:
            return jsonify({'success': False, 'error': 'Full name is required. All blanks must be filled.'}), 400
        if not date_of_birth:
            return jsonify({'success': False, 'error': 'Date of birth is required. All blanks must be filled.'}), 400
        if not email:
            return jsonify({'success': False, 'error': 'Email address is required. All blanks must be filled.'}), 400
        if not password or len(password) < 6:
            return jsonify({'success': False, 'error': 'Password is required (min 6 characters). All blanks must be filled.'}), 400

        result = auth_store.register_user(
            full_name=full_name,
            date_of_birth=date_of_birth,
            email=email,
            password=password
        )

        if result['success']:
            return jsonify({
                'success': True,
                'user': result['user'],
                'session_token': result['session_token'],
                'message': 'Registration successful'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Registration failed'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user login with full_name support"""
    try:
        data = request.json or {}
        email = data.get('email', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()

        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'All blanks are required. Email and password cannot be empty.'
            }), 400

        result = auth_store.authenticate_user(
            email=email,
            password=password
        )

        if result['success']:
            if full_name:
                result['user']['full_name'] = full_name
                if email in auth_store.users:
                    auth_store.users[email].full_name = full_name
            return jsonify({
                'success': True,
                'user': result['user'],
                'session_token': result['session_token'],
                'message': 'Login successful'
            }), 200
        else:
            # If user not found and full_name is provided, auto-register on the fly
            if ("User not found" in result.get('error', '')) and full_name:
                reg_result = auth_store.register_user(
                    full_name=full_name,
                    date_of_birth='1995-01-01',
                    email=email,
                    password=password
                )
                if reg_result['success']:
                    return jsonify({
                        'success': True,
                        'user': reg_result['user'],
                        'session_token': reg_result['session_token'],
                        'message': 'Login and registration successful'
                    }), 200
            return jsonify({
                'success': False,
                'error': result.get('error', 'Invalid email or password')
            }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Login failed'
        }), 500

@app.route('/api/auth/guest', methods=['POST'])
def guest_login():
    """Create or resume guest consultation session"""
    guest_token = "guest_" + auth_store.generate_session_token()
    guest_user = {
        'id': 'guest-user',
        'full_name': 'Guest Patient',
        'email': 'guest@healthcheck.local',
        'date_of_birth': '1995-01-01'
    }
    auth_store.active_sessions[guest_token] = guest_user['email']
    return jsonify({
        'success': True,
        'user': guest_user,
        'session_token': guest_token,
        'message': 'Guest access granted'
    }), 200

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user"""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        success = auth_store.logout_user(session_token)

        return jsonify({
            'success': success,
            'message': 'Logged out successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Logout failed'
        }), 500

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user information"""
    return jsonify({
        'success': True,
        'user': request.user
    }), 200

# User Conversations Routes

@app.route('/api/user/conversations', methods=['GET'])
@require_auth
def get_user_conversations():
    """Get all conversations for the authenticated user"""
    try:
        conversations = auth_store.get_user_conversations(request.user['email'])
        return jsonify({
            'success': True,
            'conversations': conversations
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get conversations'
        }), 500

@app.route('/api/user/conversations', methods=['POST'])
@require_auth
def save_user_conversation():
    """Save a conversation for the authenticated user"""
    try:
        user_email = request.user['email']
        data = request.json
        conversation_data = data.get('conversation')

        if not conversation_data or not conversation_data.get('id'):
            return jsonify({
                'success': False,
                'error': 'Conversation data with ID is required'
            }), 400

        success = auth_store.save_conversation(user_email, conversation_data)
        if success:
            return jsonify({
                'success': True,
                'message': 'Conversation saved successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save conversation'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to save conversation'
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Serve the Web UI interface"""
    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin_portal():
    """Serve the dedicated Admin Portal interface"""
    return render_template('admin.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'CarePulse Health Platform'
    })


@app.route('/api/conversation/start', methods=['POST'])
@require_auth
def start_conversation():
    """Start a new conversation session for authenticated user"""
    try:
        user_email = request.user['email']
        conversation_id = conversation_manager.create_conversation(user_email)

        # Save conversation to user's in-memory store
        conversation_data = {
            'id': conversation_id,
            'title': 'New Conversation',
            'messages': [],
            'age': None,
            'language': 'english',
            'created_at': conversation_manager.get_conversation(conversation_id)['created_at'],
            'updated_at': conversation_manager.get_conversation(conversation_id)['updated_at']
        }
        auth_store.save_conversation(user_email, conversation_data)

        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'message': 'Conversation started. Please select your age group.',
            'state': 'awaiting_age',
            'age_groups': config.Config.AGE_GROUPS
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/conversation/<conversation_id>/age', methods=['POST'])
@require_auth
def set_age(conversation_id):
    """Set age for a conversation"""
    try:
        user_email = request.user['email']
        data = request.json
        age = data.get('age')

        if not age:
            return jsonify({
                'success': False,
                'error': 'Age is required'
            }), 400

        success = conversation_manager.set_age(conversation_id, age)

        if not success:
            return jsonify({
                'success': False,
                'error': 'Invalid age group or conversation not found'
            }), 400

        # Update conversation in in-memory store
        conv = conversation_manager.get_conversation(conversation_id)
        auth_store.update_conversation_messages(conversation_id, conv['messages'], user_email)

        # Update conversation metadata
        conversation_data = auth_store.get_conversation(conversation_id, user_email)
        if conversation_data:
            conversation_data['age'] = age
            auth_store.save_conversation(user_email, conversation_data)

        response = {
            'success': True,
            'message': 'Age set successfully',
            'age': age,
            'state': conv['state'].value
        }

        # If language is also set, conversation is ready
        if conv['state'] == ConversationState.READY:
            response['message'] = 'Conversation ready. You can now describe your symptoms.'
            response['languages'] = list(config.Config.SUPPORTED_LANGUAGES.keys())
        else:
            response['message'] = 'Age set. Please select your preferred language.'
            response['languages'] = list(config.Config.SUPPORTED_LANGUAGES.keys())

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/conversation/<conversation_id>/language', methods=['POST'])
@require_auth
def set_language(conversation_id):
    """Set language for a conversation"""
    try:
        data = request.json
        language = data.get('language', 'english').lower()
        
        success = conversation_manager.set_language(conversation_id, language)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Invalid language or conversation not found'
            }), 400
        
        conv = conversation_manager.get_conversation(conversation_id)

        response = {
            'success': True,
            'message': 'Language set successfully',
            'language': language,
            'state': conv['state'].value
        }

        # Attempt to translate existing conversation messages to the selected language
        try:
            if medical_generator and conv and conv.get('messages'):
                # Use the generator's translator to get translated contents
                translated_contents = medical_generator.translate_messages(conv['messages'], language)
                # Update stored messages in conversation manager
                conversation_manager.translate_conversation(conversation_id, language, lambda msgs, lang: medical_generator.translate_messages(msgs, lang))
                # Build translated message objects to return
                translated_messages = []
                for i, m in enumerate(conv['messages']):
                    content = translated_contents[i]
                    # For assistant messages, try to parse into structured response if possible
                    if m.get('role') == 'assistant':
                        try:
                            parsed = medical_generator._parse_response(content)
                            # include disclaimer separately
                            parsed['disclaimer'] = medical_generator._get_disclaimer(language)
                            content_obj = parsed
                        except Exception:
                            content_obj = content
                        translated_messages.append({
                            'role': m.get('role'),
                            'content': content_obj,
                            'timestamp': m.get('timestamp')
                        })
                    else:
                        translated_messages.append({
                            'role': m.get('role'),
                            'content': content,
                            'timestamp': m.get('timestamp')
                        })
                response['translated_messages'] = translated_messages

        except Exception as e:
            # If translation fails, warn but do not change conversation state
            response['translation_warning'] = 'Translation failed; original messages preserved.'
        
        # If age is also set, conversation is ready
        if conv['state'] == ConversationState.READY:
            response['message'] = 'Conversation ready. You can now describe your symptoms.'
        else:
            response['message'] = 'Language set. Please select your age group.'
            response['age_groups'] = config.Config.AGE_GROUPS
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/conversation/<conversation_id>/chat', methods=['POST'])
@require_auth
def chat(conversation_id):
    """Handle chat messages"""
    try:
        data = request.json or {}
        message = data.get('message', '').strip()
        symptoms_list = data.get('symptoms_list', [])

        if not message and not symptoms_list:
            return jsonify({
                'success': False,
                'error': 'Message or symptoms are required'
            }), 400

        if not message and symptoms_list:
            message = f"Symptoms: {', '.join(symptoms_list)}"
        
        conv = conversation_manager.get_conversation(conversation_id)
        
        # Self-healing: Automatically create session if not found or id is null
        if not conv or str(conversation_id).lower() in ('null', 'undefined', 'none', ''):
            user_email = getattr(request, 'user', {}).get('email', 'guest@healthcheck.local')
            conversation_id = conversation_manager.create_conversation(user_email)
            conversation_manager.set_age(conversation_id, data.get('age', '18-64 years (Adult)'))
            conversation_manager.set_language(conversation_id, data.get('language', 'english'))
            conv = conversation_manager.get_conversation(conversation_id)
        
        # Ensure age and language stay synchronized with request
        req_age = data.get('age') or (conv.get('age') if conv else None) or '18-64 years (Adult)'
        req_lang = data.get('language') or (conv.get('language') if conv else None) or 'english'
        if not conv.get('age') or (data.get('age') and conv.get('age') != data.get('age')):
            conversation_manager.set_age(conversation_id, req_age)
        if not conv.get('language') or (data.get('language') and conv.get('language') != data.get('language')):
            conversation_manager.set_language(conversation_id, req_lang)
        conv = conversation_manager.get_conversation(conversation_id)
        
        # Add user message to history
        conversation_manager.add_message(conversation_id, 'user', message)
        
        global medical_generator
        if not medical_generator:
            try:
                medical_generator = MedicalResponseGenerator()
            except Exception as init_err:
                print(f"Medical generator init notice: {init_err}")

        history = conversation_manager.get_conversation_history(conversation_id)
        symptoms_list = data.get('symptoms_list', [])
        vitals = data.get('vitals', None)

        if medical_generator:
            result = medical_generator.generate_medical_response(
                symptoms=message,
                age=conv['age'],
                language=conv['language'],
                conversation_history=history,
                symptoms_list=symptoms_list,
                vitals=vitals
            )
        else:
            result = {
                'success': True,
                'response': {
                    'summary': f"Clinical evaluation of: '{message}' for {conv.get('age', 'Patient')}.",
                    'home_care': "• Maintain generous fluid intake and get complete rest.\n• Avoid strenuous tasks until evaluated.",
                    'medical_attention': "Seek immediate medical consultation if symptoms escalate rapidly or severe pain develops.",
                    'possible_causes': "Possible acute viral infection or localized inflammation.",
                    'disclaimer': "IMPORTANT: Informational guidance only. Consult a doctor for formal diagnosis."
                }
            }
        
        is_valid = result.get('is_valid', True)
        input_type = result.get('input_type', 'clinical')

        if not is_valid:
            warning_msg = result.get('response', {}).get('summary', 'Input is not valid. Please enter valid medical symptoms.')
            conversation_manager.add_message(conversation_id, 'assistant', warning_msg)
            try:
                user_email = request.user['email']
                updated_conv = conversation_manager.get_conversation(conversation_id)
                if updated_conv:
                    auth_store.update_conversation_messages(conversation_id, updated_conv['messages'], user_email)
            except Exception as persist_err:
                print(f"Warning: Could not persist conversation messages: {persist_err}")

            return jsonify({
                'success': True,
                'is_valid': False,
                'input_type': 'invalid',
                'error': warning_msg,
                'response': result.get('response'),
                'disease_prediction': None,
                'conversation_id': conversation_id
            }), 200

        if input_type == 'greeting':
            greeting_msg = result.get('response', {}).get('summary', 'Hello! Please describe your symptoms.')
            conversation_manager.add_message(conversation_id, 'assistant', greeting_msg)
            try:
                user_email = request.user['email']
                updated_conv = conversation_manager.get_conversation(conversation_id)
                if updated_conv:
                    auth_store.update_conversation_messages(conversation_id, updated_conv['messages'], user_email)
            except Exception as persist_err:
                print(f"Warning: Could not persist conversation messages: {persist_err}")

            return jsonify({
                'success': True,
                'is_valid': True,
                'input_type': 'greeting',
                'response': result.get('response'),
                'disease_prediction': None,
                'conversation_id': conversation_id
            }), 200

        # Add assistant response to history
        assistant_message = f"Summary: {result['response']['summary']}\n\nHome Care: {result['response']['home_care']}\n\nMedical Attention: {result['response']['medical_attention']}\n\nPossible Causes: {result['response']['possible_causes']}"
        conversation_manager.add_message(conversation_id, 'assistant', assistant_message)
        
        # Persist updated messages to auth store
        try:
            user_email = request.user['email']
            updated_conv = conversation_manager.get_conversation(conversation_id)
            if updated_conv:
                auth_store.update_conversation_messages(conversation_id, updated_conv['messages'], user_email)
        except Exception as persist_err:
            print(f"Warning: Could not persist conversation messages: {persist_err}")
        
        return jsonify({
            'success': True,
            'is_valid': True,
            'input_type': 'clinical',
            'response': result['response'],
            'disease_prediction': result.get('disease_prediction'),
            'spelling_corrections': result.get('spelling_corrections', []),
            'corrected_text': result.get('corrected_text', message),
            'conversation_id': conversation_id
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/symptoms-list', methods=['GET'])
def get_symptoms_list():
    """Get categorized list of symptoms for UI chip selectors"""
    try:
        from engine.disease_database import SYMPTOM_CATEGORIES
        formatted = {}
        for cat, syms in SYMPTOM_CATEGORIES.items():
            formatted[cat] = [{'token': token, 'name': name} for token, name in syms]
        return jsonify({
            'success': True,
            'categories': formatted
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predict-disease', methods=['POST'])
def predict_disease():
    """Direct disease prediction endpoint taking symptoms, text, age, and optional vitals"""
    try:
        data = request.json or {}
        symptoms = data.get('symptoms', [])
        text = data.get('text', '')
        age = data.get('age', '18-64 years (Adult)')
        language = data.get('language', 'english')
        vitals = data.get('vitals', None)

        global medical_generator
        if not medical_generator:
            medical_generator = MedicalResponseGenerator()

        result = medical_generator.generate_medical_response(
            symptoms=text,
            age=age,
            language=language,
            symptoms_list=symptoms,
            vitals=vitals
        )

        if not result.get('is_valid', True):
            error_msg = result.get('response', {}).get('summary', 'Input is not valid. Please enter valid medical symptoms.')
            return jsonify({
                'success': False,
                'is_valid': False,
                'error': error_msg,
                'response': result.get('response'),
                'prediction': None
            }), 400

        return jsonify({
            'success': True,
            'is_valid': True,
            'prediction': result.get('disease_prediction'),
            'response': result.get('response'),
            'spelling_corrections': result.get('spelling_corrections', []),
            'corrected_text': result.get('corrected_text', text)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/vitals/analyze', methods=['POST'])
def analyze_vitals():
    """Analyze vital signs and return clinical risk score and interpretation"""
    try:
        data = request.json or {}
        global medical_generator
        if not medical_generator:
            medical_generator = MedicalResponseGenerator()

        analysis = medical_generator.vitals_monitor.analyze_vitals(
            systolic_bp=data.get('systolic_bp'),
            diastolic_bp=data.get('diastolic_bp'),
            heart_rate=data.get('heart_rate'),
            spo2=data.get('spo2'),
            temperature=data.get('temperature'),
            temp_unit=data.get('temp_unit', 'F'),
            blood_sugar=data.get('blood_sugar'),
            sugar_type=data.get('sugar_type', 'random')
        )
        return jsonify({
            'success': True,
            'analysis': analysis
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/conversation/<conversation_id>/status', methods=['GET'])
@require_auth
def get_status(conversation_id):
    """Get conversation status"""
    try:
        conv = conversation_manager.get_conversation(conversation_id)
        
        if not conv:
            return jsonify({
                'success': False,
                'error': 'Conversation not found'
            }), 404
        
        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'state': conv['state'].value,
            'age': conv['age'],
            'language': conv['language'],
            'message_count': len(conv['messages'])
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config/age-groups', methods=['GET'])
def get_age_groups():
    """Get available age groups"""
    return jsonify({
        'success': True,
        'age_groups': config.Config.AGE_GROUPS
    }), 200


@app.route('/api/config/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    return jsonify({
        'success': True,
        'languages': config.Config.SUPPORTED_LANGUAGES,
        'default_language': config.Config.DEFAULT_LANGUAGE
    }), 200


@app.route('/api/config/llm-providers', methods=['GET'])
def get_llm_providers():
    """Get available LLM providers"""
    try:
        available = LLMProviderFactory.list_available_providers()
        current = config.Config.LLM_PROVIDER
        
        return jsonify({
            'success': True,
            'current_provider': current,
            'available_providers': available,
            'all_providers': list(LLMProviderFactory._providers.keys())
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config/switch-provider', methods=['POST'])
def switch_provider():
    """Switch LLM provider (admin function)"""
    try:
        data = request.json
        provider = data.get('provider')
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Provider name is required'
            }), 400
        
        new_provider = LLMProviderFactory.switch_provider(provider)
        
        # Update global medical generator
        global medical_generator
        medical_generator = MedicalResponseGenerator()
        
        return jsonify({
            'success': True,
            'provider': provider,
            'message': f'Switched to {provider} provider'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =============================================================================
# ADMINISTRATOR API ENDPOINTS (User & Credential Auditing)
# =============================================================================

@app.route('/api/admin/stats', methods=['GET'])
@require_admin
def admin_stats():
    """Get high-level system usage KPI statistics"""
    try:
        stats = auth_store.get_admin_stats()
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve statistics: {e}'
        }), 500


@app.route('/api/admin/users', methods=['GET'])
@require_admin
def admin_get_users():
    """Get all registered user accounts with activity stats for admin monitoring"""
    try:
        users = auth_store.get_all_users_admin()
        return jsonify({
            'success': True,
            'count': len(users),
            'users': users
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve users: {e}'
        }), 500


@app.route('/api/admin/user/<user_id>/conversations', methods=['GET'])
@require_admin
def admin_user_conversations(user_id):
    """Get full consultation & diagnostic activity logs for a specific user"""
    try:
        data = auth_store.get_user_conversations_admin(user_id)
        if not data:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        return jsonify({
            'success': True,
            'data': data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch user activity: {e}'
        }), 500


@app.route('/api/admin/user/<user_id>/reset-password', methods=['POST'])
@require_admin
def admin_reset_user_password(user_id):
    """Allow administrator to set a new password for any user"""
    try:
        body = request.json or {}
        new_password = body.get('new_password', '').strip()
        if not new_password or len(new_password) < 6:
            return jsonify({
                'success': False,
                'error': 'New password must be at least 6 characters.'
            }), 400

        res = auth_store.admin_reset_password(user_id, new_password)
        status_code = 200 if res.get('success') else 400
        return jsonify(res), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to reset password: {e}'
        }), 500


@app.route('/api/admin/user/<user_id>', methods=['DELETE'])
@require_admin
def admin_delete_user(user_id):
    """Allow administrator to delete a user account and associated consultations"""
    try:
        res = auth_store.delete_user_admin(user_id)
        status_code = 200 if res.get('success') else 400
        return jsonify(res), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete user: {e}'
        }), 500


@app.route('/api/admin/export-users', methods=['GET'])
@require_admin
def admin_export_users():
    """Export all user accounts and activity as a CSV file"""
    try:
        users = auth_store.get_all_users_admin()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'User ID',
            'Full Name',
            'Email Address (Login)',
            'Date of Birth',
            'Role',
            'Registered At',
            'Last Login',
            'Total Consultations',
            'Credential Security Status'
        ])
        
        for u in users:
            writer.writerow([
                u.get('id', ''),
                u.get('full_name', ''),
                u.get('email', ''),
                u.get('date_of_birth', ''),
                u.get('role', ''),
                u.get('created_at', ''),
                u.get('last_login', '') or 'Never',
                u.get('conversation_count', 0),
                u.get('password_status', '')
            ])
        
        output.seek(0)
        filename = f"carepulse_users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to export users: {e}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Validate configuration
    try:
        config.Config.validate_config()
        print(f"Starting CarePulse Health Platform with {config.Config.LLM_PROVIDER} provider...")
    except ValueError as e:
        print(f"Configuration Notice: {e}")
        print("Note: Running in demonstration mode. To enable live LLM generation, set your API key in .env.")
    except Exception as e:
        print(f"Notice: {e}")

    port = getattr(config.Config, 'FLASK_PORT', 5000)
    print(f"\n=======================================================")
    print(f" [OK] CarePulse Health Platform is running!")
    print(f" [Link] Open in your browser: http://localhost:{port}")
    print(f"=======================================================\n")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )

