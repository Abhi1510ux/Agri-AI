import requests

def get_weather_data(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    return response.json()

def analyze_weather_impact(weather_data):
    temp = weather_data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    
    if temp > 25 and humidity > 70:
        return "🚨 High risk of pest activity! Monitor crops closely."
    else:
        return "✅ Low risk of pest activity."
