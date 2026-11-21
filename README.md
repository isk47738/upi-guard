# UPI Guard Pro – Real-Time Fake UPI Receipt Forensic Shield

> 🛡️ **Hackathon Round 3 Qualifier Project** | AI-powered forensic detector for fake UPI payment screenshots & spoof APKs

---

## 🔗 Quick Submission Links

| Material | Link |
| :--- | :--- |
| 🌐 **Live Web App** | [https://isk47738.github.io/upi-guard/](https://isk47738.github.io/upi-guard/) |
| 💻 **GitHub Repository** | [https://github.com/isk47738/upi-guard](https://github.com/isk47738/upi-guard) |
| 📱 **2nd Phone Test Simulator** | [https://isk47738.github.io/upi-guard/test_screens.html](https://isk47738.github.io/upi-guard/test_screens.html) |
| 📸 **Sample Photos & GIFs Gallery** | [https://isk47738.github.io/upi-guard/samples/](https://isk47738.github.io/upi-guard/samples/) |

> _No installation needed. Works on Android & iOS directly in browser. Offline PWA enabled._

---

## 📱 What it does

Campus canteens and small shops get shown **edited "Payment Successful" screenshots or FakePe spoof APK screens** to avoid paying. Staff have under 3 seconds to decide.

**UPI Guard Pro** lets any staff member aim their phone camera at the customer's phone and get a **✅ REAL / 🚨 FAKE** verdict in **0.43 seconds** — completely offline with zero server costs.

---

## 🔬 Core Innovations

1. **⚡ Green Tick Liveness Pulse Detector (1.2 Hz):** Captures rolling 15 FPS video frames to measure the genuine checkmark animation pulse. Static screenshots & spoof APKs have dead ticks and fail instantly!
2. **🔬 Dual-Zone Relative Error Level Analysis (ELA):** Mathematical compression noise disparity analysis between the amount zone and reference metadata card. Highlights digitally edited amounts in red.
3. **🔊 Canteen Soundbox 4G Gateway:** Multi-language voice announcements (Hindi, English, Punjabi, Marathi) with instant audio verification.
4. **🔁 Double-Spend Crypt-Ledger:** In-memory UTR hash table prevents the same screenshot from being reused across counters.
5. **📊 Loss Prevention Analytics Dashboard:** Real-time metrics showing verified volume, blocked fraud count, and saved revenue.

---

## 📲 Supported UPI Apps
- **Google Pay** (blue header, green tick)
- **PhonePe** (purple header)
- **Paytm** (cyan/blue header)

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/isk47738/upi-guard.git
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
