"""
Root Application Launcher
Allows starting the Health Monitoring & Disease Prediction System from the project root directory.
"""
import os
import sys

# Ensure inner directory is on Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
inner_dir = os.path.join(current_dir, "AI-Based-Health-Monitoring-System-main")

if os.path.exists(inner_dir):
    os.chdir(inner_dir)
    sys.path.insert(0, inner_dir)
else:
    sys.path.insert(0, current_dir)

if __name__ == "__main__":
    print("\n=======================================================")
    print(" [OK] Starting CarePulse - Clinical Health Monitoring & Disease Diagnostic System...")
    print("=======================================================\n")
    try:
        from app import app
        import config
        port = getattr(config.Config, 'FLASK_PORT', 5000)
        print(f" [Link] Open in your browser: http://localhost:{port}")
        print("=======================================================\n")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"[Error starting application]: {e}")
        sys.exit(1)
