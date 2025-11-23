// src/App.js
import React, { useEffect, useState } from "react";
import "./App.css";
import ecoLogo from "./assets/eco-logo.png"; // keep your logo here

const API_URL = "http://127.0.0.1:5000/metrics"; // Flask endpoint

function App() {
  const [metrics, setMetrics] = useState({
    occupancy: 4,
    carbon_score: 0.61,
    hvac_load: 0.4,
    device_load: 0.55,
    co2_per_hour: 1.9,
    cost_per_hour: 0.22,
    recommendation:
      "Reduce AC by 1°C and power down 2 idle laptops to save ~12% energy.",
    lastUpdated: null,
  });

  const [isLive, setIsLive] = useState(false);

  // Helper: format money nicely
  const formatMoney = (value) => {
    if (value === null || value === undefined) return "$0.00";
    return `$${value.toFixed(2)}`;
  };

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error("Network response was not ok");
        const data = await res.json();

        setMetrics((prev) => ({
          ...prev,
          ...data,
          lastUpdated: new Date().toLocaleTimeString(),
        }));
        setIsLive(true);
      } catch (err) {
        console.error("Error fetching metrics:", err);
        setIsLive(false);
      }
    }

    // initial fetch
    fetchMetrics();
    // poll every 2 seconds
    const id = setInterval(fetchMetrics, 2000);
    return () => clearInterval(id);
  }, []);

  const moneyPerHour = metrics.cost_per_hour ?? metrics.carbon_score * 0.25; // fallback

  return (
    <div className="app-root">
      <div className="app-shell">
        {/* Main card */}
        <main className="app-card">
          <header className="app-header">
            <div className="logo-ring">
              <img src={ecoLogo} alt="Eco Sense AI logo" className="logo-img" />
            </div>
            <div className="title-block">
              <h1 className="app-title">Eco Sense AI</h1>
              <p className="app-subtitle">
                Acoustic energy &amp; cost intelligence for every room.
              </p>
              <p className="app-pill">
                {isLive ? "Live monitoring" : "Waiting for data…"}
              </p>
            </div>
          </header>

          {/* Top row: people + $/hour */}
          <section className="top-metrics">
            <div className="metric-card metric-primary">
              <span className="metric-label">Estimated occupancy</span>
              <span className="metric-value big">
                {metrics.occupancy ?? "–"}{" "}
                <span className="metric-unit">people</span>
              </span>
            </div>

            <div className="metric-card metric-money">
              <span className="metric-label">Estimated energy cost</span>
              <span className="metric-value big">
                {formatMoney(moneyPerHour)}{" "}
                <span className="metric-unit">per hour</span>
              </span>
              <span className="metric-hint">
                (live estimate based on room noise &amp; load)
              </span>
            </div>
          </section>

          {/* Bars row */}
          <section className="bars-section">
            <div className="bar-metric">
              <div className="bar-label-row">
                <span>HVAC load</span>
                <span className="bar-value">
                  {(metrics.hvac_load * 100).toFixed(0)}%
                </span>
              </div>
              <div className="bar-track">
                <div
                  className="bar-fill hvac"
                  style={{ width: `${(metrics.hvac_load || 0) * 100}%` }}
                />
              </div>
            </div>

            <div className="bar-metric">
              <div className="bar-label-row">
                <span>Device load</span>
                <span className="bar-value">
                  {(metrics.device_load * 100).toFixed(0)}%
                </span>
              </div>
              <div className="bar-track">
                <div
                  className="bar-fill devices"
                  style={{ width: `${(metrics.device_load || 0) * 100}%` }}
                />
              </div>
            </div>

            <div className="bar-metric">
              <div className="bar-label-row">
                <span>Overall energy score</span>
                <span className="bar-value">
                  {(metrics.carbon_score * 100).toFixed(0)} / 100
                </span>
              </div>
              <div className="bar-track">
                <div
                  className="bar-fill score"
                  style={{ width: `${(metrics.carbon_score || 0) * 100}%` }}
                />
              </div>
            </div>
          </section>

          {/* Recommendation + footer */}
          <section className="recommendation">
            <div className="rec-icon">💡</div>
            <div>
              <h2>Smart recommendation</h2>
              <p>{metrics.recommendation}</p>
              {metrics.lastUpdated && (
                <p className="timestamp">
                  Last updated at {metrics.lastUpdated}
                </p>
              )}
            </div>
          </section>

          <footer className="app-footer">
            <button
              className="primary-btn"
              onClick={() => window.location.reload()}
            >
              Refresh view
            </button>
            <button
              className="ghost-btn"
              onClick={() =>
                window.open("https://github.com", "_blank", "noreferrer")
              }
            >
              View GitHub repo
            </button>
          </footer>
        </main>
      </div>
    </div>
  );
}

export default App;
