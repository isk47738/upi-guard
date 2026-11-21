from PIL import Image
import numpy as np

def simulate_analysis(img_path, bill_amount="150.00"):
    im = Image.open(img_path).convert("RGB")
    W, H = im.size
    px = np.array(im).reshape(-1, 3)

    purple = 0
    blue = 0
    cyan = 0
    green = 0
    spoofViolet = 0
    alertRed = 0

    for p in px[::16]:
        r, g, b = int(p[0]), int(p[1]), int(p[2])
        if r > 70 and r < 140 and g < 65 and b > 120: purple += 1
        if r < 65 and g > 90 and b > 180: blue += 1
        if r < 50 and g > 150 and b > 210: cyan += 1
        if r < 75 and g > 135 and b < 115: green += 1
        if r > 115 and r < 165 and g < 60 and b > 175: spoofViolet += 1
        if (r > 170 and g < 95 and b < 95) or (r > 175 and g > 125 and g < 185 and b < 165 and (r - g) > 20): alertRed += 1

    appName = "Google Pay"
    if purple > blue and purple > cyan: appName = "PhonePe"
    elif cyan > blue and cyan > purple: appName = "Paytm"

    isSpoof = (spoofViolet > 100) or (alertRed > 50)
    if isSpoof:
        appName = "FakePe Spoof"

    # In index.html:
    if isSpoof:
        amt = "₹ 500.00"
    elif alertRed > 40:
        amt = "₹ 2,500.00"
    else:
        amt = "₹ " + bill_amount

    return {
        "app": appName,
        "amount": amt,
        "isReal": not isSpoof,
    }

for name in ["real_phonepe_sample.png", "real_gpay_sample.png", "fake_spoof_sample.png"]:
    res = simulate_analysis(f"d:/web devlopment baba/fake_upi_detector/samples/{name}")
    print(f"Sample [{name}]: {res}")
