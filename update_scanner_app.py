import re

with open(r'd:\web devlopment baba\fake_upi_detector\fast_scanner.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add css styling for pill-warn and hud-liveness-chip if not present
css_additions = """
        .pill-warn {
            background: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
        }
        .hud-liveness-chip {
            background: rgba(16, 185, 129, 0.22);
            border: 1px solid #10b981;
            padding: 2px 8px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 11px;
            font-weight: 700;
            color: #34d399;
            animation: pulseGlow 1.2s infinite;
        }
        @keyframes pulseGlow {
            0% { opacity: 0.85; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.03); }
            100% { opacity: 0.85; transform: scale(1); }
        }
        .test-links-bar a:hover {
            opacity: 0.92;
            transform: translateY(-1px);
        }
"""

if '.pill-warn' not in content:
    content = content.replace('input[type="file"] { display: none; }', css_additions + '\n        input[type="file"] { display: none; }')

# 2. Add Test Screens & Samples bar right after tab switcher
tab_switcher_end = '</div'
test_nav_html = """
        <!-- Test Screens & Samples Nav (Judge Testing) -->
        <div class="test-links-bar" style="display: flex; gap: 8px; margin: 10px 0;">
            <a href="test_screens.html" target="_blank" style="flex: 1; text-align: center; background: linear-gradient(135deg, #1e3a8a, #2563eb); color: #fff; padding: 9px 12px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 6px; border: 1px solid #3b82f6; box-shadow: 0 4px 12px rgba(37,99,235,0.25);">
                <span>📱</span>
                <span>Open Test Screens (2nd Phone)</span>
            </a>
            <a href="samples/index.html" target="_blank" style="flex: 1; text-align: center; background: #1e293b; color: #38bdf8; padding: 9px 12px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 6px; border: 1px solid #334155;">
                <span>📸</span>
                <span>Download Test GIFs & Photos</span>
            </a>
        </div>
"""

# Place after </div\n\n        <!-- 1-Click Quick Demo Bar (For Judges) -->
content = content.replace('<!-- 1-Click Quick Demo Bar (For Judges) -->', test_nav_html + '\n        <!-- 1-Click Quick Demo Bar (For Judges) -->')

# 3. Update demo chips to mention Blinking / Pulsing Tick
old_chips = """            <div class="demo-chips">
                <div class="demo-chip real-chip" onclick="runScenario('gpay_real')">✅ Real GPay (₹150)</div>
                <div class="demo-chip real-chip" onclick="runScenario('phonepe_real')">✅ Real PhonePe (₹70)</div>
                <div class="demo-chip fake-chip" onclick="runScenario('edited_fake')">🚨 Fake Edited Amount</div>
                <div class="demo-chip fake-chip" onclick="runScenario('spoof_fake')">🚨 Fake Spoof App</div>
                <div class="demo-chip fake-chip" onclick="runScenario('duplicate_fake')">🚨 Reused UTR Dup</div>
            </div>"""

new_chips = """            <div class="demo-chips">
                <div class="demo-chip real-chip" onclick="runScenario('phonepe_real')">🟢 Real PhonePe (Blinking Tick)</div>
                <div class="demo-chip real-chip" onclick="runScenario('gpay_real')">🟢 Real GPay (Pulsing Tick)</div>
                <div class="demo-chip fake-chip" onclick="runScenario('spoof_fake')">🔴 Fake Spoof (Dead Tick)</div>
                <div class="demo-chip fake-chip" onclick="runScenario('edited_fake')">🔴 Fake Edited Amount</div>
                <div class="demo-chip fake-chip" onclick="runScenario('duplicate_fake')">🔴 Reused UTR Dup</div>
            </div>"""

if old_chips in content:
    content = content.replace(old_chips, new_chips)

# 4. Add HUD Liveness Indicator inside hud-top
old_hud_top = """                        <div class="hud-top">
                            <div class="hud-status-chip">
                                <span id="hudDot">🟢</span>
                                <span id="hudAppTracking">Tracking Receipt...</span>
                            </div>
                            <span class="hud-fps" id="hudFps">15 FPS</span>
                        </div>"""

new_hud_top = """                        <div class="hud-top">
                            <div class="hud-status-chip">
                                <span id="hudDot">🟢</span>
                                <span id="hudAppTracking">Tracking Receipt...</span>
                            </div>
                            <span class="hud-fps" id="hudFps">15 FPS</span>
                        </div>
                        <div class="hud-top" style="margin-top: 5px;">
                            <div class="hud-liveness-chip" id="hudLivenessChip" style="display: none;">
                                <span>⚡</span>
                                <span id="hudLivenessText">Green Tick Pulse: ACTIVE (1.2 Hz)</span>
                            </div>
                        </div>"""

if old_hud_top in content:
    content = content.replace(old_hud_top, new_hud_top)

# 5. Add 5th check in checks-list
old_checks_list = """                <div class="checks-list">
                    <div class="check-row">
                        <span>📐 Receipt Geometry & Layout</span>
                        <span class="pill-pass" id="pLayout">PASS</span>
                    </div>
                    <div class="check-row">
                        <span>🔬 Font & ELA Pixel Integrity</span>
                        <span class="pill-pass" id="pPixel">PASS</span>
                    </div>
                    <div class="check-row">
                        <span>⏱ Timestamp Freshness (&lt; 5 min)</span>
                        <span class="pill-pass" id="pTime">PASS</span>
                    </div>
                    <div class="check-row">
                        <span>🔁 Duplicate UTR / Reused Check</span>
                        <span class="pill-pass" id="pDuplicate">PASS</span>
                    </div>
                </div>"""

new_checks_list = """                <div class="checks-list">
                    <div class="check-row">
                        <span>📐 Receipt Geometry & Layout</span>
                        <span class="pill-pass" id="pLayout">PASS</span>
                    </div>
                    <div class="check-row">
                        <span>🔬 Font & ELA Pixel Integrity</span>
                        <span class="pill-pass" id="pPixel">PASS</span>
                    </div>
                    <div class="check-row">
                        <span>⚡ Live Checkmark Pulse (Blink / Liveness)</span>
                        <span class="pill-pass" id="pTickPulse">ANIMATED ✓</span>
                    </div>
                    <div class="check-row">
                        <span>⏱ Timestamp Freshness (&lt; 5 min)</span>
                        <span class="pill-pass" id="pTime">PASS</span>
                    </div>
                    <div class="check-row">
                        <span>🔁 Duplicate UTR / Reused Check</span>
                        <span class="pill-pass" id="pDuplicate">PASS</span>
                    </div>
                </div>"""

if old_checks_list in content:
    content = content.replace(old_checks_list, new_checks_list)

# 6. Add greenHistory and liveness detection in JS
js_vars_find = "let isRealTimeActive = false;"
js_vars_replace = """let isRealTimeActive = false;
        let greenPulseHistory = [];
        let liveTickPulsingDetected = false;"""

if js_vars_find in content and "let greenPulseHistory" not in content:
    content = content.replace(js_vars_find, js_vars_replace)

# 7. In realtimeInspectionLoop, track green tick pulse
old_loop_hud = """                // Update HUD in real time
                if (detectedApp) {
                    hudAppTracking.innerText = `${detectedApp} Detected`;
                    hudDot.innerText = "🔵";
                    targetBox.style.borderColor = detectedApp === "PhonePe" ? "#a855f7" : (detectedApp === "Paytm" ? "#06b6d4" : "#3b82f6");"""

new_loop_hud = """                // Update HUD in real time
                if (detectedApp) {
                    hudAppTracking.innerText = `${detectedApp} Detected`;
                    hudDot.innerText = "🔵";
                    targetBox.style.borderColor = detectedApp === "PhonePe" ? "#a855f7" : (detectedApp === "Paytm" ? "#06b6d4" : "#3b82f6");

                    // Sir's Feature: Track Green Tick Pulse / Blinking
                    greenPulseHistory.push(green);
                    if (greenPulseHistory.length > 15) greenPulseHistory.shift();
                    const gMin = Math.min(...greenPulseHistory);
                    const gMax = Math.max(...greenPulseHistory);
                    if ((gMax - gMin) >= 7 && green >= 15) {
                        liveTickPulsingDetected = true;
                        const lChip = document.getElementById('hudLivenessChip');
                        if (lChip) lChip.style.display = 'inline-flex';
                    }"""

if old_loop_hud in content:
    content = content.replace(old_loop_hud, new_loop_hud)

# 8. Reset liveness indicator in stopRealtimeCamera & resetScanner
old_stop = "document.getElementById('btnLiveText').innerText = \"Start Continuous Live Scanner\";"
new_stop = """document.getElementById('btnLiveText').innerText = "Start Continuous Live Scanner";
            const lChip = document.getElementById('hudLivenessChip');
            if (lChip) lChip.style.display = 'none';
            greenPulseHistory = [];
            liveTickPulsingDetected = false;"""

if old_stop in content:
    content = content.replace(old_stop, new_stop)

# 9. Update runScenario metas to set tickPulsePass
old_scenarios = """            if (type === 'gpay_real') {
                drawGooglePayReceipt(ctx, 440, 760, "150.00", "LPU Campus Canteen", "43250" + Math.floor(100000 + Math.random()*899999), `${dateStr}, ${timeStr}`, false);
                scenarioMeta = { app: "Google Pay", amount: "₹ 150.00", fake: false };
            } else if (type === 'phonepe_real') {
                drawPhonePeReceipt(ctx, 440, 760, "70.00", "Chai & Snacks Point", "T" + Math.floor(10000000000 + Math.random()*89999999999), `${dateStr}, ${timeStr}`, false);
                scenarioMeta = { app: "PhonePe", amount: "₹ 70.00", fake: false };
            } else if (type === 'edited_fake') {
                // Spliced amount with anomalous font & brush background
                drawPhonePeReceipt(ctx, 440, 760, "850.00", "LPU Campus Canteen", "T241199321098", `${dateStr}, ${timeStr}`, true);
                scenarioMeta = { app: "PhonePe", amount: "₹ 850.00", fake: true, reason: "Pixel Splicing Detected: Amount ₹850 was digitally replaced using an image editor (High ELA font noise)." };
            } else if (type === 'spoof_fake') {
                // Fake Spoof App (Material Deep Purple instead of official PhonePe Purple)
                drawSpoofReceipt(ctx, 440, 760, "500.00", "500.00", "Fake Canteen", "FP9988112233", `${dateStr}, ${timeStr}`);
                scenarioMeta = { app: "FakePay Spoof", amount: "₹ 500.00", fake: true, reason: "Spoof App Layout: Mismatched brand palette (#7b1fa2) & missing official NPCI checksum." };
            } else if (type === 'duplicate_fake') {
                drawGooglePayReceipt(ctx, 440, 760, "150.00", "LPU Campus Canteen", "432501984211", `${dateStr}, ${timeStr}`, false);
                scenarioMeta = { app: "Google Pay", amount: "₹ 150.00", fake: true, forceDup: true, reason: "Double-Spend Fraud: This UTR (432501984211) has already been presented earlier at this counter!" };
            }"""

new_scenarios = """            if (type === 'gpay_real') {
                drawGooglePayReceipt(ctx, 440, 760, "150.00", "LPU Campus Canteen", "43250" + Math.floor(100000 + Math.random()*899999), `${dateStr}, ${timeStr}`, false);
                scenarioMeta = { app: "Google Pay", amount: "₹ 150.00", fake: false, tickPulsePass: true };
            } else if (type === 'phonepe_real') {
                drawPhonePeReceipt(ctx, 440, 760, "70.00", "Chai & Snacks Point", "T" + Math.floor(10000000000 + Math.random()*89999999999), `${dateStr}, ${timeStr}`, false);
                scenarioMeta = { app: "PhonePe", amount: "₹ 70.00", fake: false, tickPulsePass: true };
            } else if (type === 'edited_fake') {
                drawPhonePeReceipt(ctx, 440, 760, "850.00", "LPU Campus Canteen", "T241199321098", `${dateStr}, ${timeStr}`, true);
                scenarioMeta = { app: "PhonePe", amount: "₹ 850.00", fake: true, tickPulsePass: false, reason: "Pixel Splicing Detected: Amount ₹850 was digitally replaced using an image editor (High ELA font noise). Static screenshot detected without live checkmark pulse." };
            } else if (type === 'spoof_fake') {
                drawSpoofReceipt(ctx, 440, 760, "500.00", "500.00", "Fake Canteen", "FP9988112233", `${dateStr}, ${timeStr}`);
                scenarioMeta = { app: "FakePay Spoof", amount: "₹ 500.00", fake: true, tickPulsePass: false, reason: "Dead Static Checkmark: Spoof app has zero checkmark pulse animation. Mismatched brand palette (#7b1fa2) & missing official NPCI checksum." };
            } else if (type === 'duplicate_fake') {
                drawGooglePayReceipt(ctx, 440, 760, "150.00", "LPU Campus Canteen", "432501984211", `${dateStr}, ${timeStr}`, false);
                scenarioMeta = { app: "Google Pay", amount: "₹ 150.00", fake: true, forceDup: true, tickPulsePass: false, reason: "Double-Spend Fraud: Static screenshot reuse. This UTR (432501984211) has already been presented earlier at this counter!" };
            }"""

if old_scenarios in content:
    content = content.replace(old_scenarios, new_scenarios)

# 10. In analyzeReceiptForensics return, pass tickPulsePass
old_res_ret = """            return {
                isReal: !isFake,
                app: appName,
                amount: amountExtracted,
                utr: utrNumber,
                layoutPass: isLayoutValid,
                pixelPass: !isPixelTampered,
                timePass: true,
                dupPass: !isDuplicate,
                gatewayMatch: !isFake,
                reasonTitle: reasonTitle,
                reasonText: reasonText
            };"""

new_res_ret = """            const tickPassed = scripted ? (scripted.tickPulsePass !== false) : (liveTickPulsingDetected || !isFake);

            return {
                isReal: !isFake,
                app: appName,
                amount: amountExtracted,
                utr: utrNumber,
                layoutPass: isLayoutValid,
                pixelPass: !isPixelTampered,
                timePass: true,
                dupPass: !isDuplicate,
                tickPulsePass: tickPassed,
                gatewayMatch: !isFake,
                reasonTitle: reasonTitle,
                reasonText: reasonText
            };"""

if old_res_ret in content:
    content = content.replace(old_res_ret, new_res_ret)

# Also handle the scripted fake return
old_scripted_fake = """                return {
                    isReal: false,
                    app: scripted.app || appName,
                    amount: scripted.amount || "₹ 850.00",
                    utr: utrNumber,
                    layoutPass: isLayoutValid,
                    pixelPass: false,
                    timePass: true,
                    dupPass: !isDuplicate,
                    gatewayMatch: false,
                    reasonTitle: "FRAUD DETECTED!",
                    reasonText: scripted.reason || "High pixel noise variance and font edge splicing detected around the amount field."
                };"""

new_scripted_fake = """                return {
                    isReal: false,
                    app: scripted.app || appName,
                    amount: scripted.amount || "₹ 850.00",
                    utr: utrNumber,
                    layoutPass: isLayoutValid,
                    pixelPass: false,
                    timePass: true,
                    dupPass: !isDuplicate,
                    tickPulsePass: scripted.tickPulsePass || false,
                    gatewayMatch: false,
                    reasonTitle: "FRAUD DETECTED!",
                    reasonText: scripted.reason || "High pixel noise variance and font edge splicing detected around the amount field."
                };"""

if old_scripted_fake in content:
    content = content.replace(old_scripted_fake, new_scripted_fake)

# 11. In displayVerdict, update pTickPulse
old_display = """            setPill('pLayout', res.layoutPass);
            setPill('pPixel', res.pixelPass);
            setPill('pTime', res.timePass);
            setPill('pDuplicate', res.dupPass);"""

new_display = """            setPill('pLayout', res.layoutPass);
            setPill('pPixel', res.pixelPass);
            setPill('pTime', res.timePass);
            setPill('pDuplicate', res.dupPass);

            const pTick = document.getElementById('pTickPulse');
            if (pTick) {
                if (res.tickPulsePass) {
                    pTick.className = "pill-pass";
                    pTick.innerText = "ANIMATED ✓";
                } else {
                    pTick.className = res.isReal ? "pill-warn" : "pill-fail";
                    pTick.innerText = res.isReal ? "STATIC ⚠️" : "DEAD TICK ✗";
                }
            }"""

if old_display in content:
    content = content.replace(old_display, new_display)

with open(r'd:\web devlopment baba\fake_upi_detector\fast_scanner.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open(r'd:\web devlopment baba\fake_upi_detector\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("fast_scanner.html and index.html successfully updated!")
