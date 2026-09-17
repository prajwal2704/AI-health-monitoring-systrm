"""
Health Vitals Monitoring Engine
Clinical evaluation of vital signs according to American Heart Association (AHA),
World Health Organization (WHO), and American Diabetes Association (ADA) standards.
"""
from typing import Dict, Any, Optional

class VitalsMonitor:
    """Analyzes vital signs and calculates clinical risk index"""

    @staticmethod
    def analyze_vitals(
        systolic_bp: Optional[float] = None,
        diastolic_bp: Optional[float] = None,
        heart_rate: Optional[float] = None,
        spo2: Optional[float] = None,
        temperature: Optional[float] = None,
        temp_unit: str = 'F',
        blood_sugar: Optional[float] = None,
        sugar_type: str = 'random'
    ) -> Dict[str, Any]:
        """
        Evaluate full vital signs panel.
        Returns classifications, risk scores, warnings, and clinical recommendations.
        """
        results = {}
        alerts = []
        risk_score = 0  # 0: Normal, 1-2: Mild, 3-4: Moderate, >=5: High/Emergency

        # 1. Blood Pressure Analysis (AHA 2017 guidelines)
        if systolic_bp is not None and diastolic_bp is not None:
            sbp = float(systolic_bp)
            dbp = float(diastolic_bp)

            if sbp > 180 or dbp > 120:
                bp_status = "Hypertensive Crisis"
                bp_level = "critical"
                risk_score += 5
                alerts.append("[CRITICAL] Blood Pressure is in Hypertensive Crisis (>180/120 mmHg). Seek emergency care immediately!")
            elif sbp >= 140 or dbp >= 90:
                bp_status = "Stage 2 Hypertension"
                bp_level = "high"
                risk_score += 3
                alerts.append("[WARNING] Blood Pressure is Stage 2 Hypertension (≥140/90 mmHg). Consult your physician.")
            elif (130 <= sbp <= 139) or (80 <= dbp <= 89):
                bp_status = "Stage 1 Hypertension"
                bp_level = "moderate"
                risk_score += 2
            elif (120 <= sbp <= 129) and dbp < 80:
                bp_status = "Elevated Blood Pressure"
                bp_level = "mild"
                risk_score += 1
            elif sbp < 90 or dbp < 60:
                bp_status = "Hypotension (Low BP)"
                bp_level = "moderate"
                risk_score += 2
                alerts.append("[WARNING] Low blood pressure detected (<90/60 mmHg). Stay hydrated and sit down if dizzy.")
            else:
                bp_status = "Normal Blood Pressure"
                bp_level = "normal"

            results["blood_pressure"] = {
                "reading": f"{sbp:.0f}/{dbp:.0f} mmHg",
                "status": bp_status,
                "level": bp_level,
                "systolic": sbp,
                "diastolic": dbp
            }

        # 2. Pulse / Heart Rate Analysis (AHA)
        if heart_rate is not None:
            hr = float(heart_rate)
            if hr > 120:
                hr_status = "Severe Tachycardia"
                hr_level = "high"
                risk_score += 3
                alerts.append(f"[WARNING] Resting pulse is markedly elevated ({hr:.0f} bpm). Avoid stimulants and rest.")
            elif hr > 100:
                hr_status = "Tachycardia (Elevated)"
                hr_level = "moderate"
                risk_score += 2
            elif hr < 50:
                hr_status = "Marked Bradycardia"
                hr_level = "moderate"
                risk_score += 2
                alerts.append(f"[WARNING] Low heart rate detected ({hr:.0f} bpm). Consult doctor if feeling faint.")
            elif hr < 60:
                hr_status = "Mild Bradycardia"
                hr_level = "mild"
                risk_score += 1
            else:
                hr_status = "Normal Heart Rate"
                hr_level = "normal"

            results["heart_rate"] = {
                "reading": f"{hr:.0f} bpm",
                "status": hr_status,
                "level": hr_level,
                "value": hr
            }

        # 3. Oxygen Saturation SpO2 (WHO)
        if spo2 is not None:
            sat = float(spo2)
            if sat <= 90:
                spo2_status = "Severe Hypoxia"
                spo2_level = "critical"
                risk_score += 5
                alerts.append(f"[CRITICAL] Blood oxygen level is critically low ({sat:.0f}%). Oxygen support urgently needed!")
            elif sat <= 94:
                spo2_status = "Mild Hypoxia / Low Oxygen"
                spo2_level = "high"
                risk_score += 3
                alerts.append(f"[WARNING] Oxygen saturation is depressed ({sat:.0f}%). Monitor closely and seek medical checkup.")
            else:
                spo2_status = "Normal Oxygenation"
                spo2_level = "normal"

            results["spo2"] = {
                "reading": f"{sat:.0f}%",
                "status": spo2_status,
                "level": spo2_level,
                "value": sat
            }

        # 4. Body Temperature
        if temperature is not None:
            t = float(temperature)
            # Convert to Fahrenheit for standardizing
            temp_f = (t * 9/5 + 32) if temp_unit.upper() == 'C' else t

            if temp_f > 103.0:
                temp_status = "Severe High Fever / Hyperpyrexia"
                temp_level = "high"
                risk_score += 4
                alerts.append(f"[CRITICAL] High temperature detected ({temp_f:.1f}°F / {((temp_f-32)*5/9):.1f}°C). Sponge with lukewarm water.")
            elif temp_f > 100.4:
                temp_status = "Fever"
                temp_level = "moderate"
                risk_score += 2
            elif temp_f > 99.0:
                temp_status = "Low-Grade Fever"
                temp_level = "mild"
                risk_score += 1
            elif temp_f < 95.0:
                temp_status = "Hypothermia"
                temp_level = "high"
                risk_score += 3
                alerts.append(f"[WARNING] Abnormally low temperature ({temp_f:.1f}°F). Warm the patient immediately.")
            else:
                temp_status = "Normal Temperature"
                temp_level = "normal"

            results["temperature"] = {
                "reading": f"{temp_f:.1f}°F ({((temp_f-32)*5/9):.1f}°C)",
                "status": temp_status,
                "level": temp_level,
                "value_f": temp_f,
                "value_c": round((temp_f - 32) * 5/9, 1)
            }

        # 5. Blood Sugar / Glucose (ADA guidelines)
        if blood_sugar is not None:
            bs = float(blood_sugar)
            is_fasting = sugar_type.lower() == 'fasting'

            if bs < 70:
                bs_status = "Hypoglycemia (Low Blood Sugar)"
                bs_level = "high"
                risk_score += 4
                alerts.append(f"[CRITICAL] Hypoglycemia alert ({bs:.0f} mg/dL)! Consume 15g fast-acting sugar (fruit juice, candy) immediately.")
            elif is_fasting:
                if bs >= 126:
                    bs_status = "Diabetic Range (Fasting)"
                    bs_level = "high"
                    risk_score += 3
                    alerts.append(f"[WARNING] Fasting blood glucose is elevated ({bs:.0f} mg/dL). HbA1c test recommended.")
                elif bs >= 100:
                    bs_status = "Impaired Fasting Glucose (Pre-diabetic)"
                    bs_level = "moderate"
                    risk_score += 2
                else:
                    bs_status = "Normal Fasting Glucose"
                    bs_level = "normal"
            else:
                # Random / Post-prandial
                if bs >= 200:
                    bs_status = "Diabetic Range (Random)"
                    bs_level = "high"
                    risk_score += 3
                    alerts.append(f"[WARNING] Random blood glucose is significantly high ({bs:.0f} mg/dL). Consult your endocrinologist.")
                elif bs >= 140:
                    bs_status = "Elevated Blood Glucose"
                    bs_level = "moderate"
                    risk_score += 2
                else:
                    bs_status = "Normal Random Glucose"
                    bs_level = "normal"

            results["blood_sugar"] = {
                "reading": f"{bs:.0f} mg/dL ({sugar_type.title()})",
                "status": bs_status,
                "level": bs_level,
                "value": bs,
                "type": sugar_type
            }

        # Overall composite category
        if risk_score >= 5:
            overall_status = "Critical Risk"
            overall_color = "red"
        elif risk_score >= 3:
            overall_status = "High Risk"
            overall_color = "orange"
        elif risk_score >= 1:
            overall_status = "Mild Concern"
            overall_color = "yellow"
        else:
            overall_status = "Normal / Healthy Vitals"
            overall_color = "green"

        return {
            "success": True,
            "vitals": results,
            "risk_score": risk_score,
            "overall_status": overall_status,
            "overall_color": overall_color,
            "alerts": alerts,
            "has_data": len(results) > 0
        }
