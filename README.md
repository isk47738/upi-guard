# UPI Guard – Fake UPI Payment Screenshot Detector

> 🛡️ **Hackathon Project** | AI-powered forensic detector for fake UPI payment screenshots

## 🌐 Live App
**Open on any phone, anywhere:**  
👉 [https://YOUR_USERNAME.github.io/upi-guard](https://YOUR_USERNAME.github.io/upi-guard)

> _No installation needed. Works on Android & iOS directly in browser. Install as native app via "Add to Home Screen"._

---

## 📱 What it does

Campus canteens and small shops get shown **edited "Payment Successful" screenshots** to avoid paying. Staff have 3 seconds to decide.

**UPI Guard** lets any staff member snap or upload a payment screenshot and get a **✅ REAL / 🚨 FAKE** verdict in under 3 seconds.

---

## 🔬 5-Layer Forensic Engine

| Check | What it detects |
|-------|----------------|
| 📐 **Aspect Ratio** | Non-mobile screenshot dimensions (cropped/resized fakes) |
| 🔬 **ELA Pixel Scan** | High edge-ratio & variance = digitally spliced amount text |
| 📦 **Compression Noise** | Block-level JPEG noise anomalies in edited regions |
| 🎨 **Color Profile** | Background white ratio mismatch — colored overlays from editing |
| 🔁 **UTR Duplicate** | Same transaction ID reused across customers |

---

## 📲 Supported UPI Apps
- **Google Pay** (blue header, green tick)
- **PhonePe** (purple header)
- **Paytm** (cyan/blue header)

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/upi-guard.git
cd upi-guard

# Start server (Python required)
python server.py

# Open in browser
# Laptop: http://localhost:8000
# Phone (same Wi-Fi): http://<your-ip>:8000
```

---

## 🏆 Hackathon Context

**Problem:** Merchants near campus lose money to fake UPI screenshots.  
**Solution:** 3-second forensic scan, works offline, installs as native app (PWA).  
**Why AI alone fails:** Generic models don't know what genuine receipts from each app look like — we built custom reference forensics.

---

## 📂 Project Structure

```
upi-guard/
├── fast_scanner.html   ← Main app (self-contained, offline-capable)
├── manifest.json       ← PWA manifest (Android install support)
├── service-worker.js   ← Offline cache handler
├── server.py           ← Local Python server with SQLite UTR backend
└── HACKATHON_GUIDE.md  ← Pitch script & judge Q&A
```

---

## 👨‍💻 Tech Stack

- **Frontend:** Pure HTML5 + CSS3 + Vanilla JS (zero dependencies)
- **Forensics:** Canvas API + ELA pixel analysis + color histogram
- **Backend:** Python stdlib HTTP server + SQLite
- **PWA:** Service Worker + Web App Manifest
- **Deployment:** GitHub Pages (HTTPS, free, global)

---

_Built for hackathon · LPU · 2026_
