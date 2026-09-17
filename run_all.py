"""
CarePulse Dual-Server Launcher
Runs both the Patient Health Monitoring Portal and the Dedicated Admin Server simultaneously.
- Patient Portal: http://localhost:5005 (or configured port)
- Admin Portal:   http://localhost:5006 (or configured port)
"""
import subprocess
import sys
import time
import os
import signal

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = sys.executable

    print("\n=======================================================")
    print(" CarePulse Multi-Server Orchestrator")
    print("=======================================================")
    print(" Starting Patient Portal on Port 5005...")
    print(" Starting Admin Portal on Port 5006...")
    print(" Press Ctrl+C at any time to stop both servers.")
    print("=======================================================\n")

    p_app = subprocess.Popen([python_exe, os.path.join(root_dir, "run_app.py")])
    time.sleep(1.5)
    p_admin = subprocess.Popen([python_exe, os.path.join(root_dir, "admin_server.py")])

    try:
        while True:
            time.sleep(1)
            # Check if any exited
            if p_app.poll() is not None:
                print("Patient Portal exited.")
                break
            if p_admin.poll() is not None:
                print("Admin Server exited.")
                break
    except KeyboardInterrupt:
        print("\nStopping all CarePulse servers...")
    finally:
        for p in [p_app, p_admin]:
            try:
                p.terminate()
            except Exception:
                pass
        print("CarePulse servers stopped.")

if __name__ == "__main__":
    main()
