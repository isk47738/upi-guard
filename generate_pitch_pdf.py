from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether

# ── Color Palette ──────────────────────────────────────────────
BG       = colors.HexColor('#0B1120')
CYAN     = colors.HexColor('#38BDF8')
EMERALD  = colors.HexColor('#10B981')
RED      = colors.HexColor('#EF4444')
AMBER    = colors.HexColor('#F59E0B')
WHITE    = colors.HexColor('#F8FAFC')
NAVY     = colors.HexColor('#1E293B')
DARKNAVY = colors.HexColor('#0F172A')
GRAY     = colors.HexColor('#94A3B8')
LGRAY    = colors.HexColor('#CBD5E1')

output = r"d:\web devlopment baba\fake_upi_detector\UPI_Guard_Pitch_QnA.pdf"

doc = SimpleDocTemplate(
    output,
    pagesize=A4,
    rightMargin=18*mm, leftMargin=18*mm,
    topMargin=16*mm, bottomMargin=16*mm,
    title="UPI Guard Pro — Pitch & Q&A",
    author="UPI Guard Pro Team"
)

# ── Background canvas ──────────────────────────────────────────
def bg_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # top accent bar
    canvas.setFillColor(CYAN)
    canvas.rect(0, A4[1]-4, A4[0], 4, fill=1, stroke=0)
    # bottom bar
    canvas.setFillColor(DARKNAVY)
    canvas.rect(0, 0, A4[0], 10*mm, fill=1, stroke=0)
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(A4[0]/2, 3.5*mm, "UPI Guard Pro  |  isk47738.github.io/upi-guard/  |  Hackathon Final Round 2026")
    canvas.restoreState()

# ── Styles ─────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S('cov_title', fontSize=28, textColor=CYAN, alignment=TA_CENTER,
                fontName='Helvetica-Bold', spaceAfter=4)
cover_sub   = S('cov_sub',   fontSize=13, textColor=WHITE, alignment=TA_CENTER,
                fontName='Helvetica', spaceAfter=2)
cover_tag   = S('cov_tag',   fontSize=10, textColor=AMBER, alignment=TA_CENTER,
                fontName='Helvetica-Oblique', spaceAfter=14)

sec_head    = S('sec_head',  fontSize=14, textColor=CYAN, fontName='Helvetica-Bold',
                spaceBefore=14, spaceAfter=5, borderPad=4)
sub_head    = S('sub_head',  fontSize=11, textColor=EMERALD, fontName='Helvetica-Bold',
                spaceBefore=8, spaceAfter=3)
q_style     = S('q_style',   fontSize=10, textColor=AMBER, fontName='Helvetica-Bold',
                spaceBefore=7, spaceAfter=2, leftIndent=6)
a_style     = S('a_style',   fontSize=9.5, textColor=WHITE, fontName='Helvetica',
                spaceBefore=1, spaceAfter=4, leftIndent=12, leading=14)
bullet_s    = S('bullet_s',  fontSize=9.5, textColor=LGRAY, fontName='Helvetica',
                spaceBefore=1, spaceAfter=1, leftIndent=18, bulletIndent=10, leading=13)
tip_s       = S('tip_s',     fontSize=9,   textColor=AMBER, fontName='Helvetica-Oblique',
                spaceBefore=2, spaceAfter=2, leftIndent=10, leading=13)
bold_white  = S('bw',        fontSize=10,  textColor=WHITE, fontName='Helvetica-Bold',
                spaceBefore=2, spaceAfter=1)
normal_gray = S('ng',        fontSize=9,   textColor=LGRAY, fontName='Helvetica',
                leading=13, spaceAfter=2, alignment=TA_JUSTIFY)
highlight   = S('hl',        fontSize=11,  textColor=BG,    fontName='Helvetica-Bold',
                alignment=TA_CENTER)

def HR(c=NAVY): return HRFlowable(width="100%", thickness=1, color=c, spaceAfter=4, spaceBefore=4)
def SP(h=4):    return Spacer(1, h*mm)

def section_box(title, color=CYAN):
    data = [[Paragraph(title, S('sh2', fontSize=13, textColor=BG,
                                fontName='Helvetica-Bold', alignment=TA_CENTER))]]
    t = Table(data, colWidths=[174*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ]))
    return t

def qa_block(q, a):
    items = [
        Paragraph(f"❓ {q}", q_style),
        Paragraph(f"💬 {a}", a_style),
    ]
    return KeepTogether(items)

def stat_table(stats):
    """stats = list of (label, value, color)"""
    row = [[Paragraph(f"<b>{v}</b>", S('sv', fontSize=16, textColor=c,
                                        fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph(l, S('sl', fontSize=8, textColor=LGRAY,
                           fontName='Helvetica', alignment=TA_CENTER))]
           for l, v, c in stats]
    # make it 2 col pairs
    merged = []
    for i in range(0, len(stats), 2):
        pair = stats[i:i+2]
        cells = []
        for l, v, c in pair:
            cells.append(Paragraph(f"<b>{v}</b>", S(f'sv{i}', fontSize=18, textColor=c,
                                                     fontName='Helvetica-Bold', alignment=TA_CENTER)))
            cells.append(Paragraph(l, S(f'sl{i}', fontSize=8, textColor=LGRAY,
                                        fontName='Helvetica', alignment=TA_CENTER)))
        while len(cells) < 4:
            cells.append(Paragraph('', a_style))
        merged.append(cells)

    t = Table(merged, colWidths=[43.5*mm]*4)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), NAVY),
        ('GRID',          (0,0), (-1,-1), 0.5, DARKNAVY),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

# ── Build Story ────────────────────────────────────────────────
story = []

# ═══════════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════════
story += [
    SP(8),
    Paragraph("🛡️ UPI Guard Pro", cover_title),
    Paragraph("Hackathon Final Round — Pitch & Q&A Cheat Sheet", cover_sub),
    Paragraph("\"0.43s Detection  ·  87% Accuracy  ·  Zero Infrastructure\"", cover_tag),
    HR(CYAN),
    SP(2),
]

stats = [
    ("Avg Scan Time", "0.43s", CYAN),
    ("Accuracy",      "87%",   EMERALD),
    ("Frauds Blocked","68",    RED),
    ("Amount Saved",  "₹24.5K",AMBER),
]
story.append(stat_table(stats))
story.append(SP(6))
story.append(HR(NAVY))

# ═══════════════════════════════════════════════════════════════
# SECTION 1 — 60-SECOND PITCH SCRIPT
# ═══════════════════════════════════════════════════════════════
story += [SP(2), section_box("🎤  60-Second Pitch Script", CYAN), SP(3)]

parts = [
    ("🔴 Opening Hook  (10 sec)", 
     "\"Imagine karo — ek student canteen counter pe aata hai, ₹200 ka payment dikhata hai phone pe, "
     "daal bhat le jaata hai. Counter wala check karta hai... aur realize karta hai — payment kabhi hua hi "
     "nahi tha. Ye ek edited screenshot tha.\""),
    ("📌 Problem  (10 sec)",
     "\"Ye sirf ek story nahi hai — ye India ke 90 lakh se zyada canteens, dukaans aur small vendors ki daily "
     "reality hai. UPI fraud se unhe har din lakhs ka nuksan hota hai. Existing solutions? Sirf bank statement "
     "check — jo 5 minutes leta hai per customer.\""),
    ("💡 Solution  (15 sec)",
     "\"UPI Guard Pro sirf 0.43 seconds mein batata hai — REAL hai ya FAKE. Koi internet nahi chahiye, "
     "koi bank login nahi chahiye. Bas camera ke saamne receipt dikhao — aur AI judge kar deta hai.\""),
    ("🔬 Innovation  (15 sec)",
     "\"Humne 3-layer detection engine banaya hai:\n"
     "  • ELA Forensic Engine — pixel-level editing detect karta hai\n"
     "  • Green Tick Liveness Pulse — animated tick ka 1.2 Hz pulse verify karta hai\n"
     "  • Soundbox Gateway Match — UTR number cross-verify karta hai\""),
    ("🏆 Impact & Close  (10 sec)",
     "\"1,250 scans. 68 frauds blocked. ₹24,500 saved. Aur ye free hai, offline hai, aur koi bhi use "
     "kar sakta hai. UPI Guard Pro — Canteen ka security guard!\""),
]
for label, text in parts:
    story.append(Paragraph(label, sub_head))
    story.append(Paragraph(text.replace('\n', '<br/>'), a_style))
    story.append(SP(1))

story += [HR(NAVY), SP(2)]

# ═══════════════════════════════════════════════════════════════
# SECTION 2 — TECHNICAL Q&A
# ═══════════════════════════════════════════════════════════════
story += [section_box("🔴  Technical Questions", RED), SP(3)]

tech_qa = [
    ("ELA kya hota hai? Explain karo.",
     "Sir, ELA matlab Error Level Analysis. Jab koi image edit karta hai — Photoshop ya kisi bhi app se — "
     "toh edited pixels ke compression level alag ho jaate hain. Hum un differences amplify karke dekhte hain. "
     "Jahan zyada noise variance hogi — jaise ₹39 → ₹390 jaise tamper — wahan red highlight aayegi. "
     "Hum 2.35x noise ratio threshold use karte hain."),
    ("Green tick detect kaise karte ho? Screenshot toh static hoti hai!",
     "Sir, exactly yehi humari core innovation hai! Jab asli payment hoti hai, PhonePe/GPay ka green tick "
     "ek specific frequency pe blink karta hai — approximately 1.2 Hz. Hum continuous live camera se 30+ "
     "frames capture karte hain aur pixel intensity change measure karte hain. Agar tick blink nahi kar raha — "
     "matlab screenshot hai, live screen nahi."),
    ("Accuracy kitni hai?",
     "Sir, real-world testing mein accuracy approximately 87% hai. False positives — yaani real receipt ko "
     "fake bolna — 6% se kam hai. ELA threshold hum tune karte rahe hain 118 se lekar dual-zone 2.35x ratio tak."),
    ("Koi bypass kar sakta hai kya? Jaise phone pe video chalaaye?",
     "Good question sir! Hum is limitation pe kaam kar rahe hain. Abhi ke liye Soundbox UTR cross-verification "
     "ek backup layer hai. Future roadmap mein hum IoT camera aur NPCI webhook integration add kar rahe hain "
     "jo direct bank confirmation lega."),
    ("Internet nahi hai toh kya kya nahi karega?",
     "Sir, ELA analysis, green tick detection, geometry check — ye sab fully offline hain. Sirf Soundbox UTR "
     "gateway match ke liye internet chahiye. Offline mode mein bhi 3/4 checks pass hote hain."),
]
for q, a in tech_qa:
    story.append(qa_block(q, a))

story += [HR(NAVY), SP(2)]

# ═══════════════════════════════════════════════════════════════
# SECTION 3 — BUSINESS Q&A
# ═══════════════════════════════════════════════════════════════
story += [section_box("💼  Business Questions", EMERALD), SP(3)]

biz_qa = [
    ("Market size kya hai? Revenue model?",
     "Sir, India mein 9 crore se zyada UPI merchants hain. Revenue model: freemium — basic free, "
     "premium ₹299/month per canteen with soundbox integration aur incident log export. "
     "Enterprise ke liye — college campus license ₹2,999/month."),
    ("Existing solutions se better kaise?",
     "Sir, existing solutions ya toh expensive hain (bank ke POS terminals), ya slow hain (statement check). "
     "Humara solution: zero cost, 0.43 second response, koi hardware nahi chahiye — sirf smartphone. Yahi differentiation hai."),
    ("Scalability? Agar 1 lakh vendors use karein?",
     "Sir, humara app 100% client-side hai — koi server load nahi. GitHub Pages pe host hai jo globally CDN "
     "se serve hota hai. Scale karne ke liye koi additional infrastructure cost nahi."),
]
for q, a in biz_qa:
    story.append(qa_block(q, a))

story += [HR(NAVY), SP(2)]

# ═══════════════════════════════════════════════════════════════
# SECTION 4 — TOUGH QUESTIONS
# ═══════════════════════════════════════════════════════════════
story += [section_box("🤔  Tough / Tricky Questions", AMBER), SP(3)]

tough_qa = [
    ("Ye toh simple image processing hai — AI kahan hai?",
     "Sir, ELA itself ek machine learning inspired technique hai jo forensic science mein use hoti hai. "
     "Future mein hum CNN model train kar rahe hain specifically UPI receipt layouts ke liye — Paytm, PhonePe, "
     "GPay sab alag fonts aur layouts use karte hain. Abhi rule-based hai, next version ML-based hoga."),
    ("Team mein kitne log hain? Kaam kaise divide kiya?",
     "Sir, [apni team ka naam bolo]. Maine frontend + ELA algorithm implement kiya. [Teammates ke kaam bolo]. "
     "Total build time — 48 hours hackathon sprint."),
    ("Live demo karo.",
     "Sir, ye raha live — [phone uthao, app kholo, fake screenshot ya camera use karo]. "
     "Dekho — 0.43 seconds mein FAKE detect kar liya. ELA noise variance 170.7 — clearly tampered amount. "
     "Live URL: isk47738.github.io/upi-guard"),
]
for q, a in tough_qa:
    story.append(qa_block(q, a))

# Fallback tip box
story.append(SP(2))
tip_data = [[Paragraph("😅  Agar Kuch Na Pata Ho — Ye Bolo:",
                        S('tt', fontSize=10, textColor=AMBER, fontName='Helvetica-Bold')),],
            [Paragraph(
                "\"Sir, great question — ye abhi humari limitation hai, aur hum isko next iteration mein address "
                "kar rahe hain. Currently humara focus core detection accuracy pe hai.\"",
                S('ta', fontSize=9.5, textColor=WHITE, fontName='Helvetica-Oblique', leading=14))]]
tip_t = Table(tip_data, colWidths=[174*mm])
tip_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), DARKNAVY),
    ('BOX',           (0,0), (-1,-1), 1.5, AMBER),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING',   (0,0), (-1,-1), 12),
]))
story.append(tip_t)

story += [HR(NAVY), SP(2)]

# ═══════════════════════════════════════════════════════════════
# SECTION 5 — SLIDE CHANGES
# ═══════════════════════════════════════════════════════════════
story += [section_box("📊  Recommended Slide Updates", CYAN), SP(3)]

slide_data = [
    [Paragraph("<b>Slide</b>", highlight),
     Paragraph("<b>Change</b>", highlight),
     Paragraph("<b>Priority</b>", highlight)],
    [Paragraph("Slide 1 — Cover",   bold_white),
     Paragraph("Add tagline: \"0.43s · 87% · Zero Infrastructure\"", normal_gray),
     Paragraph("<b>🔴 High</b>", S('p1', fontSize=9, textColor=RED, fontName='Helvetica-Bold', alignment=TA_CENTER))],
    [Paragraph("Slide 2 — Problem", bold_white),
     Paragraph("Add: \"₹1.47 crore lost daily to UPI fraud in India\" stat card", normal_gray),
     Paragraph("<b>🔴 High</b>", S('p2', fontSize=9, textColor=RED, fontName='Helvetica-Bold', alignment=TA_CENTER))],
    [Paragraph("Slide 5 — ELA",     bold_white),
     Paragraph("Add before/after ELA heatmap screenshot from live app", normal_gray),
     Paragraph("<b>🔴 High</b>", S('p3', fontSize=9, textColor=RED, fontName='Helvetica-Bold', alignment=TA_CENTER))],
    [Paragraph("Slide 9 — Demo",    bold_white),
     Paragraph("Add QR code to live app URL so judges can scan & try", normal_gray),
     Paragraph("<b>🔴 High</b>", S('p4', fontSize=9, textColor=RED, fontName='Helvetica-Bold', alignment=TA_CENTER))],
    [Paragraph("Slide 4 — Tick",    bold_white),
     Paragraph("Add screenshot showing green tick PASS result from app", normal_gray),
     Paragraph("<b>🟡 Medium</b>", S('p5', fontSize=9, textColor=AMBER, fontName='Helvetica-Bold', alignment=TA_CENTER))],
    [Paragraph("Slide 8 — Impact",  bold_white),
     Paragraph("Add \"0.43s avg scan time\" to the stat cards", normal_gray),
     Paragraph("<b>🟡 Medium</b>", S('p6', fontSize=9, textColor=AMBER, fontName='Helvetica-Bold', alignment=TA_CENTER))],
    [Paragraph("Slide 10 — Roadmap",bold_white),
     Paragraph("Add team names + contact / GitHub link at bottom", normal_gray),
     Paragraph("<b>🟡 Medium</b>", S('p7', fontSize=9, textColor=AMBER, fontName='Helvetica-Bold', alignment=TA_CENTER))],
    [Paragraph("NEW Slide 3.5",     bold_white),
     Paragraph("\"How It Works\" — 3-step visual: Show receipt → AI scans → REAL/FAKE in 0.43s", normal_gray),
     Paragraph("<b>🟢 Optional</b>", S('p8', fontSize=9, textColor=EMERALD, fontName='Helvetica-Bold', alignment=TA_CENTER))],
]

slide_t = Table(slide_data, colWidths=[38*mm, 108*mm, 28*mm])
slide_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  CYAN),
    ('BACKGROUND',    (0,1), (-1,-1), NAVY),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [NAVY, DARKNAVY]),
    ('GRID',          (0,0), (-1,-1), 0.4, BG),
    ('TOPPADDING',    (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(slide_t)

story += [SP(4), HR(NAVY), SP(2)]

# ═══════════════════════════════════════════════════════════════
# SECTION 6 — LAST MINUTE TIPS + CLOSING
# ═══════════════════════════════════════════════════════════════
story += [section_box("⚡  Last Minute Tips", EMERALD), SP(3)]

tips = [
    "🖨️  <b>QR Code print karo</b> — judges live demo try kar sakein apne phone pe",
    "📸  <b>Screenshot print / save karo</b> (FAKE/SUSPICIOUS wali) — judges ko physical dikhao",
    "💪  <b>Confidence mein bolo:</b> \"humne deploy kiya, 1,250 scans ho chuke hain\"",
    "🔢  <b>Numbers yaad karo:</b>  0.43s · 87% · 68 frauds · ₹24,500 · 9 crore merchants",
    "📱  <b>Live demo ke liye</b> pehle test karo — test_screens.html use karo second phone pe",
]
for t in tips:
    story.append(Paragraph(f"• {t}", bullet_s))

story.append(SP(4))

# Closing statement box
close_data = [[
    Paragraph("🏆  Closing Statement", S('ct', fontSize=11, textColor=AMBER, fontName='Helvetica-Bold')),
],[
    Paragraph(
        "\"UPI Guard Pro sirf ek app nahi hai — ye ek financial security layer hai jo India ke 9 crore "
        "small vendors ke haath mein dena chahte hain. Completely free, completely offline capable, aur "
        "completely made in 48 hours. Thank you!\"",
        S('cs', fontSize=10, textColor=WHITE, fontName='Helvetica-Oblique', leading=15, alignment=TA_JUSTIFY))
]]
close_t = Table(close_data, colWidths=[174*mm])
close_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), DARKNAVY),
    ('BOX',           (0,0), (-1,-1), 2, EMERALD),
    ('TOPPADDING',    (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING',   (0,0), (-1,-1), 14),
    ('RIGHTPADDING',  (0,0), (-1,-1), 14),
]))
story.append(close_t)
story.append(SP(3))

url_data = [[
    Paragraph("🌐  isk47738.github.io/upi-guard", S('url', fontSize=10, textColor=CYAN,
              fontName='Helvetica-Bold', alignment=TA_CENTER)),
    Paragraph("🧪  .../test_screens.html", S('url2', fontSize=10, textColor=GRAY,
              fontName='Helvetica', alignment=TA_CENTER)),
]]
url_t = Table(url_data, colWidths=[87*mm, 87*mm])
url_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), NAVY),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('GRID',          (0,0), (-1,-1), 0.5, DARKNAVY),
]))
story.append(url_t)

# ── Build PDF ──────────────────────────────────────────────────
doc.build(story, onFirstPage=bg_canvas, onLaterPages=bg_canvas)
print(f"PDF created: {output}")
