import os
from PIL import Image, ImageDraw, ImageFont

samples_dir = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(samples_dir, exist_ok=True)

# Helper to draw a checkmark
def draw_check(draw, cx, cy, radius, stroke_color, stroke_width):
    # checkmark coordinates
    p1 = (cx - radius * 0.45, cy)
    p2 = (cx - radius * 0.1, cy + radius * 0.38)
    p3 = (cx + radius * 0.5, cy - radius * 0.35)
    draw.line([p1, p2, p3], fill=stroke_color, width=stroke_width, joint="curve")

# 1. GENERATE ANIMATED GIF FOR PHONEPE (With green checkmark blinking / pulsing)
phonepe_frames = []
w, h = 400, 650

# 12 frames of smooth pulse (scale 1.0 to 1.15 and back)
import math
for f in range(16):
    im = Image.new("RGB", (w, h), color="#f5f6f8")
    d = ImageDraw.Draw(im)

    # Header bar
    d.rectangle([0, 0, w, 70], fill="#5f259f")
    d.text((w//2 - 40, 25), "PhonePe", fill="#ffffff")

    # Animated green tick pulse
    pulse_factor = 1.0 + 0.12 * math.sin(f * (2 * math.pi / 16))
    r = int(45 * pulse_factor)
    cx, cy = w // 2, 160

    # Ripple ring when expanding
    if f < 10:
        ripple_r = int(50 + f * 4.5)
        alpha_color = "#a7f3d0" if f % 2 == 0 else "#6ee7b7"
        d.ellipse([cx - ripple_r, cy - ripple_r, cx + ripple_r, cy + ripple_r], outline=alpha_color, width=3)

    # Green circle
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#10b981")
    # White checkmark
    draw_check(d, cx, cy, r, "#ffffff", int(7 * pulse_factor))

    # Payment details
    d.text((w//2 - 75, 230), "Payment Successful", fill="#0f172a")
    d.text((w//2 - 60, 275), "Rs. 150.00", fill="#0f172a")
    d.text((w//2 - 65, 320), "Paid to Campus Canteen", fill="#475569")

    # Card box
    d.rectangle([25, 360, w - 25, 590], fill="#ffffff", outline="#e2e8f0", width=1)
    d.text((40, 380), "Transaction Details", fill="#5f259f")
    d.line([40, 410, w - 40, 410], fill="#f1f5f9", width=1)
    d.text((40, 425), "Transaction ID", fill="#64748b")
    d.text((40, 445), "T24112021594839201", fill="#0f172a")

    d.text((40, 485), "Debited from State Bank of India", fill="#64748b")
    d.text((40, 505), "UTR: 432589012345", fill="#0f172a")

    d.text((40, 545), "Date & Time: 21 Nov 2026, 02:45 AM", fill="#64748b")

    phonepe_frames.append(im)

gif_path = os.path.join(samples_dir, "real_phonepe_tick_blink.gif")
phonepe_frames[0].save(gif_path, save_all=True, append_images=phonepe_frames[1:], duration=80, loop=0)
print(f"Generated {gif_path}")

# 2. GENERATE REAL PHONEPE STATIC SAMPLE (Frame 0)
real_pp_path = os.path.join(samples_dir, "real_phonepe_sample.png")
phonepe_frames[4].save(real_pp_path)
print(f"Generated {real_pp_path}")

# 3. GENERATE REAL GOOGLE PAY SAMPLE & ANIMATED GIF
gpay_frames = []
for f in range(16):
    im = Image.new("RGB", (w, h), color="#ffffff")
    d = ImageDraw.Draw(im)

    # GPay top bar
    d.rectangle([0, 0, w, 65], fill="#1a73e8")
    d.text((w//2 - 45, 25), "Google Pay", fill="#ffffff")

    # Animated Green Tick
    pulse_factor = 1.0 + 0.10 * math.sin(f * (2 * math.pi / 16))
    r = int(42 * pulse_factor)
    cx, cy = w // 2, 150

    # Glow wave
    if f < 9:
        wave_r = int(46 + f * 4)
        d.ellipse([cx - wave_r, cy - wave_r, cx + wave_r, cy + wave_r], outline="#bbf7d0", width=2)

    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#1e8e3e")
    draw_check(d, cx, cy, r, "#ffffff", int(6 * pulse_factor))

    d.text((w//2 - 50, 220), "Rs. 250.00", fill="#202124")
    d.text((w//2 - 70, 260), "Paid to Campus Cafe", fill="#3c4043")

    d.line([30, 295, w - 30, 295], fill="#e8eaed", width=1)
    d.text((40, 320), "UPI transaction ID", fill="#5f6368")
    d.text((40, 345), "432901928471", fill="#202124")

    d.text((40, 390), "Date & Time", fill="#5f6368")
    d.text((40, 412), "21 Nov 2026, 02:46 AM", fill="#202124")
    d.text((40, 450), "Paid via State Bank of India", fill="#5f6368")

    gpay_frames.append(im)

gpay_gif_path = os.path.join(samples_dir, "real_gpay_tick_blink.gif")
gpay_frames[0].save(gpay_gif_path, save_all=True, append_images=gpay_frames[1:], duration=80, loop=0)
print(f"Generated {gpay_gif_path}")

real_gp_path = os.path.join(samples_dir, "real_gpay_sample.png")
gpay_frames[3].save(real_gp_path)
print(f"Generated {real_gp_path}")

# 4. GENERATE FAKE SPOOF APP SAMPLE (Static, dead tick, bad font/colors)
im_fake = Image.new("RGB", (w, h), color="#f3e8ff")
d_fake = ImageDraw.Draw(im_fake)
# Wrong shade of purple
d_fake.rectangle([0, 0, w, 65], fill="#7e22ce")
d_fake.text((w//2 - 40, 25), "FakePay UPI", fill="#ffffff")

# Static dead circle (flat green, no glow, thin misaligned check)
cx, cy = w // 2, 150
d_fake.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill="#22c55e")
draw_check(d_fake, cx, cy, 32, "#ffffff", 3)

d_fake.text((w//2 - 70, 220), "Payment Done!", fill="#000000")
d_fake.text((w//2 - 55, 260), "Rs. 500", fill="#000000")

# Missing NPCI format, spoofed layout
d_fake.rectangle([25, 310, w - 25, 480], fill="#ffffff", outline="#d8b4fe", width=1)
d_fake.text((40, 330), "Trans ID: FP998877", fill="#6b21a8")
d_fake.text((40, 370), "Time: Just now", fill="#6b21a8")
d_fake.text((40, 410), "Status: Success (Spoofed)", fill="#6b21a8")

fake_spoof_path = os.path.join(samples_dir, "fake_spoof_sample.png")
im_fake.save(fake_spoof_path)
print(f"Generated {fake_spoof_path}")

# 5. GENERATE FAKE EDITED AMOUNT SAMPLE (Spliced font)
im_edit = Image.new("RGB", (w, h), color="#ffffff")
d_edit = ImageDraw.Draw(im_edit)
d_edit.rectangle([0, 0, w, 65], fill="#1a73e8")
d_edit.text((w//2 - 45, 25), "Google Pay", fill="#ffffff")

# Normal tick
d_edit.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill="#1e8e3e")
draw_check(d_edit, cx, cy, 38, "#ffffff", 6)

# Edited amount with rectangular noisy patch around it (Photoshop artifact simulation)
d_edit.rectangle([w//2 - 90, 205, w//2 + 90, 255], fill="#e2e8f0", outline="#94a3b8", width=1)
d_edit.text((w//2 - 65, 220), "Rs. 2,500.00", fill="#ef4444")

d_edit.text((w//2 - 70, 270), "Paid to Campus Cafe", fill="#3c4043")
d_edit.line([30, 305, w - 30, 305], fill="#e8eaed", width=1)
d_edit.text((40, 330), "UPI transaction ID", fill="#5f6368")
d_edit.text((40, 355), "432901928471", fill="#202124")

fake_edit_path = os.path.join(samples_dir, "fake_edited_sample.png")
im_edit.save(fake_edit_path)
print(f"Generated {fake_edit_path}")

print("All sample assets generated successfully!")
