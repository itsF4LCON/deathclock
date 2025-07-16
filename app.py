from flask import Flask, request, jsonify, send_from_directory, render_template
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load countries data once on startup
COUNTRIES_FILE = os.path.join(app.static_folder, 'countries.json')
with open(COUNTRIES_FILE, encoding='utf-8') as f:
    countries_data = json.load(f)

# Create a dict for quick lookup of life expectancy by country name
life_expectancy_map = {c['name']: c['life_expectancy'] for c in countries_data}

DEFAULT_LIFE_EXPECTANCY = 75.0  # fallback if country missing

@app.route('/')
def index():
    # Assuming you have an index.html inside templates folder
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/countries')
def get_countries():
    # Optional: just in case you want to serve countries via this route
    return jsonify([c['name'] for c in countries_data])

@app.route('/', methods=['POST'])
def calculate_life():
    data = request.json

    try:
        age = float(data.get('age', 0))
        country = data.get('country', None)
        smoker = data.get('smoker', 'no')
        exercise = data.get('exercise', 'no')
        diet = data.get('diet', 'average')
        alcohol = data.get('alcohol', 'none')
        sleep = data.get('sleep', 'normal')
        stress = data.get('stress', 'medium')
        medical = data.get('medical', 'none')
    except Exception:
        return jsonify({'error': 'Invalid input data'}), 400

    # Get base life expectancy from country or default
    base_life = life_expectancy_map.get(country, DEFAULT_LIFE_EXPECTANCY)

    # Adjust life expectancy with simple logic (you can refine this)
    life_adj = 0

    if smoker == 'yes':
        life_adj -= 8  # smokers tend to live less
    if exercise == 'yes':
        life_adj += 4
    if diet == 'healthy':
        life_adj += 3
    elif diet == 'unhealthy':
        life_adj -= 3
    if alcohol == 'heavy':
        life_adj -= 4
    elif alcohol == 'light':
        life_adj += 1
    if sleep == 'less':
        life_adj -= 2
    elif sleep == 'more':
        life_adj += 1
    if stress == 'high':
        life_adj -= 3
    elif stress == 'low':
        life_adj += 2
    if medical == 'some':
        life_adj -= 5
    elif medical == 'severe':
        life_adj -= 10

    estimated_life = base_life + life_adj
    if estimated_life < age:
        estimated_life = age + 1  # ensure life expectancy > current age

    remaining_years = estimated_life - age

    now = datetime.now()
    death_date = now + timedelta(days=remaining_years * 365.25)
    seconds_left = int(remaining_years * 365.25 * 24 * 3600)

    death_date_str = death_date.strftime('%Y-%m-%d')

    return jsonify({
        'death_date': death_date_str,
        'life': remaining_years,
        'seconds': seconds_left,
    })

if __name__ == '__main__':
    app.run(debug=True)
