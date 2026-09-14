# CarePulse - Clinical Health Monitoring & Disease Diagnostic System

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/prajwal2704/AI-health-monitoring-systrm)

CarePulse is a comprehensive, production-grade clinical health monitoring and disease prediction platform. It delivers differential diagnostic evaluations, real-time vital sign risk index tracking, multi-turn clinical chat consultations, and regional multi-language medical guidance.

---

## 🚀 1-Click Free Cloud Deployment (24/7 Permanent Link)

You can deploy CarePulse to the cloud for free with **zero command line setup**:

1. Click the button below:  
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/prajwal2704/AI-health-monitoring-systrm)
2. Sign in with your GitHub account (**prajwal2704**).
3. Click **"Apply"** / **"Create Web Service"**.
4. Render will automatically build the service and give you a permanent HTTPS URL:
   ```
   https://carepulse.onrender.com
   ```
   *This link remains active 24/7, has no connection limits, and can be opened from any mobile phone, tablet, or PC worldwide.*

---

## 🌟 Key Features

- **Clinical Disease Prediction Engine** (`engine/`):
  - Weighted inference model supporting 40+ disease diagnostic profiles across 8 clinical specialties.
  - Calculated percentage confidence scores with primary and top 3 differential diagnoses.
  - Dynamic follow-up questions tailored to resolve overlapping symptoms.
- **AHA/WHO Vitals Risk Analyzer**:
  - Real-time evaluations for Blood Pressure, Heart Rate, Oxygen Saturation (SpO2), Temperature, and Blood Glucose.
- **Mobile-Responsive Web Dashboard**:
  - Optimized for mobile and desktop screens with bottom navigation bar and slide-out menu drawer.
  - Interactive symptom chips and instant disease prediction cards.
- **Multi-Language Support**:
  - English, Kannada (ಕನ್ನಡ), Hindi (हिंदी), Telugu (తెలుగు), Tamil (தமிழ்), Bengali, Marathi, and 7 additional regional languages.
- **Mandatory Patient Authentication**:
  - Strict input validation on all login and registration fields.
  - Demo / Quick Guest access mode for immediate clinical evaluation.

---

## 💻 Local Development

### 1. Clone & Install
```bash
git clone https://github.com/prajwal2704/AI-health-monitoring-systrm.git
cd AI-health-monitoring-systrm
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run_app.py
```
Open **`http://localhost:5000`** in your browser.

---

## 🐳 Docker Deployment
```bash
docker build -t carepulse .
docker run -p 5000:5000 carepulse
```
