<div align="center">

# 🌿 Eco Sense AI

**Real-time acoustic environmental monitor.**

Tracks energy load, carbon output, and occupancy using only a microphone.

![Python](https://img.shields.io/badge/Python-3.8+-3572A5?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Signal_Processing-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Audio](https://img.shields.io/badge/sounddevice-Audio_Capture-4B8BBE?style=for-the-badge&logo=soundcloud&logoColor=white)

![Status](https://img.shields.io/badge/Status-Active-22d3a0?style=flat-square)
![No API Keys](https://img.shields.io/badge/API_Keys-Not_Required-blue?style=flat-square)
![Hardware](https://img.shields.io/badge/Hardware-Mic_Only-lightgrey?style=flat-square)

</div>

---

##  Overview

Eco Sense AI listens to ambient room audio and turns it into actionable sustainability data. No sensors, no hardware setup, no API keys. Just a microphone and Python.

Most buildings waste energy because nobody knows what's actually happening in a room at any given moment. Eco Sense AI solves this with a lightweight acoustic analysis engine that estimates how many people are present, how hard the HVAC system is working, and how many devices are active, all from sound alone.

Every second it updates a live terminal dashboard showing energy scores, estimated CO₂ output, electricity cost, and a plain English recommendation for reducing waste.

---

##  How It Works

The system captures a one second audio window from the microphone and extracts three acoustic features:

| Signal | Measured As | Proxy For |
|---|---|---|
| **Energy** (loudness) | RMS amplitude | Room activity level |
| **Activity** (variation) | Zero-crossing rate | Speech and movement |
| **Brightness** (tone) | Spectral centroid | Device and HVAC noise |

Those three signals feed into four estimates: occupancy count, HVAC load, device load, and an overall carbon/energy score. From the score it derives a CO₂ rate in kg/hour and an electricity cost in $/hour, then prints a targeted recommendation.

---

## 📟 Live Dashboard (Terminal Output)

```
ECO SENSE AI  Acoustic Energy & Carbon Monitor

Estimated occupancy:   8 people

Energy (loudness):     0.54  [##########----------]
Activity (variation):  0.61  [############--------]
Brightness (tone):     0.38  [########------------]
HVAC load:             0.47  [#########-----------]
Device load:           0.52  [##########----------]
Carbon/Energy score:   0.58  [###########---------]

   ≈ 2.90 kg CO₂ / hour
   ≈ $0.26 per hour in electricity

Recommendation:
   Minor improvements possible → small HVAC or device adjustments.
```

---

##  Getting Started

### Prerequisites
- Python 3.8+
- A working microphone

### Installation

```bash
# Clone the repo
git clone https://github.com/Kerima-001/eco-sense-ai.git
cd eco-sense-ai

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install sounddevice numpy
```

On some systems `sounddevice` requires PortAudio. Install it first:

```bash
# macOS
brew install portaudio

# Ubuntu / Debian
sudo apt-get install libportaudio2

# Windows
# No extra step needed, PortAudio is bundled with the pip package
```

### Run

```bash
python main.py
```

Press `Ctrl+C` to stop.

---

## 📂 Project Structure

```
eco-sense-ai/
├── main.py       # Core analysis loop and terminal dashboard
└── README.md
```

---

##  Tech Stack

| Layer | Tools |
|---|---|
| **Language** | Python 3.8+ |
| **Audio Capture** | sounddevice |
| **Signal Processing** | NumPy (FFT, RMS, ZCR) |
| **Output** | Terminal / CLI |

---

## ⚙️ Configuration

All tunable constants live at the top of `main.py`:

| Constant | Default | Description |
|---|---|---|
| `SAMPLE_RATE` | 16000 | Audio samples per second |
| `WINDOW_SEC` | 1.0 | Analysis window length |
| `MAX_OCCUPANCY` | 120 | Max people used for scaling |
| `MAX_CO2_KG_PER_HOUR` | 5.0 | Carbon rate ceiling |
| `ELECTRICITY_COST_PER_KWH` | 0.15 | Cost in USD |

---

##  Roadmap

* Web dashboard (Flask + Chart.js) for live browser visualization
* CSV logging for historical trend analysis
* Email or SMS alerts when carbon score exceeds a threshold
* Multi-room support with named microphone inputs
* Integration with smart home APIs (Google Home, Home Assistant)

---

<div align="center">

**Turning sound into sustainability insight.**

</div>
