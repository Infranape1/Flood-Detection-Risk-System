# risk_predict.py
# SMART AI FLOOD RISK ENGINE

import joblib
import numpy as np

# ==========================================
# LOAD TRAINED MODEL
# ==========================================
model = joblib.load("risk_model.pkl")

# ==========================================
# MAIN PREDICTION
# ==========================================
def predict_risk(temp, humidity, rainfall):
    """
    Smart flood risk prediction using:
    - ML model
    - Real rainfall logic
    - Humidity logic
    - Temperature logic
    - Safety corrections
    """

    # ======================================
    # TRY MODEL FIRST
    # ======================================
    try:
        data = np.array([[temp, humidity, rainfall]])
        pred = model.predict(data)[0]

        mapping = {
            0: "Low",
            1: "Medium",
            2: "High"
        }

        if pred in mapping:
            pred = mapping[pred]

        pred = str(pred).title()

    except:
        pred = "Low"

    # ======================================
    # REAL WORLD LOGIC OVERRIDE
    # ======================================

    # No rainfall at all
    if rainfall <= 0:
        if humidity < 70:
            return "Low"
        else:
            return "Medium"

    # Very light rain
    if 0 < rainfall < 2:
        if humidity > 85:
            return "Medium"
        return "Low"

    # Light rain
    if 2 <= rainfall < 10:
        if humidity >= 80:
            return "Medium"
        return "Low"

    # Moderate rain
    if 10 <= rainfall < 25:
        if humidity >= 75:
            return "High"
        return "Medium"

    # Heavy rain
    if 25 <= rainfall < 50:
        return "High"

    # Extreme rain
    if rainfall >= 50:
        return "High"

    # ======================================
    # Temperature based correction
    # ======================================

    # Cold + rain = slower runoff
    if temp < 10 and pred == "High":
        return "Medium"

    # Hot + humidity + rain can intensify storms
    if temp > 32 and humidity > 80 and rainfall >= 10:
        return "High"

    # ======================================
    # Final fallback
    # ======================================
    return pred