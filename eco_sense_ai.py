
import sounddevice as sd
import numpy as np
import time
import os

SAMPLE_RATE = 16000       # audio samples per second
WINDOW_SEC = 1.0          # analysis window length in seconds
MAX_OCCUPANCY = 120     # rough max people per room for scaling
MAX_CO2_KG_PER_HOUR = 5.0 # pretend "max" carbon rate 
ELECTRICITY_COST_PER_KWH = 0.15  # in  dollars


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def normalize01(x, low, high):
    if high == low:
        return 0.0
    return max(0.0, min(1.0, (x - low) / (high - low)))


def extract_audio_features(samples):
   
    if len(samples) == 0:
        return 0.0, 0.0, 0.0

    rms = np.sqrt(np.mean(samples ** 2))
    energy = normalize01(rms, 0.002, 0.1)

    zero_crossings = np.nonzero(np.diff(np.sign(samples)))[0].size
    zcr = zero_crossings / len(samples)
    activity = normalize01(zcr, 0.01, 0.25)

    mag = np.abs(np.fft.rfft(samples))
    freqs = np.fft.rfftfreq(len(samples), 1.0 / SAMPLE_RATE)
    if mag.sum() > 0:
        centroid = float(np.sum(freqs * mag) / np.sum(mag))
    else:
        centroid = 0.0
    brightness = normalize01(centroid, 300, 4000)

    return energy, activity, brightness


def estimate_occupancy(energy, activity):
  
    level = (energy + activity) / 2.0
    people = int(1 + level * (MAX_OCCUPANCY - 1))
    return max(1, min(MAX_OCCUPANCY, people))


def estimate_hvac_load(energy, brightness):
 
    low_freq_factor = 1.0 - brightness
    hvac = normalize01(0.7 * energy + 0.3 * low_freq_factor, 0.0, 1.0)
    return hvac


def estimate_device_load(brightness, activity):
  
    device = normalize01(0.6 * brightness + 0.4 * activity, 0.0, 1.0)
    return device


def compute_carbon_score(occupancy, hvac_load, device_load):
    
    occ_factor = occupancy / MAX_OCCUPANCY
    score = 0.4 * occ_factor + 0.3 * hvac_load + 0.3 * device_load
    return max(0.0, min(1.0, score))


def estimate_co2_and_cost(score):
  
    co2_per_hour = score * MAX_CO2_KG_PER_HOUR

    max_kw = 3.0
    kw = score * max_kw
    cost_per_hour = kw * ELECTRICITY_COST_PER_KWH

    return co2_per_hour, cost_per_hour


def make_recommendation(score, occupancy, hvac_load, device_load):
  
    if score > 0.75:
        return "High energy & carbon load → reduce HVAC or power down idle devices."
    if hvac_load > 0.6:
        return "HVAC load high → try raising setpoint 1°C or improving airflow."
    if device_load > 0.6:
        return "Many devices active → turn off or sleep unused laptops/displays."
    if occupancy < 3 and score > 0.4:
        return "Few people in room → consolidate activity into fewer spaces."
    if score < 0.25:
        return "Room is efficient right now "
    return "Minor improvements possible → small HVAC or device adjustments."


def bar(value, length=20):
    filled = int(round(value * length))
    return "[" + "#" * filled + "-" * (length - filled) + "]"


def main():
    sd.default.samplerate = SAMPLE_RATE
    print("Eco Sense AI starting microphone stream ...")
    time.sleep(1.0)

    try:
        while True:
            # 1) Re
            num_samples = int(SAMPLE_RATE * WINDOW_SEC)
            audio = sd.rec(num_samples, channels=1, dtype="float32")
            sd.wait()
            samples = audio[:, 0]

            # 2) Extract features
            energy, activity, brightness = extract_audio_features(samples)

            occupancy = estimate_occupancy(energy, activity)
            hvac_load = estimate_hvac_load(energy, brightness)
            device_load = estimate_device_load(brightness, activity)
            score = compute_carbon_score(occupancy, hvac_load, device_load)
            co2_per_hour, cost_per_hour = estimate_co2_and_cost(score)
            recommendation = make_recommendation(score, occupancy, hvac_load, device_load)

            
            clear_screen()
            print("ECO SENSE AI  Acoustic Energy & Carbon Monitor\n")
            print(f"Estimated occupancy:   {occupancy} people")
            print(f"Energy (loudness):     {energy:.2f}  {bar(energy)}")
            print(f"Activity (variation):  {activity:.2f}  {bar(activity)}")
            print(f"Brightness (tone):     {brightness:.2f}  {bar(brightness)}")
            print()
            print(f"HVAC load:             {hvac_load:.2f}  {bar(hvac_load)}")
            print(f"Device load:           {device_load:.2f}  {bar(device_load)}")
            print()
            print(f"Carbon/Energy score:{score:.2f}  {bar(score)}")
            print(f"   ≈ {co2_per_hour:.2f} kg CO₂ / hour")
            print(f"   ≈ ${cost_per_hour:.2f} per hour in electricity")
            print()
            print(" Recommendation:")
            print(f"   {recommendation}")
            print("\n(Press Ctrl+C in this window to stop.)")

    except KeyboardInterrupt:
        clear_screen()
        print("Eco Sense AI stopped by user.")
    except Exception as e:
        clear_screen()
        print(" Error in Eco Sense AI:", e)


if __name__ == "__main__":
    main()
