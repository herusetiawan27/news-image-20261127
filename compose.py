#!/usr/bin/env python3
"""Compose the 27 November 2026 'THE WORLD TODAY' front page (1024x1024 PNG).

Six stories, all first reported on Friday 27 November 2026:
  LEAD  Kuwait drone strike kills two Italian technicians; Iran denies (Reuters/BBC)
  2     EU leaders deadlocked on budget + $49bn Ukraine loan (AP)
  3     Thanksgiving storm batters US coasts (AP/Reuters)
  4     NZ ruling coalition falls one seat short of majority (Reuters)
  5     Japan eyes $353bn five-year defence plan (Reuters)
  6     Markets steady; Tokyo core inflation at 16-month high (Reuters)
Exactly three editorial illustrations, each tagged ILLUSTRATION.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 42, 33)
GREY = (90, 90, 90)
RULE = (30, 30, 30)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, font):
    return d.textlength(s, font=font)

def center(s, y, font, fill=INK):
    d.text(((W - text_w(s, font)) / 2, y), s, font=font, fill=fill)

def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines

def para(x, y, s, font, width, lh, fill=INK):
    for ln in wrap(s, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def headline(x, y, s, font, width, lh):
    return para(x, y, s, font, width, lh)

def illus_tag(x, y):
    f = F(SANS_B, 13)
    label = "ILLUSTRATION"
    tw = text_w(label, f) + 12
    d.rectangle([x, y, x + tw, y + 20], fill=(20, 20, 20))
    d.text((x + 6, y + 3), label, font=f, fill=(255, 255, 255))

# ---------- frame ----------
d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=3)
d.rectangle([22, 22, W - 22, H - 22], outline=RULE, width=1)

# ---------- masthead ----------
center("THE WORLD TODAY", 34, F(SERIF_B, 64))
d.line([40, 122, W - 40, 122], fill=RULE, width=3)
center("FRIDAY 27 NOVEMBER 2026", 132, F(SANS_B, 27), fill=RED)
d.text((44, 138), "GLOBAL EDITION", font=F(SANS_B, 15), fill=GREY)
r = "ONE DAY • SIX STORIES"
d.text((W - 44 - text_w(r, F(SANS_B, 15)), 138), r, font=F(SANS_B, 15), fill=GREY)
d.line([40, 172, W - 40, 172], fill=RULE, width=1)

# ---------- lead story ----------
LX, LY = 44, 188
d.text((LX, LY), "MIDDLE EAST  •  LEAD STORY", font=F(SANS_B, 16), fill=RED)
hy = headline(LX, LY + 26, "TWO ITALIANS KILLED IN KUWAIT DRONE STRIKE — IRAN DENIES INVOLVEMENT",
              F(SERIF_B, 35), 936, 44)
lead_body = ("Two technicians for Rheinmetall, the German defence group, died when drones struck an "
             "air-defence surveillance site in Kuwait, Italy's foreign minister told the Senate in Rome. "
             "Kuwait's defence ministry called it an Iranian attack and said four people were first "
             "wounded by falling debris. Tehran denied any involvement — the second reported Iranian "
             "attack on the US-allied Gulf state this month.")
by = para(LX, hy + 10, lead_body, F(SERIF, 19), 560, 27)

# lead illustration: night sky, Kuwait-style towers, drone
IX, IY, IW, IH = 628, hy + 6, 352, 236
for i in range(IH):
    t = i / IH
    col = (int(16 + 30 * t), int(22 + 38 * t), int(48 + 60 * t))
    d.line([IX, IY + i, IX + IW, IY + i], fill=col)
# searchlight beams
d.polygon([(IX + 40, IY + IH), (IX + 150, IY + 40), (IX + 185, IY + 46), (IX + 90, IY + IH)], fill=(70, 80, 105))
# towers (two tapered Kuwait-tower silhouettes with spheres)
for cx, th in [(IX + 235, 150), (IX + 295, 118)]:
    d.polygon([(cx - 13, IY + IH), (cx - 4, IY + IH - th), (cx + 4, IY + IH - th), (cx + 13, IY + IH)], fill=(8, 10, 18))
    d.ellipse([cx - 17, IY + IH - th - 6, cx + 17, IY + IH - th + 28], fill=(10, 13, 24))
    d.ellipse([cx - 11, IY + IH - th - 52, cx + 11, IY + IH - th - 30], fill=(10, 13, 24))
# city blocks
for bx in range(IX + 6, IX + 200, 26):
    bh = 26 + (bx * 7) % 40
    d.rectangle([bx, IY + IH - bh, bx + 20, IY + IH], fill=(10, 12, 22))
    for wy in range(IY + IH - bh + 6, IY + IH - 6, 11):
        d.point((bx + 6, wy), fill=(240, 200, 90)); d.point((bx + 13, wy), fill=(240, 200, 90))
# drone silhouette + red light
dx, dy = IX + 96, IY + 52
d.line([dx - 34, dy - 14, dx + 34, dy + 14], fill=(230, 230, 230), width=3)
d.line([dx - 34, dy + 14, dx + 34, dy - 14], fill=(230, 230, 230), width=3)
d.ellipse([dx - 13, dy - 8, dx + 13, dy + 8], fill=(235, 235, 235))
for ex, ey in [(dx - 34, dy - 14), (dx + 34, dy + 14), (dx - 34, dy + 14), (dx + 34, dy - 14)]:
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], outline=(235, 235, 235), width=2)
d.ellipse([dx - 4, dy + 10, dx + 4, dy + 18], fill=(255, 60, 40))
d.rectangle([IX, IY, IX + IW, IY + IH], outline=RULE, width=2)
illus_tag(IX + 8, IY + IH - 28)
lead_end = max(by, IY + IH + 8)

# ---------- middle row: three text stories ----------
MY = lead_end + 14
d.line([40, MY - 8, W - 40, MY - 8], fill=RULE, width=2)
cols = [
    ("EUROPE",
     "EU DEADLOCKED ON BUDGET AND UKRAINE LOAN",
     "After 12+ hours of talks in Brussels, leaders failed to agree the 2028–34 budget "
     "or a $49bn loan for Ukraine. Macron set an end-of-year deadline. (AP)"),
    ("NEW ZEALAND",
     "RULING COALITION FALLS ONE SEAT SHORT",
     "Final results gave PM Christopher Luxon's coalition 65 of 130 seats — one short "
     "of a majority — leaving him reliant on the centrist Opportunity Party. (Reuters)"),
    ("JAPAN",
     "TOKYO EYES $353 BILLION FIVE-YEAR DEFENCE PLAN",
     "Tokyo is considering ¥56.3 trillion ($353bn) of defence spending over five years "
     "from fiscal 2027 — a record plan, but below the military's request. (Reuters)"),
]
cw, gap = 296, 24
mid_end = MY
for i, (kick, head, body) in enumerate(cols):
    x = 44 + i * (cw + gap)
    d.text((x, MY), kick, font=F(SANS_B, 15), fill=RED)
    yy = headline(x, MY + 24, head, F(SANS_B, 20), cw, 25)
    end = para(x, yy + 6, body, F(SANS, 15), cw, 21)
    mid_end = max(mid_end, end)
    if i:
        d.line([x - gap // 2, MY, x - gap // 2, MY + 210], fill=(160, 150, 130), width=1)
MID_END = mid_end + 6

# ---------- bottom row: storm + markets ----------
BY = MID_END + 12
d.line([40, BY - 6, W - 40, BY - 6], fill=RULE, width=2)
PW = 458
# storm panel: kicker + headline full width, then illustration + body
d.text((44, BY), "UNITED STATES  •  WEATHER", font=F(SANS_B, 15), fill=RED)
hy2 = headline(44, BY + 24, "THANKSGIVING STORM BATTERS US COASTS", F(SANS_B, 20), PW, 25)
ROW = hy2 + 8
# storm illustration: sea, rain, lightning
SX, SY, SW, SH = 44, ROW, 170, 118
for i in range(SH):
    t = i / SH
    col = (int(28 + 22 * t), int(48 + 30 * t), int(74 + 40 * t))
    d.line([SX, SY + i, SX + SW, SY + i], fill=col)
for rx in range(SX + 8, SX + SW - 6, 17):  # rain
    d.line([rx, SY + 12, rx - 7, SY + 34], fill=(190, 210, 225), width=2)
d.polygon([(SX + 128, SY + 16), (SX + 104, SY + 62), (SX + 122, SY + 62), (SX + 96, SY + 112),
           (SX + 138, SY + 52), (SX + 120, SY + 52), (SX + 146, SY + 16)], fill=(250, 205, 60))
for k in range(3):  # waves
    wy = SY + SH - 34 + k * 12
    for wx in range(SX + 4, SX + SW - 26, 30):
        d.arc([wx, wy, wx + 30, wy + 16], 180, 360, fill=(225, 238, 245), width=3)
d.rectangle([SX, SY, SX + SW, SY + SH], outline=RULE, width=2)
illus_tag(SX + 8, SY + SH - 28)
tx = SX + SW + 16
para(tx, ROW,
     "A coastal storm flooded East Coast towns, brought 70 mph gusts and left 900,000+ "
     "customers without power. 400+ flights cancelled; Macy's parade postponed — a "
     "first in 100 years. (AP / Reuters)",
     F(SANS, 15), PW - SW - 16, 19)

# markets panel: kicker + headline full width, then illustration + body
GX = 44 + PW + 28
d.text((GX, BY), "MARKETS  •  ASIA", font=F(SANS_B, 15), fill=RED)
hy3 = headline(GX, BY + 24, "SHARES STEADY AS TOKYO INFLATION HITS 16-MONTH HIGH", F(SANS_B, 20), PW, 25)
ROW2 = hy3 + 8
MX, MY2, MW, MH = GX, ROW2, 170, 118
d.rectangle([MX, MY2, MX + MW, MY2 + MH], fill=(238, 232, 214))
bars = [(16, 30), (48, 44), (80, 40), (112, 62), (146, 80)]
for bx, bh in bars:
    d.rectangle([MX + bx - 11, MY2 + MH - 14 - bh, MX + bx + 11, MY2 + MH - 14], fill=(46, 96, 60))
d.line([MX + 10, MY2 + MH - 48, MX + 56, MY2 + MH - 62, MX + 92, MY2 + MH - 58, MX + 152, MY2 + MH - 92],
       fill=RED, width=4)
d.polygon([(MX + 152, MY2 + MH - 92), (MX + 134, MY2 + MH - 90), (MX + 146, MY2 + MH - 76)], fill=RED)
d.ellipse([MX + 116, MY2 + 8, MX + 146, MY2 + 38], outline=INK, width=2)
d.text((MX + 124, MY2 + 12), "¥", font=F(SANS_B, 19), fill=INK)
d.ellipse([MX + 20, MY2 + 8, MX + 50, MY2 + 38], outline=INK, width=2)
d.text((MX + 29, MY2 + 12), "$", font=F(SANS_B, 19), fill=INK)
d.rectangle([MX, MY2, MX + MW, MY2 + MH], outline=RULE, width=2)
illus_tag(MX + 8, MY2 + MH - 28)
tx2 = GX + MW + 16
para(tx2, ROW2,
     "Asian shares steadied after a bruising month; the dollar rose for a third month. "
     "Tokyo core inflation hit 2.9%, a 16-month high, fuelling Bank of Japan hike "
     "bets. (Reuters)",
     F(SANS, 15), PW - MW - 16, 19)

# ---------- footer ----------
d.line([40, H - 36, W - 40, H - 36], fill=RULE, width=2)
center("Sources: Reuters • Associated Press • BBC — every story reported on Friday 27 November 2026",
       H - 27, F(SANS, 12), fill=GREY)

img.save("/home/hatch/workspace/makefun/news-image-20261127/entry.png")
print("saved")
