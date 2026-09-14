# CarePulse - Production Deployment Guide

This guide provides step-by-step instructions to deploy **CarePulse** (Clinical Health Monitoring & Disease Diagnostic System) to public cloud platforms and containers.

---

## 🌟 Quick Overview of Deployment Options

| Option | Platform | Cost | Setup Time | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Option 1 (Recommended)** | **Render.com** | **Free** | 5 mins | Zero-cost cloud hosting with automatic HTTPS & CI/CD from GitHub. |
| **Option 2** | **Railway / Fly.io** | Free Trial | 5 mins | Fast container deployment with instant domain. |
| **Option 3** | **Docker Container** | VPS Cost | 2 mins | AWS, DigitalOcean, Azure, Google Cloud, or local production server. |
| **Option 4** | **Instant Public Tunnel (ngrok)** | **Free** | 30 seconds | Test live immediately on mobile devices without any cloud account. |

---

## 🚀 Option 1: Free Cloud Deployment via Render.com (Recommended)

Render provides 100% free web hosting for Python Flask web applications directly from GitHub.

### Step 1: Push Your Code to GitHub

Open terminal in the project directory:

```bash
# 1. Initialize git repository
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: CarePulse production ready"

# 4. Create a new repository on GitHub (https://github.com/new), then link and push:
git remote add origin https://github.com/YOUR_USERNAME/carepulse.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to **[render.com](https://render.com)** and sign in with your GitHub account.
2. Click **New +** in the top navigation and select **Web Service**.
3. Connect your `carepulse` GitHub repository.
4. Render will automatically detect the settings from `render.yaml` and `Procfile`. Verify:
   - **Name**: `carepulse`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
   - **Instance Type**: `Free`
5. *(Optional)* Add Environment Variables under **Advanced**:
   - `LLM_PROVIDER`: `openai` (or `gemini`)
   - `OPENAI_API_KEY`: `your-key-here` (optional, offline clinical engine works without keys!)
6. Click **Deploy Web Service**.
7. In ~2 minutes, your service will be live at:
   `https://carepulse-xxxx.onrender.com`

---

## 🐳 Option 2: Deploy with Docker

CarePulse is pre-configured with a production-ready `Dockerfile` and `docker-compose.yml`.

### Running Locally or on Any VPS (Ubuntu / Debian / CentOS / AWS / DigitalOcean):

1. **Build and start the container:**
   ```bash
   docker-compose up --build -d
   ```

2. **Check container status:**
   ```bash
   docker ps
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

4. **Stop the container:**
   ```bash
   docker-compose down
   ```

---

## ⚡ Option 3: Deploy to Railway

1. Go to **[railway.app](https://railway.app)**.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your `carepulse` repository.
4. Railway automatically detects `Procfile` and `requirements.txt` and provisions a public domain.

---

## 📲 Option 4: Instant Public URL via ngrok (No Cloud Registration Needed)

If you want an immediate live HTTPS URL to show on your phone or send to others right now:

1. **Install ngrok** (if not already installed) from [ngrok.com](https://ngrok.com) or run:
   ```powershell
   winget install ngrok
   ```

2. **Ensure CarePulse is running locally:**
   ```bash
   python run_app.py
   ```

3. **Start the public tunnel:**
   ```bash
   ngrok http 5000
   ```

4. You will receive a secure public HTTPS link (e.g. `https://xxxx.ngrok-free.app`) accessible from any smartphone, tablet, or external computer!

---

## 🔒 Production Security Checklist

- [x] **WSGI Production Server**: Configured with Gunicorn (Linux/Cloud) and Waitress (Windows).
- [x] **Zero-Knowledge Session Store**: In-memory patient assessments isolated per session.
- [x] **Offline Clinical Fallback**: Rule engine with 40+ conditions operates without relying on third-party cloud uptime.
- [x] **Multi-Language Support**: English, Spanish, French, Kannada, Hindi, Telugu, Tamil, and more.
- [x] **Health Check Route**: Dedicated `GET /health` endpoint for cloud orchestrator liveness checks.
