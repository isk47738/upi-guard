with open(r'd:\web devlopment baba\fake_upi_detector\fast_scanner.html', 'r', encoding='utf-8') as f:
    code = f.read()

old_camera_code = """        async function startRealtimeCamera() {
            try {
                const constraints = {
                    video: {
                        facingMode: currentFacingMode,
                        width: { ideal: 1280 },
                        height: { ideal: 720 }
                    },
                    audio: false
                };

                videoStream = await navigator.mediaDevices.getUserMedia(constraints);
                video.srcObject = videoStream;
                await video.play();

                placeholder.style.display = 'none';
                imgPreview.style.display = 'none';
                verdictBox.style.display = 'none';
                video.style.display = 'block';
                laser.style.display = 'block';

                document.getElementById('btnLiveText').innerText = "Stop Real-Time Scanner";
                isRealTimeActive = true;

                requestAnimationFrame(realtimeInspectionLoop);

            } catch (err) {
                console.warn("Camera failed:", err);
                alert("Camera permission denied. If using Chrome, please allow camera permission or open via HTTPS!");
                stopRealtimeCamera();
            }
        }

        function stopRealtimeCamera() {
            if (videoStream) {
                videoStream.getTracks().forEach(t => t.stop());
                videoStream = null;
            }
            isRealTimeActive = false;
            isTorchOn = false;
            document.getElementById('btnTorch').classList.remove('active');
            video.style.display = 'none';
            laser.style.display = 'none';
            lockIndicator.style.display = 'none';
            placeholder.style.display = 'flex';
            targetBox.className = 'target-box';
            document.getElementById('btnLiveText').innerText = "Start Continuous Live Scanner";
            hudAppTracking.innerText = "Tracking Receipt...";
            hudDot.innerText = "🟢";

            const lChip = document.getElementById('hudLivenessChip');
            if (lChip) lChip.style.display = 'none';
            greenPulseHistory = [];
            liveTickPulsingDetected = false;
        }"""

new_camera_code = """        async function startRealtimeCamera() {
            try {
                isProcessing = false;
                lockProgress = 0;

                let stream = null;
                // Strategy 1: Ideal facingMode constraint
                try {
                    stream = await navigator.mediaDevices.getUserMedia({
                        video: { facingMode: { ideal: currentFacingMode } },
                        audio: false
                    });
                } catch (e1) {
                    console.warn("Strategy 1 failed, trying fallback to any camera:", e1);
                    // Strategy 2: Generic fallback for strict mobile drivers
                    stream = await navigator.mediaDevices.getUserMedia({
                        video: true,
                        audio: false
                    });
                }

                videoStream = stream;
                video.srcObject = videoStream;

                placeholder.style.display = 'none';
                imgPreview.style.display = 'none';
                verdictBox.style.display = 'none';
                video.style.display = 'block';
                laser.style.display = 'block';

                // Robust non-blocking play
                video.onloadedmetadata = () => {
                    video.play().catch(e => console.log("Play onloadedmetadata:", e));
                };
                video.play().catch(e => console.log("Play direct:", e));

                document.getElementById('btnLiveText').innerText = "Stop Real-Time Scanner";
                isRealTimeActive = true;

                requestAnimationFrame(realtimeInspectionLoop);

            } catch (err) {
                console.warn("Camera failed completely:", err);
                alert("Camera access failed (" + (err.name || err.message) + "). Please allow camera permissions in your browser or use 'Camera Snap' / 'Upload Photo' below!");
                stopRealtimeCamera();
            }
        }

        function stopRealtimeCamera() {
            if (videoStream) {
                videoStream.getTracks().forEach(t => t.stop());
                videoStream = null;
            }
            isRealTimeActive = false;
            isProcessing = false;
            lockProgress = 0;
            isTorchOn = false;
            const torchBtn = document.getElementById('btnTorch');
            if (torchBtn) torchBtn.classList.remove('active');
            video.style.display = 'none';
            laser.style.display = 'none';
            lockIndicator.style.display = 'none';
            placeholder.style.display = 'flex';
            targetBox.className = 'target-box';
            document.getElementById('btnLiveText').innerText = "Start Continuous Live Scanner";
            hudAppTracking.innerText = "Tracking Receipt...";
            hudDot.innerText = "🟢";

            const lChip = document.getElementById('hudLivenessChip');
            if (lChip) lChip.style.display = 'none';
            greenPulseHistory = [];
            liveTickPulsingDetected = false;
        }"""

if old_camera_code in code:
    code = code.replace(old_camera_code, new_camera_code)
    print("Replaced camera functions successfully!")
else:
    print("Could not find exact old_camera_code block, checking...")

# Also update resetScanner to reset isProcessing
old_reset = """        function resetScanner() {
            verdictBox.style.display = 'none';
            imgPreview.style.display = 'none';
            placeholder.style.display = 'flex';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }"""

new_reset = """        function resetScanner() {
            verdictBox.style.display = 'none';
            imgPreview.style.display = 'none';
            placeholder.style.display = 'flex';
            isProcessing = false;
            lockProgress = 0;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }"""

if old_reset in code:
    code = code.replace(old_reset, new_reset)
    print("Updated resetScanner successfully!")

with open(r'd:\web devlopment baba\fake_upi_detector\fast_scanner.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open(r'd:\web devlopment baba\fake_upi_detector\index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Both fast_scanner.html and index.html updated successfully!")
