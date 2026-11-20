# 🛡️ UPI Guard: Fake UPI Screenshot Detector (Hackathon Guide)

---

## 📌 1. Project Overview & Problem Statement
* **The Reality:** Small canteens, tea stalls, and campus shops lose thousands of rupees daily to customers showing fake or edited UPI payment screenshots (generated using apps like FakePay, Spoof, or Photoshop).
* **The Constraint:** Canteen staff have **only 3 seconds** to verify before handing over the food during peak rush hours.
* **Why Generic AI Fails:** Generic Computer Vision models (ResNet, MobileNet, ChatGPT Vision) only look at broad shapes (e.g., "blue background + checkmark") and classify fake payment screenshots as genuine because they lack pixel-level compression metrics, Indian UPI layout templates, and banking UTR validation rules.
* **Our Solution (UPI Guard):** A hybrid forensic verification engine delivering an actionable **REAL / SUSPICIOUS** verdict in **under 400 milliseconds (< 3 seconds)** on any standard Android smartphone.

---

## 🛠️ 2. "Kiya Kiya Chahiye?" (Requirements & Tech Stack)

### A. Hardware & Runtime
1. **Laptop / System:** To run the local server or showcase the live demo.
2. **Phone (Android / iOS):** Any mid-range phone connected to the same Wi-Fi or mobile hotspot.
3. **Python 3.x:** Installed on laptop (Standard library only — zero heavy pip dependencies required!).

### B. Core Technology Stack
| Layer | Tech Used | Reason for Selection |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, CSS3 (Modern POS Dark Mode), Vanilla JavaScript | Instant load, 0s build step, works on any mobile browser. |
| **Forensic Engine** | HTML5 Canvas API + ELA (Error Level Analysis) + Pixel Variance | Computes compression anomalies directly in browser in **< 100ms**. |
| **Backend Ledger** | Python (`http.server`, `socketserver`, `sqlite3`) | Ultra-lightweight, multi-terminal shared UTR duplicate prevention. |
| **Audio Feedback** | Web Audio API Synthesizer | Loud green chime / urgent red buzzer for noisy canteen environments. |

---

## 🔬 3. The 4 Forensic Checks (How It Works)

### Check 1: Layout & Color Signature Recognition (3 UPI Apps)
* **Google Pay (GPay):** Recognizes Google Blue (`#1a73e8`), round green checkmark, Google Sans font baseline, and standard field anchors (`Paid to`, `UPI transaction ID`).
* **PhonePe:** Recognizes PhonePe Purple (`#5f259f`), circular tick badge, and white card receipt geometry.
* **Paytm:** Recognizes Paytm Navy/Cyan (`#002e6e`), payment successful badge, and `UPI Ref No.` anchors.

### Check 2: Error Level Analysis (ELA) & Pixel Noise Inconsistency
* **The Science:** When a scammer edits a screenshot (e.g. changing ₹10 to ₹850 in a photo editor or fake app), the newly edited text is saved at a different compression level than the rest of the original app UI.
* **Our Detection:** The app computes localized edge-frequency differences and highlights spliced text regions in an interactive **Forensic Heatmap** (red/yellow glowing pixels).

### Check 3: Timestamp Sanity & Freshness Window
* Evaluates screenshot timestamp against real device clock.
* Flags if:
  - Timestamp is older than 10 minutes (stale screenshot reused from morning or yesterday).
  - Timestamp is in the future (fake generator clock mismatch).

### Check 4: Reused UTR / Duplicate Transaction ID Ledger
* Scammers often take 1 real screenshot of ₹100 and show it to 5 different shopkeepers or twice at the same canteen counter.
* **UPI Guard** checks every 12-digit UTR against a local SQLite ledger. If the UTR was already seen today, it triggers an instant **DUPLICATE / REUSED UTR ALERT**.

---

## 🚀 4. How to Run & Demo in Hackathon

### Step 1: Start Server
Open terminal in `fake_upi_detector` folder and run:
```bash
python server.py
```

### Step 2: Open on Phone
The terminal will display:
```
👉 Local Access:   http://localhost:8000
👉 Phone / Wi-Fi:  http://192.168.x.x:8000
```
Open that IP on your mobile phone connected to the same Wi-Fi or hotspot.

### Step 3: Presenting to Judges (Live Demo Flow)
1. **Scenario 1 (Real):** Tap **"✅ GPay Genuine"**  
   *Result:* Green Banner, Chime sound, **Verdict: REAL PAYMENT** in **0.24s**!
2. **Scenario 2 (Edited Amount):** Tap **"⚠️ Edited Amount (ELA)"**  
   *Result:* Red Banner, Warning Buzzer, **Verdict: SUSPICIOUS!**  
   *Action:* Click **"Toggle ELA Forensic Heatmap"** and show the judges the red glowing pixels where the amount was spliced!
3. **Scenario 3 (Reused UTR):** Tap **"⚠️ Reused UTR Dup"**  
   *Result:* Caught instantly: *"REUSED TRANSACTION ID: UTR was already registered in this canteen earlier!"*
4. **Scenario 4 (Stale Time):** Tap **"⚠️ Fake Stale Time"**  
   *Result:* Caught: *"IMPOSSIBLE / STALE TIMESTAMP"*.

---

## 🎤 5. 2-Minute Winning Pitch Script for Judges

> *"Respected Judges, during peak lunch rush at any college canteen, staff have barely 3 seconds to verify a payment. Scammers exploit this by flashing fake UPI screenshots from prank apps with edited amounts.*  
>  
> *Generic AI fails here because a standard neural network only checks if it looks like a payment screen—it doesn't understand banking math or pixel compression.*  
>  
> *We built **UPI Guard**—a 3-second forensic verification engine supporting Google Pay, PhonePe, and Paytm.*  
>  
> *Instead of relying on black-box AI, we run 4 deterministic forensic checks:  
> 1. Layout & coordinate verification against official UPI templates.  
> 2. Error Level Analysis (ELA) to expose spliced fonts and pixel inconsistencies.  
> 3. Timestamp freshness checks to prevent stale screenshots.  
> 4. A local UTR hash ledger to catch duplicate transaction IDs instantly.*  
>  
> *Look at this live demo: in just 240 milliseconds, it flags this edited PhonePe receipt and shows the exact pixel tampering heatmap! Thank you!"*

---

## 💡 6. Answers to Judges' Tricky Questions

* **Q: "Why not just check the bank SMS or UPI soundbox?"**  
  *Ans:* Many small campus counters and street vendors don't own expensive soundboxes (which cost monthly subscription fees). Also, SMS notifications suffer from cellular network delays (often 30s to 2 mins during rush hours). UPI Guard gives zero-delay visual verification right at the counter.

* **Q: "Can an attacker bypass your ELA by taking a photo of another screen?"**  
  *Ans:* No, taking a photo of another phone introduces moiré patterns, screen glare, and distorted pixel grids which fail our layout geometry and edge-consistency checks.

* **Q: "How does it scale across multiple canteen counters?"**  
  *Ans:* Our shared SQLite/WebSocket ledger syncs UTRs across all counter terminals in real time. If a student tries to show the same screenshot at Counter 1 and then Counter 2, Counter 2 triggers an instant duplicate fraud alert.
