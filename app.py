from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Get list of countries from Rest Countries API for dropdown
@app.route('/countries')
def countries():
    try:
        response = requests.get('https://restcountries.com/v3.1/all')
        response.raise_for_status()
        countries = sorted([c['name']['common'] for c in response.json()])
        return jsonify(countries)
    except Exception:
        return jsonify([])

def estimate_life_seconds(age, base_life, smoker, exercise, diet, alcohol, sleep, stress, medical):
    life = base_life
    if smoker: life -= 8
    if exercise: life += 3
    if diet == "unhealthy": life -= 2
    elif diet == "healthy": life += 2
    if alcohol == "heavy": life -= 4
    elif alcohol == "light": life -= 1
    if sleep == "less": life -= 2
    if stress == "high": life -= 2
    if medical == "severe": life -= 5
    elif medical == "some": life -= 2

    years_left = max(0, life - age)
    seconds_left = int(years_left * 365.25 * 24 * 60 * 60)
    return seconds_left, life

def get_life_expectancy(country_name):
    try:
        # Use Rest Countries API to get cca3 code
        c_response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        c_response.raise_for_status()
        code = c_response.json()[0]["cca3"]

        # Use World Bank API for life expectancy
        url = f"https://api.worldbank.org/v2/country/{code}/indicator/SP.DYN.LE00.IN?format=json"
        data = requests.get(url).json()
        for entry in data[1]:
            if entry["value"]:
                return entry["value"]
    except Exception:
        pass
    return 72.6  # fallback average

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        age = int(data.get("age"))
        country = data.get("country")
        smoker = data.get("smoker") == "yes"
        exercise = data.get("exercise") == "yes"
        diet = data.get("diet")
        alcohol = data.get("alcohol")
        sleep = data.get("sleep")
        stress = data.get("stress")
        medical = data.get("medical")

        base_life = get_life_expectancy(country)
        seconds, estimated_life = estimate_life_seconds(age, base_life, smoker, exercise, diet, alcohol, sleep, stress, medical)
        death_date = datetime.now() + timedelta(seconds=seconds)

        return {
            "seconds": seconds,
            "death_date": death_date.strftime('%Y-%m-%d'),
            "life": estimated_life
        }
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
