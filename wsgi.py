"""
WSGI Entrypoint for CarePulse Production Deployment
Supports Gunicorn, Waitress, uWSGI, and cloud platforms (Render, Railway, Fly.io, AWS, Heroku)
"""
import os
import sys

# Ensure inner application directory is prioritized in Python module lookup
current_dir = os.path.dirname(os.path.abspath(__file__))
inner_dir = os.path.join(current_dir, "AI-Based-Health-Monitoring-System-main")

if os.path.exists(inner_dir):
    os.chdir(inner_dir)
    sys.path.insert(0, inner_dir)
else:
    sys.path.insert(0, current_dir)

from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    try:
        from waitress import serve
        print(f"Serving CarePulse on http://0.0.0.0:{port} with Waitress WSGI...")
        serve(app, host="0.0.0.0", port=port)
    except ImportError:
        app.run(host="0.0.0.0", port=port, debug=False)
