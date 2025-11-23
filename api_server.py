from flask import Flask, jsonify
import threading
import time
from eco_sense_ai import (
    SAMPLE_RATE, WINDOW_SEC,
    extract_audio_features, estimate_occupancy,
    estimate_hvac_load, estimate_device_load,
    compute_carbon_score, estimate_co2_and_cost
)
import sounddevice as sd
import numpy as np

app = Flask(__name__)

latest_data = {
    "occupancy": 0,
    "energy": 0,
    "activity": 0,
    "brightness": 0,
    "hvac": 0,
    "devices": 0,
    "score": 0,
    "co2": 0,
    "cost": 0,
    "recommendation": ""
}

def background_audio_loop():
    global latest_data
    while True:
        num_samples = int(SAMPLE_RATE * WINDOW_SEC)
        audio = sd.rec(num_samples, channels=1, dtype="float32")
        sd.wait()
        samples = audio[:, 0]

        energy, activity, brightness = extract_audio_features(samples)
        occupancy = estimate_occupancy(energy, activity)
        hvac = estimate_hvac_load(energy, brightness)
        devices = estimate_device_load(brightness, activity)
        score = compute_carbon_score(occupancy, hvac, devices)
        co2, cost = estimate_co2_and_cost(score)

        latest_data = {
            "occupancy": occupancy,
            "energy": round(energy, 2),
            "activity": round(activity, 2),
            "brightness": round(brightness, 2),
            "hvac": round(hvac, 2),
            "devices": round(devices, 2),
            "score": round(score, 2),
            "co2": round(co2, 2),
            "cost": round(cost, 2),
        }

        time.sleep(1)

@app.get("/live")
def live():
    return jsonify(latest_data)

thread = threading.Thread(target=background_audio_loop)
thread.daemon = True
thread.start()

app.run(port=5000)
