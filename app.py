from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import json
import logging

app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

try:
    with open('static/countries.json', 'r') as f:
        country_data = json.load(f)
except Exception as e:
    app.logger.error(f"Failed to load countries.json: {e}")
    country_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def calculate():
    try:
        data = request.get_json(force=True)
        app.logger.debug(f"Received data: {data}")

        age = int(data.get('age', 0))
        country = data.get('country', None)
        smoker = data.get('smoker', 'no')
        exercise = data.get('exercise', 'no')
        diet = data.get('diet', 'average')
        alcohol = data.get('alcohol', 'none')
        sleep = data.get('sleep', 'normal')
        stress = data.get('stress', 'medium')
        medical = data.get('medical', 'none')

        # Base life expectancy by country
        estimated_life = country_data.get(country, 75)

        # Lifestyle adjustments
        if smoker == "yes":
            estimated_life -= 5
        if exercise == "yes":
            estimated_life += 2
        if diet == "healthy":
            estimated_life += 2
        elif diet == "unhealthy":
            estimated_life -= 2
        if alcohol == "heavy":
            estimated_life -= 3
        elif alcohol == "light":
            estimated_life -= 1
        if sleep == "less":
            estimated_life -= 1
        elif sleep == "more":
            estimated_life += 0.5
        if stress == "high":
            estimated_life -= 2
        elif stress == "low":
            estimated_life += 1
        if medical == "some":
            estimated_life -= 2
        elif medical == "severe":
            estimated_life -= 5

        remaining_years = max(0, estimated_life - age)
        now = datetime.now()
        death_date = now + timedelta(days=remaining_years * 365.25)
        seconds_left = int((death_date - now).total_seconds())

        response = {
            'death_date': death_date.strftime('%d %B %Y'),
            'seconds': seconds_left
        }

        app.logger.debug(f"Response: {response}")
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error in calculation: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/countries')
def countries():
    return jsonify(sorted(country_data.keys()))
