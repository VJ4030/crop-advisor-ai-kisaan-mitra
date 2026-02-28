from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

OPENWEATHER_API_KEY = "a56c881b76ed126c2bc50d680af9f5e9"

# Home page with embedded HTML
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>KisaanMitra</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        input, select, button { padding: 10px; margin: 5px 0; width: 100%; }
        .chatbox { border: 1px solid #ccc; padding: 10px; max-height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <h1>KisaanMitra - Your Farming Assistant</h1>
    <select id="location">
        <option value="Ludhiana">Ludhiana</option>
        <option value="Jalandhar">Jalandhar</option>
        <option value="Ratnagiri">Ratnagiri</option>
        <option value="Raigad">Raigad</option>
    </select>
    <input type="text" id="crop" placeholder="Enter crop name" />
    <button onclick="getWeather()">Get Weather</button>
    <button onclick="getSoil()">Soil Info</button>
    <button onclick="getMarket()">Market Price</button>
    <div class="chatbox" id="chatbox"></div>

    <script>
        function appendMessage(msg) {
            let box = document.getElementById('chatbox');
            box.innerHTML += "<div>" + msg + "</div>";
            box.scrollTop = box.scrollHeight;
        }

        function getWeather() {
            let loc = document.getElementById('location').value;
            fetch("/weather", {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({location: loc})
            }).then(res => res.json())
              .then(data => appendMessage("Weather: " + data.message));
        }

        function getSoil() {
            let loc = document.getElementById('location').value;
            fetch("/soil", {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({location: loc})
            }).then(res => res.json())
              .then(data => appendMessage("Soil Info: " + data.message));
        }

        function getMarket() {
            let loc = document.getElementById('location').value;
            let crop = document.getElementById('crop').value;
            fetch("/market", {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({location: loc, crop: crop})
            }).then(res => res.json())
              .then(data => appendMessage("Market Price: " + data.message));
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/weather", methods=["POST"])
def weather():
    data = request.json
    location = data.get("location", "")
    lat, lon = get_coordinates(location)
    if lat is None:
        return jsonify({"message": "Invalid location"})
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    msg = f"{location}: {response['weather'][0]['description'].capitalize()}, Temp: {response['main']['temp']}°C"
    return jsonify({"message": msg})

@app.route("/soil", methods=["POST"])
def soil():
    data = request.json
    location = data.get("location", "")
    msg = f"Recommended soil for {location}: Loamy soil with balanced nutrients."
    return jsonify({"message": msg})

@app.route("/market", methods=["POST"])
def market():
    data = request.json
    location = data.get("location", "")
    crop = data.get("crop", "")
    msg = f"Current market price of {crop} in {location}: ₹ 1200 per quintal."
    return jsonify({"message": msg})

def get_coordinates(location):
    coords = {
        "Ludhiana": (30.9, 75.85),
        "Jalandhar": (31.33, 75.58),
        "Ratnagiri": (16.99, 73.3),
        "Raigad": (18.25, 73.15)
    }
    return coords.get(location, (None, None))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
