"""
Root Application Launcher
Allows starting the Health Monitoring & Disease Prediction System from the project root directory.
"""
import os
import sys
import socket

# Ensure inner directory is on Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
inner_dir = os.path.join(current_dir, "AI-Based-Health-Monitoring-System-main")

if os.path.exists(inner_dir):
    os.chdir(inner_dir)
    sys.path.insert(0, inner_dir)
else:
    sys.path.insert(0, current_dir)

def get_free_port(default_port=5000):
    for p in [default_port, 5005, 5050, 8000, 8080]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', p))
                return p
        except OSError:
            continue
    return default_port

if __name__ == "__main__":
    print("\n=======================================================")
    print(" [OK] Starting CarePulse - Clinical Health Monitoring & Disease Diagnostic System...")
    print("=======================================================\n")
    try:
        from app import app
        import config
        configured_port = int(os.environ.get("PORT", getattr(config.Config, 'FLASK_PORT', 5000)))
        port = get_free_port(configured_port)
        print(f" [Link] Open in your browser: http://localhost:{port}")
        print("=======================================================\n")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"[Error starting application]: {e}")
        sys.exit(1)
