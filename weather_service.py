#You must pip install openmeteo-requests

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

#intialize flask instance, everything needed is in the program
app = Flask(__name__)

#Explicitly enable CORS options needed
CORS(app, resources={r"/weather": {"origins": "*"}}, methods=["GET", "POST", "DELETE", "OPTIONS"])

@app.route('/weather', methods=['POST'])
def POST_weather():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload provided"}, 400)

    lat = data.get('latitude')
    long = data.get('longitude')

    coords = [lat, long]
    #now use those to query the weather API for some values.
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&temperature_unit=fahrenheit"

    try:
        response = requests.get(url)
        data_weath = response.json()

        daily_data = data_weath.get('daily', {})
        dates = daily_data.get('time', [])[:5]
        max_temps = daily_data.get('temperature_2m_max',[])[:5]
        min_temps = daily_data.get('temperature_2m_min',[])[:5]

        forecast = []
        for i in range(len(dates)):
            forecast.append({
                "date": dates[i],
                "max_temp": max_temps[i],
                "min_temp": min_temps[i]
            })

        print(forecast)

        return jsonify({
            "latitude": lat,
            "longitude": long,
            "forecast": forecast
        }), 200

    except Exception as e:
        return jsonify({"error"}),500

if __name__ == '__main__':
    app.run(port=5004, debug=True)