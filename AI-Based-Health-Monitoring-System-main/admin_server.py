"""
CarePulse Dedicated Administration Server
Runs on a separate server / port (Default: 5006) isolated from the Patient Portal.
Restricted exclusively to administrative and clinical operations personnel.
"""
import os
import sys
import socket

# Ensure directory is on Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def get_free_port(default_port=5006):
    for p in [default_port, 5007, 5051, 8001, 8081]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', p))
                return p
        except OSError:
            continue
    return default_port

if __name__ == "__main__":
    print("\n=======================================================")
    print(" [OK] Starting CarePulse Dedicated Administration Server...")
    print(" [Role] Isolated Administrative Portal (Staff Only)")
    print("=======================================================\n")
    try:
        from flask import render_template
        from app import app
        import config

        # Set root '/' to exclusively serve the admin dashboard
        app.view_functions['index'] = lambda: render_template('admin.html')

        configured_port = int(os.environ.get("ADMIN_PORT", 5006))
        port = get_free_port(configured_port)
        print(f" [Link] Admin Console Portal: http://localhost:{port}")
        print(" [Credentials] Default Admin: admin@carepulse.local / Admin@CarePulse2026!")
        print("=======================================================\n")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"[Error starting Admin Server]: {e}")
        sys.exit(1)
