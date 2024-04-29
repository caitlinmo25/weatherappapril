from flask import Flask, render_template, request, jsonify
from cs50 import SQL
import requests
import datetime
import json  # Used for converting JSON data to string and vice versa

app = Flask(__name__)

# Setup the CS50 SQL connection to the SQLite database
db = SQL("sqlite:///weather.db")

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = 'b88cc12bb7fbe1e3980d1218fe79de72'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    location = request.form.get('location')
    q = f'{location},usa'
    # First try to fetch the data from the database
    weather = db.execute("SELECT * FROM weather_data WHERE location = :location ORDER BY timestamp DESC LIMIT 1", location=location)
    if weather and weather[0]['timestamp'] > (datetime.datetime.now() - datetime.timedelta(hours=3)).isoformat():
        # If recent data is available in the database, use it
        daily_weather = json.loads(weather[0]['weather_data'])
    else:
        # Otherwise, fetch new data from the API
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={q}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        if data.get('list'):
            daily_weather = data['list'][:7]
            # Convert JSON data to string to store in SQLite
            weather_json = json.dumps(daily_weather)
            db.execute("INSERT INTO weather_data (location, weather_data) VALUES (:location, :weather_data)", location=location, weather_data=weather_json)
        else:
            return render_template('error.html', message='Unable to fetch weather data')
    return render_template('weather.html', location=location, daily_weather=daily_weather)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
