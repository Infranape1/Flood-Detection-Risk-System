# app.py
# CLEAN FINAL TRUE REAL-TIME VERSION
# SAME LOGIC PRESERVED + DUPLICATE ERROR FIXED

import gradio as gr
import requests
from datetime import datetime
from weather_api import get_weather
from risk_predict import predict_risk

# ==================================================
# API KEYS
# ==================================================
OPENWEATHER_KEY = ""
NEWS_KEY = ""

last_weather_result = ""

# ==================================================
# FUTURE FORECAST
# ==================================================
def future_forecast(area, lat, lon):

    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric"

        r = requests.get(url, timeout=10)
        data = r.json()

        total_rain = 0
        max_humidity = 0
        max_temp = -999

        for item in data["list"][:16]:

            main = item["main"]

            if main["humidity"] > max_humidity:
                max_humidity = main["humidity"]

            if main["temp"] > max_temp:
                max_temp = main["temp"]

            if "rain" in item:
                total_rain += item["rain"].get("3h", 0)

        if total_rain >= 40:
            level = "🔴 High"
            reason = "Heavy rainfall forecast"
            when = "Next 48 Hours"

        elif total_rain >= 15:
            level = "🟠 Medium"
            reason = "Moderate rain forecast"
            when = "Next 48 Hours"

        elif max_humidity >= 85:
            level = "🟠 Medium"
            reason = "Extreme humidity + storm chance"
            when = "Next 3 Days"

        else:
            level = "🟢 Low"
            reason = "No major rainfall system"
            when = "Next Week"

        return f"""
📈 TRUE LIVE FORECAST

Area: {area.title()}
Time Window: {when}

Forecast Rainfall: {round(total_rain,1)} mm
Peak Humidity: {max_humidity} %
Peak Temp: {round(max_temp,1)} °C

Reason:
{reason}

Possible Risk:
{level}
"""

    except:
        return "\n📈 Forecast unavailable."


# ==================================================
# TAB 1 - FLOOD RISK
# ==================================================
def flood_risk(area):

    if area.strip() == "":
        return "❌ Please search area."

    data = get_weather(area)

    if data is None:
        return "❌ This area is not available."

    temp = data["temp"]
    humidity = data["humidity"]
    rainfall = data["rainfall"]
    lat = data["lat"]
    lon = data["lon"]

    risk = predict_risk(temp, humidity, rainfall)

    emoji = {
        "Low": "🟢",
        "Medium": "🟠",
        "High": "🔴"
    }

    now = datetime.now()

    result = f"""
📍 Area: {area.title()}

📅 Date: {now.strftime('%d-%m-%Y')}
⏰ Time: {now.strftime('%I:%M %p')}

🌡 Temperature: {temp} °C
💧 Humidity: {humidity} %
🌧 Current Rainfall: {rainfall} mm

🚨 Current Flood Risk: {emoji[risk]} {risk}
"""

    result += future_forecast(area, lat, lon)

    return result


# ==================================================
# TAB 2 - MAP SEARCH
# ==================================================
def flood_search(place):

    if place.strip() == "":
        return "❌ Please enter location."

    data = get_weather(place)

    if data is None:
        return "❌ This area is not available."

    lat = data["lat"]
    lon = data["lon"]
    humidity = data["humidity"]
    rainfall = data["rainfall"]

    if rainfall >= 20:
        status = "🔴 ACTIVE FLOOD RISK"
        flooded_area = f"{place.title()} Lowland Zone"
        reason = "Heavy rainfall currently detected"

    elif rainfall >= 8 or humidity >= 85:
        status = "🟠 MODERATE FLOOD POSSIBILITY"
        flooded_area = f"{place.title()} Drainage Area"
        reason = "Moderate rain + high humidity"

    else:
        status = "🟢 NO CURRENT FLOOD"
        flooded_area = "No flooded zone detected"
        reason = "Weather stable"

    future = future_forecast(place, lat, lon)

    return f"""
📍 Location: {place.title()}

Live Coordinates:
Lat: {lat}
Lon: {lon}

Current Status:
{status}

Flooded Part:
{flooded_area}

Reason:
{reason}

{future}
"""


def live_map(place):

    if place.strip() == "":
        place = "world"

    data = get_weather(place)

    if data is None:
        q = place
    else:
        q = f"{data['lat']},{data['lon']}"

    return f"""
    <iframe
        width="100%"
        height="550"
        style="border:none;border-radius:18px;"
        loading="lazy"
        src="https://maps.google.com/maps?q={q}&z=11&output=embed">
    </iframe>
    """


# ==================================================
# TAB 3 - LIVE ALERTS
# ==================================================
def flood_news(place):

    if place.strip() == "":
        return "❌ Please enter location.", ""

    data = get_weather(place)

    if data is None:
        return "❌ This area is not available.", ""

    lat = data["lat"]
    lon = data["lon"]
    temp = data["temp"]
    humidity = data["humidity"]
    rainfall = data["rainfall"]

    now = datetime.now()

    map_html = f"""
    <iframe
        width="100%"
        height="520"
        style="border:none;border-radius:18px;"
        loading="lazy"
        src="https://maps.google.com/maps?q={lat},{lon}&t=k&z=13&output=embed">
    </iframe>
    """

    if rainfall >= 20:

        result = f"""
🚨 LIVE ALERTS (REAL-TIME)

📍 Location: {place.title()}
📅 {now.strftime('%d-%m-%Y')}
⏰ {now.strftime('%I:%M %p')}

🔴 ACTIVE FLOOD RISK DETECTED

Flood Zone:
{place.title()} Lowland Area

🌧 Rainfall: {rainfall} mm
💧 Humidity: {humidity} %
🌡 Temp: {temp} °C

Cause:
Heavy rainfall + drainage overflow

Precautions:

👨 People:
• Stay indoors
• Avoid flooded roads

🏛 Government:
• Activate pumps
• Open shelters

👮 Police:
• Block roads

🚑 Rescue Team:
• Boats standby
"""

    elif rainfall >= 8 or humidity >= 88:

        result = f"""
⚠ LIVE ALERTS (REAL-TIME)

📍 Location: {place.title()}
📅 {now.strftime('%d-%m-%Y')}
⏰ {now.strftime('%I:%M %p')}

🟠 FLOOD POSSIBILITY

Risk Area:
{place.title()} Drainage Belt

🌧 Rainfall: {rainfall} mm
💧 Humidity: {humidity} %
🌡 Temp: {temp} °C

Cause:
Moderate rain + very high humidity

Precautions:
• Carry umbrella
• Avoid low roads
"""

    elif rainfall > 0:

        result = f"""
🌧 LIVE WEATHER ALERT

📍 {place.title()}
🌧 Light rain active

Rainfall: {rainfall} mm
Humidity: {humidity} %

Advice:
Carry umbrella.
"""

    else:

        if temp >= 34:
            msg = "Sunny today. Carry water bottle."
        elif temp <= 15:
            msg = "Cold weather. Wear warm clothes."
        else:
            msg = "Pleasant weather today."

        result = f"""
🌤 LIVE WEATHER STATUS

📍 {place.title()}

🌡 Temp: {temp} °C
💧 Humidity: {humidity} %

{msg}

Flood Chance:
🟢 Low
"""

    return result, map_html


# ==================================================
# TAB 4 - WEATHER
# ==================================================
def weather_panel(area):

    global last_weather_result

    data = get_weather(area)

    if data is None:

        if last_weather_result != "":
            return f"""
❌ This area is not available.

Previous Valid Result:

{last_weather_result}
"""
        return "❌ This area is not available."

    now = datetime.now()
    month = now.month

    if month in [6, 7, 8, 9]:
        season = "🌧 Monsoon"
    elif month in [3, 4, 5]:
        season = "🌞 Summer"
    elif month in [10, 11]:
        season = "🍂 Autumn"
    else:
        season = "❄ Winter"

    result = f"""
🌤 LIVE WEATHER

📍 {area.title()}

📅 Date: {now.strftime('%d-%m-%Y')}
⏰ Time: {now.strftime('%I:%M %p')}
🍃 Season: {season}

🌡 Temp: {data['temp']} °C
💧 Humidity: {data['humidity']} %
🌧 Rainfall: {data['rainfall']} mm
"""

    last_weather_result = result
    return result


# ==================================================
# CSS
# ==================================================
css = """
body{
background:linear-gradient(135deg,#020617,#0f172a,#111827);
}
.gradio-container{
font-family:Arial;
color:white;
}
textarea,input{
border-radius:14px !important;
background:#0b1220 !important;
color:white !important;
border:1px solid #1e293b !important;
}
button[role="tab"]{
background:#1e293b !important;
color:#94a3b8 !important;
padding:10px 18px !important;
border-radius:16px !important;
opacity:.75 !important;
}
button[role="tab"][aria-selected="true"]{
background:linear-gradient(90deg,#2563eb,#06b6d4) !important;
color:white !important;
box-shadow:0 0 18px #06b6d4 !important;
opacity:1 !important;
}
footer{visibility:hidden;}
"""


# ==================================================
# UI
# ==================================================
with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:

    gr.Markdown("# 🌊 TRUE REAL-TIME FLOOD MONITORING SYSTEM")
    gr.Markdown("### Forecast + Weather + Alerts + Maps")

    with gr.Tab("📊 Flood Risk Prediction"):
        area = gr.Textbox(label="Search Area")
        out1 = gr.Textbox(lines=18)
        btn1 = gr.Button("Predict", variant="primary")
        btn1.click(flood_risk, inputs=area, outputs=out1)

    with gr.Tab("🗺 Google Map + Flood Search"):
        place = gr.Textbox(label="Search Place")
        out2 = gr.Textbox(lines=12)
        map_box = gr.HTML()
        btn2 = gr.Button("Search", variant="primary")
        btn2.click(flood_search, inputs=place, outputs=out2)
        btn2.click(live_map, inputs=place, outputs=map_box)

    with gr.Tab("🚨 Live Alerts"):
        alert_place = gr.Textbox(label="Enter Location")
        alert_output = gr.Textbox(lines=20)
        satellite_map = gr.HTML()
        btn3 = gr.Button("Get Real-Time Alerts", variant="primary")
        btn3.click(
            flood_news,
            inputs=alert_place,
            outputs=[alert_output, satellite_map]
        )

    with gr.Tab("🌤 Live Weather"):
        city = gr.Textbox(label="Enter Area")
        out4 = gr.Textbox(lines=14)
        btn4 = gr.Button("Get Weather", variant="primary")
        btn4.click(weather_panel, inputs=city, outputs=out4)

demo.launch()