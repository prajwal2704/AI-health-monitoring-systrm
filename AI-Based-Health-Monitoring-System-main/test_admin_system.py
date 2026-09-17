"""
Comprehensive Admin & User Management Test Suite
Tests:
1. System Administrator default auto-provisioning
2. Admin authentication & role assignment
3. RBAC protection on /api/admin/* (denies non-admin)
4. /api/admin/stats returns correct counts
5. /api/admin/users lists all user accounts, emails, and credentials security
6. /api/admin/user/<id>/conversations returns activity history
7. /api/admin/user/<id>/reset-password allows updating user password and verifying login
8. /api/admin/export-users downloads valid CSV format
9. Web interface template rendering includes Admin Console markup
"""
import json
import time
from app import app
from auth_memory_store import auth_store

def run_tests():
    client = app.test_client()
    passed = 0
    total = 0

    print("\n=======================================================")
    print(" Running CarePulse Admin & User Monitoring Tests...")
    print("=======================================================\n")

    # 1. Health check
    total += 1
    r = client.get('/health')
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    assert r.json.get('status') == 'healthy'
    print(f"[{total}] Health Check: PASS")
    passed += 1

    # 2. Portals Separation: Patient UI (/) has zero admin elements; Dedicated Admin Portal (/admin) renders Admin Console
    total += 1
    # Check Patient Portal (/)
    r_patient = client.get('/')
    assert r_patient.status_code == 200
    p_html = r_patient.data.decode('utf-8')
    assert 'tab-admin' not in p_html, "tab-admin must NOT be in patient portal"
    assert 'Admin Console' not in p_html, "Admin Console must NOT be in patient portal"
    assert 'Admin Sign In' not in p_html, "Admin Sign In must NOT be in patient portal"

    # Check Dedicated Admin Portal (/admin)
    r_admin = client.get('/admin')
    assert r_admin.status_code == 200
    a_html = r_admin.data.decode('utf-8')
    assert 'CarePulse Admin' in a_html, "CarePulse Admin missing from admin portal"
    assert 'admin@carepulse.local' in a_html, "Admin default email missing from admin portal"
    assert 'users-table-body' in a_html, "users-table-body missing from admin portal"
    assert 'activity-modal' in a_html, "activity-modal missing from admin portal"
    assert 'reset-pw-modal' in a_html, "reset-pw-modal missing from admin portal"
    print(f"[{total}] Portals Separation (Patient & Dedicated Admin Portal): PASS")
    passed += 1

    # 3. Unauthenticated access to admin endpoints must be blocked (403 or 401)
    total += 1
    r = client.get('/api/admin/stats')
    assert r.status_code == 403, f"Expected 403 for unauth admin/stats, got {r.status_code}"
    r = client.get('/api/admin/users')
    assert r.status_code == 403, f"Expected 403 for unauth admin/users, got {r.status_code}"
    print(f"[{total}] RBAC Security (Unauthenticated 403 Block): PASS")
    passed += 1

    # 4. Regular patient user access to admin endpoints must be blocked (403)
    total += 1
    test_patient_email = f"patient_{int(time.time())}@carepulse.local"
    patient_res = client.post('/api/auth/register', json={
        'full_name': 'Test Regular Patient',
        'date_of_birth': '1998-05-12',
        'email': test_patient_email,
        'password': 'Password123!'
    })
    patient_token = patient_res.json['session_token']
    assert patient_res.json['user']['role'] == 'patient', f"Expected role patient, got {patient_res.json['user']['role']}"

    patient_headers = {'Authorization': f'Bearer {patient_token}'}
    r = client.get('/api/admin/stats', headers=patient_headers)
    assert r.status_code == 403, f"Expected 403 for patient on admin/stats, got {r.status_code}"
    print(f"[{total}] RBAC Security (Patient Role 403 Block): PASS")
    passed += 1

    # 5. Admin Authentication
    total += 1
    admin_login_res = client.post('/api/auth/login', json={
        'email': 'admin@carepulse.local',
        'password': 'Admin@CarePulse2026!'
    })
    assert admin_login_res.status_code == 200
    assert admin_login_res.json['success'] is True
    assert admin_login_res.json['user']['role'] == 'admin'
    admin_token = admin_login_res.json['session_token']
    admin_headers = {'Authorization': f'Bearer {admin_token}'}
    print(f"[{total}] System Administrator Login: PASS (Role: {admin_login_res.json['user']['role']})")
    passed += 1

    # 6. Admin KPI Stats Endpoint
    total += 1
    stats_res = client.get('/api/admin/stats', headers=admin_headers)
    assert stats_res.status_code == 200
    assert stats_res.json['success'] is True
    stats = stats_res.json['stats']
    assert 'total_users' in stats and stats['total_users'] > 0
    assert 'total_conversations' in stats
    assert 'active_sessions' in stats
    print(f"[{total}] Admin KPI Stats: PASS (Total Users: {stats['total_users']}, Sessions: {stats['active_sessions']})")
    passed += 1

    # 7. Admin Users List & Credential Audit Endpoint
    total += 1
    users_res = client.get('/api/admin/users', headers=admin_headers)
    assert users_res.status_code == 200
    assert users_res.json['success'] is True
    users = users_res.json['users']
    assert len(users) >= 2
    # Verify user object schema
    sample_user = users[0]
    assert 'id' in sample_user
    assert 'full_name' in sample_user
    assert 'email' in sample_user
    assert 'password_status' in sample_user
    assert 'conversation_count' in sample_user
    assert 'password_hash' not in sample_user, "Raw password hash must NOT be leaked!"
    print(f"[{total}] Admin Users & Credentials Audit: PASS ({len(users)} accounts monitored)")
    passed += 1

    # 8. User Activity & Consultation History Endpoint
    total += 1
    # Find patient_test user ID
    target_user_id = None
    for u in users:
        if u['email'] == test_patient_email:
            target_user_id = u['id']
            break
    assert target_user_id is not None
    act_res = client.get(f'/api/admin/user/{target_user_id}/conversations', headers=admin_headers)
    assert act_res.status_code == 200
    assert act_res.json['success'] is True
    assert 'user' in act_res.json['data']
    assert 'conversations' in act_res.json['data']
    print(f"[{total}] User Activity & Consultation Inspection: PASS")
    passed += 1

    # 9. Admin Password Reset Feature
    total += 1
    new_pw = "NewCarePulsePass2026!"
    reset_res = client.post(f'/api/admin/user/{target_user_id}/reset-password', 
                            headers=admin_headers,
                            json={'new_password': new_pw})
    assert reset_res.status_code == 200
    assert reset_res.json['success'] is True

    # Verify user can now authenticate with the new password
    verify_login = client.post('/api/auth/login', json={
        'email': test_patient_email,
        'password': new_pw
    })
    assert verify_login.status_code == 200
    assert verify_login.json['success'] is True
    print(f"[{total}] Admin Password Reset & Re-Authentication: PASS")
    passed += 1

    # 10. Admin Export Users to CSV
    total += 1
    csv_res = client.get('/api/admin/export-users', headers=admin_headers)
    assert csv_res.status_code == 200
    assert 'text/csv' in csv_res.content_type
    csv_text = csv_res.data.decode('utf-8')
    assert 'User ID,Full Name,Email Address (Login)' in csv_text
    assert 'admin@carepulse.local' in csv_text
    assert test_patient_email in csv_text
    print(f"[{total}] Export User Accounts to CSV: PASS")
    passed += 1

    print("\n=======================================================")
    print(f" All Tests Passed: {passed}/{total} (100% Success)")
    print("=======================================================\n")

if __name__ == '__main__':
    run_tests()
