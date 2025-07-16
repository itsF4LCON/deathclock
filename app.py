from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

def get_country_code(country_name):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        return response.json()[0]["cca3"]
    except:
        return None

def get_life_expectancy(country_name):
    code = get_country_code(country_name)
    if not code:
        return 72.6
    url = f"https://api.worldbank.org/v2/country/{code}/indicator/SP.DYN.LE00.IN?format=json"
    try:
        data = requests.get(url).json()
        for entry in data[1]:
            if entry["value"]:
                return entry["value"]
    except:
        pass
    return 72.6

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        age = int(request.form["age"])
        country = request.form["country"]
        smoker = request.form.get("smoker") == "yes"
        exercise = request.form.get("exercise") == "yes"
        diet = request.form["diet"]
        alcohol = request.form["alcohol"]
        sleep = request.form["sleep"]
        stress = request.form["stress"]
        medical = request.form["medical"]

        base_life = get_life_expectancy(country)
        seconds, estimated_life = estimate_life_seconds(age, base_life, smoker, exercise, diet, alcohol, sleep, stress, medical)
        death_date = datetime.now() + timedelta(seconds=seconds)

        return render_template("result.html", seconds=seconds, death_date=death_date.strftime('%Y-%m-%d'), life=estimated_life)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()