from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Load country data with average life expectancy
with open('static/countries.json', 'r') as f:
    country_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def calculate():
    data = request.json

    age = int(data.get('age', 0))
    country = data.get('country')
    smoker = data.get('smoker')
    exercise = data.get('exercise')
    diet = data.get('diet')
    alcohol = data.get('alcohol')
    sleep = data.get('sleep')
    stress = data.get('stress')
    medical = data.get('medical')

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

    return jsonify({
        'death_date': death_date.strftime('%d %B %Y'),
        'seconds': seconds_left
    })

@app.route('/countries')
def countries():
    return jsonify(sorted(country_data.keys()))
