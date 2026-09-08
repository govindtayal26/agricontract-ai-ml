import requests # <--- MAKE SURE THIS IS HERE!

def get_farmer_weather(lat, lon):
    # REPLACE this string with your REAL API key from OpenWeatherMap
    API_KEY = "7d3f259fd51c9475d7064c65b0021379" 
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Check if the API actually gave us a '200 OK' success code
        if response.status_code == 200:
            # Safely get the data
            temp = data.get('main', {}).get('temp', 0)
            humidity = data.get('main', {}).get('humidity', 0)
            desc = data.get('weather', [{}])[0].get('description', 'Unknown')
            city = data.get('name', 'Your Farm')
            
            # Simple Agri-Logic
            advice = "Conditions are good for farming."
            if humidity > 85:
                advice = "High humidity: Watch for fungal diseases."
            elif temp > 35:
                advice = "High heat: Increase irrigation."
                
            return {
                "city": city,
                "temp": round(temp),
                "humidity": humidity,
                "desc": desc.title(),
                "advice": advice
            }
        else:
            # If the API key is wrong, the status code might be 401
            print(f"Weather API Error: {data}") # This will print in your Django terminal
            return {"error": "API Key invalid or service unavailable."}
            
    except Exception as e:
        print(f"Weather Request Failed: {e}")
        return {"error": "Could not connect to weather service."}