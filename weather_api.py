import requests

API_KEY = ""

def get_weather(place):

    try:
        # --------------------------------------
        # Step 1: Search any place -> coordinates
        # --------------------------------------
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={place}&limit=1&appid={API_KEY}"
        geo = requests.get(geo_url, timeout=10).json()

        if len(geo) == 0:
            return None

        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        # --------------------------------------
        # Step 2: Get current weather
        # --------------------------------------
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

        data = requests.get(url, timeout=10).json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        rainfall = 0

        if "rain" in data:
            rainfall = data["rain"].get("1h", 0)

        return {
            "temp": round(temp, 2),
            "humidity": humidity,
            "rainfall": rainfall,
            "lat": lat,
            "lon": lon
        }

    except:
        return None