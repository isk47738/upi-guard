import os
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
)
from reportlab.pdfgen import canvas

# Dimensions for 16:9 Widescreen Presentation (13.33 x 7.5 inches)
PAGE_WIDTH = 13.33 * 72   # 960 pt
PAGE_HEIGHT = 7.5 * 72    # 540 pt
PAGESIZE = (PAGE_WIDTH, PAGE_HEIGHT)

MEDIA_DIR = r"C:\Users\isk47\.gemini\antigravity\brain\7d1cbc54-9eda-429c-b0d8-4a102b134657\scratch\pptx_media"
OUTPUT_PDF = r"d:\web devlopment baba\fake_upi_detector\UPI_Guard_Final_Presentation.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations()
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self):
        self.saveState()
        # Dark Navy Background
        self.setFillColor(colors.HexColor("#0B1120"))
        self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

        # Top Accent Cyan Border
        self.setFillColor(colors.HexColor("#38BDF8"))
        self.rect(0, PAGE_HEIGHT - 4, PAGE_WIDTH, 4, fill=1, stroke=0)

        # Bottom Subtle Grid Line
        self.setStrokeColor(colors.HexColor("#1E293B"))
        self.setLineWidth(1)
        self.line(40, 35, PAGE_WIDTH - 40, 35)

        # Footer Left
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#38BDF8"))
        self.drawString(45, 20, "UPI GUARD PRO")
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(135, 20, "•  Hackathon Final Round Presentation  •  Team Infinity")

        # Footer Right
        self.setFont("Helvetica", 8.5)
        self.drawRightString(PAGE_WIDTH - 45, 20, f"Slide {self._pageNumber} of 8")
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=PAGESIZE,
        leftMargin=40,
        rightMargin=40,
        topMargin=25,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    style_slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#F8FAFC')
    )

    style_slide_subtitle = ParagraphStyle(
        'SlideSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#94A3B8')
    )

    style_card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#38BDF8')
    )

    style_card_body = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#E2E8F0')
    )

    style_card_bullet = ParagraphStyle(
        'CardBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#CBD5E1')
    )

    def slide_header(title, subtitle, slide_num):
        header_table = Table([
            [
                Paragraph(f"<b>{title}</b>", style_slide_title),
                Paragraph(f"<font color='#38bdf8'><b>{slide_num}</b></font>", ParagraphStyle('Pill', fontName='Helvetica-Bold', fontSize=14, alignment=2, textColor=colors.HexColor('#38BDF8')))
            ],
            [
                Paragraph(subtitle, style_slide_subtitle),
                ""
            ]
        ], colWidths=[PAGE_WIDTH - 150, 70])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return header_table

    story = []

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    shield_img = os.path.join(MEDIA_DIR, "image1.png")
    
    badge_p = Paragraph("<font color='#38bdf8'><b>HACKATHON FINAL ROUND PRESENTATION</b></font>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#38BDF8')))
    title_p = Paragraph("<b>UPI Guard Pro</b>", ParagraphStyle('T1', fontName='Helvetica-Bold', fontSize=34, leading=38, textColor=colors.HexColor('#FFFFFF')))
    tag_p = Paragraph("<font color='#38bdf8'><b>Real-Time Fake UPI Payment Screenshot Detector & Anti-Fraud Shield</b></font>", ParagraphStyle('Tag1', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#38BDF8')))
    desc_p = Paragraph("Sub-3-second client-side forensic pixel analysis, live animated checkmark liveness verification, and anti-replay screenshot vault built for campus canteens and small merchants.", ParagraphStyle('D1', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor('#94A3B8')))
    link_p = Paragraph("<b>Live PWA Demo:</b> <font color='#38bdf8'><u>https://isk47738.github.io/upi-guard</u></font>   |   <b>Team:</b> Infinity", ParagraphStyle('L1', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#E2E8F0')))

    left_cell = [badge_p, Spacer(1, 8), title_p, Spacer(1, 4), tag_p, Spacer(1, 10), desc_p, Spacer(1, 14), link_p]
    right_cell = [RLImage(shield_img, width=110, height=120)] if os.path.exists(shield_img) else []

    s1_table = Table([[left_cell, right_cell]], colWidths=[PAGE_WIDTH - 240, 160])
    s1_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    # 4 Metric Cards
    metrics = [
        ("<font color='#34d399'><b>< 0.5s – 3s</b></font>", "Verdict Speed on<br/>Mid-Range Android"),
        ("<font color='#38bdf8'><b>5-Layer</b></font>", "Custom Forensic Pixel<br/>& Layout Engine"),
        ("<font color='#a855f7'><b>3+ Apps</b></font>", "PhonePe, Google Pay<br/>& Paytm Supported"),
        ("<font color='#fbbf24'><b>100% Offline</b></font>", "Zero-Dependency PWA<br/>+ Local Vault")
    ]
    card_data = []
    card_w = (PAGE_WIDTH - 80 - 36) / 4
    for val, label in metrics:
        p_val = Paragraph(f"<font size=16>{val}</font>", ParagraphStyle('MV', fontName='Helvetica-Bold', alignment=1))
        p_lbl = Paragraph(f"<font size=9 color='#94A3B8'>{label}</font>", ParagraphStyle('ML', fontName='Helvetica', alignment=1, leading=12))
        card_data.append([p_val, Spacer(1, 4), p_lbl])

    metrics_table = Table([card_data], colWidths=[card_w]*4)
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    story.append(Spacer(1, 20))
    story.append(s1_table)
    story.append(Spacer(1, 25))
    story.append(metrics_table)

    # =========================================================================
    # SLIDE 2: THE PROBLEM & WHY GENERIC AI GETS STUCK
    # =========================================================================
    story.append(NumberedCanvas.page_break if hasattr(NumberedCanvas, 'page_break') else Spacer(1, 0)) # We'll handle via doc
    # Instead of page_break, let's use SimpleDocTemplate pageBreak
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    story.append(slide_header("The Problem & Why Generic AI Gets Stuck", "High-rush campus counters face a 3-second trust vulnerability", "02"))
    story.append(Spacer(1, 14))

    box1_txt = """<b>The Merchant Pain Point</b><br/>
• <b>Campus canteens & small shops</b> rely on visual UPI confirmation during peak rush.<br/>
• <b>Fraudsters flash edited screenshots</b> or fake 'Payment Successful' clone apps.<br/>
• <b>Cashiers have under 3 seconds</b> to judge authenticity before handing over goods.<br/>
• <b>Direct revenue loss</b> goes unnoticed until end-of-day bank reconciliation."""

    box2_txt = """<b>Why Generic Vision AI Alone Fails</b><br/>
• <b>Generic image models lack exact UI ground-truth</b> specs for PhonePe, GPay & Paytm.<br/>
• <b>Edited digits still look semantically like valid numbers</b> to standard OCR/LLMs.<br/>
• <b>Cloud-based AI models add network latency (>3s)</b> and fail in poor canteen Wi-Fi.<br/>
• <b>Cannot distinguish a live animated receipt</b> from a static forged screenshot."""

    box3_txt = """<b>Our Core Insight: Reference-Grounded Forensics + Liveness + Anti-Replay</b><br/>
• <b>App-Specific Blueprints:</b> Hardcoded structural templates checking official brand headers, logo geometry, font styles, font sizes, and layout proportions.<br/>
• <b>Pixel-Level Tamper Detection:</b> Error Level Analysis (ELA) & JPEG block compression noise catch spliced digits invisible to the naked eye.<br/>
• <b>Real-Time Liveness & Replay Lock:</b> Detects live checkmark blink/pulse (1.2 Hz) and blocks duplicate scans by saving & fingerprinting prior receipts."""

    col_w2 = (PAGE_WIDTH - 80 - 15) / 2
    row1_table = Table([
        [Paragraph(box1_txt, style_card_body), Paragraph(box2_txt, style_card_body)]
    ], colWidths=[col_w2, col_w2])
    row1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    row2_table = Table([
        [Paragraph(box3_txt, style_card_body)]
    ], colWidths=[PAGE_WIDTH - 80])
    row2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#38BDF8')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    story.append(row1_table)
    story.append(Spacer(1, 14))
    story.append(row2_table)

    # =========================================================================
    # SLIDE 3: SOLUTION: UPI GUARD PRO
    # =========================================================================
    story.append(PageBreak())
    story.append(slide_header("Solution: UPI Guard Pro", "Autonomous Anti-Fraud Terminal & Canteen Soundbox PWA", "03"))
    story.append(Spacer(1, 14))

    col1_txt = """<b>1. Dual Scan Modes</b><br/>
• <b>Continuous Live Scanner:</b> Auto-locks receipt frames at 15 FPS via phone camera.<br/>
• <b>Photo / Gallery Upload:</b> Instant forensic audit on uploaded screenshots.<br/>
• <b>Sub-3s Verdict:</b> Delivers clear REAL or FAKE / SUSPICIOUS verdict in ~0.45s–2.5s.<br/>
• <b>Actionable Reasons:</b> Explains exact failure points (ELA spike, dead tick, reused ID)."""

    col2_txt = """<b>2. Live Liveness & UI Checks</b><br/>
• <b>Checkmark Blink Detection:</b> Verifies real-time green tick pulse/animation vs static spoof.<br/>
• <b>Brand & Logo Verification:</b> Matches PhonePe purple, GPay blue/green, Paytm cyan headers.<br/>
• <b>Typography & Layout Audit:</b> Checks font family, font size hierarchy, and UI alignment.<br/>
• <b>Transaction ID (UTR) Format:</b> Validates exact alphanumeric length & digit structure."""

    col3_txt = """<b>3. Anti-Replay Save Vault</b><br/>
• <b>Zero Double-Scanning:</b> Every scanned screenshot is saved into a protected local vault.<br/>
• <b>Instant Duplicate Alert:</b> Re-scanning the same image triggers 'Already Scanned' warning.<br/>
• <b>UTR Hash Ledger:</b> Logs transaction IDs & image hashes in SQLite / local storage.<br/>
• <b>Smart Soundbox 4G Feed:</b> Audio announcements in Hindi, English & Hinglish + CSV export."""

    col_w3 = (PAGE_WIDTH - 80 - 24) / 3
    s3_table = Table([
        [Paragraph(col1_txt, style_card_body), Paragraph(col2_txt, style_card_body), Paragraph(col3_txt, style_card_body)]
    ], colWidths=[col_w3, col_w3, col_w3])
    s3_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(s3_table)

    # =========================================================================
    # SLIDE 4: INSIDE THE 5-LAYER FORENSIC ENGINE
    # =========================================================================
    story.append(PageBreak())
    story.append(slide_header("Inside the 5-Layer Forensic Engine", "Deterministic pixel, layout, and cryptographic checks running locally", "04"))
    story.append(Spacer(1, 14))

    table_data = [
        [
            Paragraph("<b>Forensic Layer</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#38BDF8'))),
            Paragraph("<b>What It Inspects</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#38BDF8'))),
            Paragraph("<b>Fraud Attack Caught</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#38BDF8'))),
            Paragraph("<b>Speed / Method</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#38BDF8')))
        ],
        [
            Paragraph("<b>1. Aspect Ratio & Layout</b>", style_card_body),
            Paragraph("Mobile screen proportions, app header color, logo placement, font style & size", style_card_bullet),
            Paragraph("Cropped web mockups, misaligned fake generator templates", style_card_bullet),
            Paragraph("<b>< 20 ms</b><br/><font color='#94a3b8'>Canvas Geometry</font>", style_card_body)
        ],
        [
            Paragraph("<b>2. Dual-Zone ELA Pixel Scan</b>", style_card_body),
            Paragraph("Error Level Analysis comparing Amount Box vs Reference Card edge variance", style_card_bullet),
            Paragraph("Digitally pasted/edited ₹ amount text with higher compression disparity", style_card_bullet),
            Paragraph("<b>~180 ms</b><br/><font color='#94a3b8'>Pixel Matrix Diff</font>", style_card_body)
        ],
        [
            Paragraph("<b>3. Compression Noise</b>", style_card_body),
            Paragraph("8x8 block-level JPEG artifact consistency across receipt background", style_card_bullet),
            Paragraph("Local re-saving artifacts around forged merchant name or time", style_card_bullet),
            Paragraph("<b>~120 ms</b><br/><font color='#94a3b8'>DCT Block Audit</font>", style_card_body)
        ],
        [
            Paragraph("<b>4. Color Profile & Liveness</b>", style_card_body),
            Paragraph("Background white ratio mismatch + real-time green tick blink/pulse (1.2 Hz)", style_card_bullet),
            Paragraph("Colored brush overlays hiding old text & static fake screenshots", style_card_bullet),
            Paragraph("<b>~90 ms</b><br/><font color='#94a3b8'>Histogram + FPS</font>", style_card_body)
        ],
        [
            Paragraph("<b>5. UTR & Anti-Replay Vault</b>", style_card_body),
            Paragraph("UTR digit/letter count validation + saved image vault & UTR hash lookup", style_card_bullet),
            Paragraph("Invalid ID formats, old screenshots shown twice ('Already Scanned')", style_card_bullet),
            Paragraph("<b>< 15 ms</b><br/><font color='#94a3b8'>SQLite / Vault Hash</font>", style_card_body)
        ]
    ]

    t_widths = [160, 290, 270, 160]
    layer_table = Table(table_data, colWidths=t_widths)
    layer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#131D33')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(layer_table)

    # =========================================================================
    # SLIDE 5: HOW IT WORKS: 3-SECOND COUNTER WORKFLOW
    # =========================================================================
    story.append(PageBreak())
    story.append(slide_header("How It Works: 3-Second Counter Workflow", "From camera snap to forensic verdict & anti-replay vault storage", "05"))
    story.append(Spacer(1, 14))

    step_w = (PAGE_WIDTH - 80 - 36) / 4
    steps = [
        ("STEP 1: CAPTURE", "Live Camera or Upload", "Staff points phone at customer's screen (15 FPS auto-lock) or uploads screenshot."),
        ("STEP 2: VAULT CHECK", "Anti-Replay Lookup", "System checks saved folder & image hash. If scanned earlier, immediately flags 'Already Scanned!'"),
        ("STEP 3: FORENSICS", "5-Layer + Liveness Scan", "Inspects logo, font style/size, UTR digit/letter pattern, ELA heatmap & tick blink."),
        ("STEP 4: VERDICT", "Real / Fake + Soundbox", "Displays verdict in <3s with exact reasons, logs evidence & triggers audio confirmation.")
    ]

    step_cells = []
    for s_title, s_sub, s_desc in steps:
        p_t = Paragraph(f"<font color='#38bdf8'><b>{s_title}</b></font>", ParagraphStyle('ST', fontName='Helvetica-Bold', fontSize=11, leading=14))
        p_s = Paragraph(f"<b>{s_sub}</b>", ParagraphStyle('SS', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor('#FFFFFF')))
        p_d = Paragraph(s_desc, ParagraphStyle('SD', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#CBD5E1')))
        step_cells.append([p_t, Spacer(1, 4), p_s, Spacer(1, 6), p_d])

    s5_top_table = Table([step_cells], colWidths=[step_w]*4)
    s5_top_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    highlights_txt = """<b>Key Technical Highlights Built for Real-World Canteen Fraud</b><br/>
• <b>Saved Folder & Anti-Replay Protection:</b> Every scanned image is archived automatically; attempting to scan the same screenshot twice triggers an immediate duplicate warning so students cannot pass one receipt around.<br/>
• <b>Fine-Grained UI & ID Validation:</b> Verifies app-specific logos, font styles, font sizes, layout geometry, and exact Transaction ID (UTR) alphanumeric character/digit counts alongside live checkmark blink detection."""

    s5_bot_table = Table([[Paragraph(highlights_txt, style_card_body)]], colWidths=[PAGE_WIDTH - 80])
    s5_bot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#38BDF8')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    story.append(s5_top_table)
    story.append(Spacer(1, 14))
    story.append(s5_bot_table)

    # =========================================================================
    # SLIDE 6: SUPPORTED UPI APPS & LIGHTWEIGHT ARCHITECTURE
    # =========================================================================
    story.append(PageBreak())
    story.append(slide_header("Supported UPI Apps & Lightweight Architecture", "Zero-dependency Progressive Web App engineered for mid-range Android devices", "06"))
    story.append(Spacer(1, 14))

    s6_box1 = """<b>Supported UPI App Profiles (3+)</b><br/>
• <b>PhonePe:</b> Purple header signature, animated tick pulse, 12-digit UTR format.<br/>
• <b>Google Pay (GPay):</b> Blue/white header geometry, green verification badge, UPI Ref ID.<br/>
• <b>Paytm:</b> Cyan/blue brand header, specific typography scale & layout grid.<br/>
• <b>Extensible JSON/Canvas rule profiles</b> allow rapid addition of BHIM, Amazon Pay, etc."""

    s6_box2 = """<b>Zero-Bloat Tech Stack</b><br/>
• <b>Frontend:</b> Pure HTML5, CSS3 & Vanilla JS (zero heavy frameworks for instant load).<br/>
• <b>Forensic Engine:</b> HTML5 Canvas API, pixel ELA matrix & RGB color histograms.<br/>
• <b>Backend & Vault:</b> Python stdlib HTTP server + SQLite UTR & saved screenshot store.<br/>
• <b>Offline PWA:</b> Service Worker + Web App Manifest ('Add to Home Screen' install)."""

    s6_box3 = """<b>Hackathon Requirement Checklist — 100% Met & Exceeded</b><br/>
• <b>Layout, Font & Pixel Checks:</b> Detects logo mismatches, font style/size anomalies, and ELA pixel tampering.<br/>
• <b>Timestamp & Reused IDs:</b> Validates timestamp freshness (<5 min), UTR alphanumeric length, and blocks duplicate images.<br/>
• <b>3+ UPI Apps & <3s Speed:</b> Supports PhonePe, GPay & Paytm with sub-second (~0.45s) execution on mid-range phones.<br/>
• <b>Judge-Ready Demo Suite:</b> Built-in 1-Click Judge Scenarios (Real Blinking Tick, Dead Tick Spoof, Edited Amount, Reused UTR)."""

    s6_row1 = Table([
        [Paragraph(s6_box1, style_card_body), Paragraph(s6_box2, style_card_body)]
    ], colWidths=[col_w2, col_w2])
    s6_row1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    s6_row2 = Table([[Paragraph(s6_box3, style_card_body)]], colWidths=[PAGE_WIDTH - 80])
    s6_row2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#38BDF8')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    story.append(s6_row1)
    story.append(Spacer(1, 14))
    story.append(s6_row2)

    # =========================================================================
    # SLIDE 7: MERCHANT IMPACT
    # =========================================================================
    story.append(PageBreak())
    story.append(slide_header("Merchant Impact", "Ready for immediate deployment at campus canteens and local retail counters", "07"))
    story.append(Spacer(1, 14))

    s7_box1 = """<b>Live Judge Demonstration Flow</b><br/>
• <b>Scenario A — Genuine Receipt:</b> Live camera locks onto PhonePe/GPay screen, detects 1.2 Hz green tick blink -> REAL PAYMENT (0.45s).<br/>
• <b>Scenario B — Edited Amount:</b> Upload tampered receipt -> ELA Heatmap highlights blazing red splice around digits -> FAKE / SUSPICIOUS.<br/>
• <b>Scenario C — Static Spoof App:</b> Camera scans non-blinking fake screen -> Dead Tick & layout mismatch flagged.<br/>
• <b>Scenario D — Replay Attack:</b> Re-scan a previously saved screenshot -> Instant 'Already Scanned' duplicate alert."""

    s7_box2 = """<b>Real-World Impact & Future Roadmap</b><br/>
• <b>Zero Hardware Cost:</b> Runs on any shopkeeper's existing Android/iOS browser as an installable PWA.<br/>
• <b>Admin Audit Trail:</b> Exports fraud logs (CSV) with UTR hashes & ELA disparity evidence for campus authorities.<br/>
• <b>Multilingual Soundbox:</b> Speaks payment confirmations in Hindi, English & Hinglish.<br/>
• <b>Next Steps:</b> Direct NPCI/bank webhook integration & automated on-device OCR extraction."""

    s7_table = Table([
        [Paragraph(s7_box1, style_card_body), Paragraph(s7_box2, style_card_body)]
    ], colWidths=[col_w2, col_w2])
    s7_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(s7_table)

    # =========================================================================
    # SLIDE 8: LIVE DEMO (GALLERY COMPARISON)
    # =========================================================================
    story.append(PageBreak())
    story.append(slide_header("Live Demo", "Ready for immediate deployment at campus canteens and local retail counters", "08"))
    story.append(Spacer(1, 10))

    img2_path = os.path.join(MEDIA_DIR, "image2.png")
    img3_path = os.path.join(MEDIA_DIR, "image3.png")
    img4_path = os.path.join(MEDIA_DIR, "image4.png")
    img5_path = os.path.join(MEDIA_DIR, "image5.png")

    # Header bar for Fake vs Genuine
    sub_headers = Table([
        [
            Paragraph("<font color='#f87171'><b>🚨 Fake Payment</b></font>", ParagraphStyle('HFake', fontName='Helvetica-Bold', fontSize=11, alignment=1)),
            Paragraph("<font color='#34d399'><b>✅ Genuine Payment</b></font>", ParagraphStyle('HReal', fontName='Helvetica-Bold', fontSize=11, alignment=1))
        ]
    ], colWidths=[col_w2, col_w2])
    sub_headers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#2a1215')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#0d281e')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(sub_headers)
    story.append(Spacer(1, 8))

    # 4 images side by side
    img_h = 240
    pic2 = RLImage(img2_path, width=130, height=img_h) if os.path.exists(img2_path) else Paragraph("Fake Screen", style_card_body)
    pic3 = RLImage(img3_path, width=130, height=img_h) if os.path.exists(img3_path) else Paragraph("Spoof Result", style_card_body)
    pic4 = RLImage(img4_path, width=130, height=img_h) if os.path.exists(img4_path) else Paragraph("Real Screen", style_card_body)
    pic5 = RLImage(img5_path, width=130, height=img_h) if os.path.exists(img5_path) else Paragraph("Real Result", style_card_body)

    col_img_w = (PAGE_WIDTH - 80) / 4
    img_table = Table([
        [pic2, pic3, pic4, pic5]
    ], colWidths=[col_img_w]*4)
    img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(img_table)
    story.append(Spacer(1, 8))

    thanks_txt = "<b>Thank You!</b> &nbsp;|&nbsp; <b>Try UPI Guard Pro Live:</b> <font color='#38bdf8'><u>https://isk47738.github.io/upi-guard</u></font>"
    thanks_table = Table([[Paragraph(thanks_txt, ParagraphStyle('Thx', fontName='Helvetica', fontSize=11, alignment=1, textColor=colors.HexColor('#FFFFFF')))]], colWidths=[PAGE_WIDTH - 80])
    thanks_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#131D33')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#38BDF8')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(thanks_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")

if __name__ == "__main__":
    build_pdf()
