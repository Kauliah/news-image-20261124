#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news broadsheet, 1024x1024 PNG.

Six verified stories, each self-contained: headline + one short line that
says who did what, where, and why it matters. No copied artwork; every
pictogram is drawn here from PIL primitives.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
NAVY = (27, 42, 74)
PANEL = (255, 255, 255)
BORDER = (216, 210, 192)
INK = (28, 30, 38)
SUB = (74, 78, 88)
FOOT = (110, 108, 96)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw `text` centred on cx with letter tracking."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wch + tracking


# ---- header ----------------------------------------------------------------
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((W // 2, 16), "24 NOVEMBER 2026", font=font(BOLD, 64),
       fill=(255, 255, 255), anchor="ma")
spaced(d, W // 2, 92, "TUESDAY  ·  THE WORLD IN ONE IMAGE",
       font(BOLD, 19), (185, 196, 216))

# ---- pictograms -------------------------------------------------------------
def icon_scales(x, y, s, col):
    # scales of justice: post, beam, two pans
    d.line([(x + s // 2, y + 2), (x + s // 2, y + s - 8)], fill=col, width=4)
    d.line([(x + 4, y + 10), (x + s - 4, y + 10)], fill=col, width=4)
    d.polygon([(x + 2, y + 12), (x + 16, y + 12), (x + 9, y + 26)], fill=col)
    d.polygon([(x + s - 16, y + 12), (x + s - 2, y + 12), (x + s - 9, y + 26)],
              fill=col)
    d.line([(x + 8, y + s - 4), (x + s - 8, y + s - 4)], fill=col, width=4)


def icon_burst(x, y, s, col):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
    pts = []
    for i in range(16):
        ang = i * 3.14159 / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * __import__("math").cos(ang),
                    cy + rr * __import__("math").sin(ang)))
    d.polygon(pts, fill=col)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255))


def icon_flame(x, y, s, col):
    cx = x + s // 2
    d.polygon([(cx, y + 2), (cx + s // 2 - 4, y + s // 2),
               (cx + s // 4, y + s - 4), (cx - s // 4, y + s - 4),
               (cx - s // 2 + 4, y + s // 2)], fill=col)
    d.ellipse([cx - 8, y + s // 2 + 8, cx + 8, y + s // 2 + 24],
              fill=(255, 196, 66))


def icon_chart(x, y, s, col):
    pts = [(x + 2, y + s - 8), (x + s // 3, y + s // 2),
           (x + s // 2 + 2, y + s // 2 - 6), (x + s - 8, y + 6)]
    d.line(pts, fill=col, width=5, joint="curve")
    d.polygon([(x + s - 10, y + 2), (x + s - 2, y + 2), (x + s - 2, y + 10)],
              fill=col)
    d.line([(x + 2, y + s - 4), (x + s - 2, y + s - 4)], fill=col, width=3)


def icon_globe(x, y, s, col):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=col, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=col, width=3)
    d.polygon([(cx - 2, cy - r // 2), (cx + 8, cy - r // 4),
               (cx + 2, cy + 2), (cx - 8, cy - 2)], fill=col)


def icon_medal(x, y, s, col):
    cx, cy, r = x + s // 2, y + s // 2 + 2, s // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4],
              outline=(255, 255, 255), width=3)
    d.text((cx, cy - 2), "3", font=font(BOLD, 26), fill=(255, 255, 255),
           anchor="mm")


ICONS = {
    "scales": icon_scales,
    "burst": icon_burst,
    "flame": icon_flame,
    "chart": icon_chart,
    "globe": icon_globe,
    "medal": icon_medal,
}

# ---- stories ----------------------------------------------------------------
STORIES = [
    dict(tag="TECH  ·  LAW  —  USA / CHINA", color=(139, 30, 45),
         icon="scales",
         head="HUAWEI FOUND GUILTY ON 10 COUNTS",
         sub="A Brooklyn jury convicts the Chinese telecom giant of bank "
             "fraud, sanctions violations and stealing US trade secrets."),
    dict(tag="MIDDLE EAST  ·  GAZA", color=(179, 84, 30),
         icon="burst",
         head="ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
         sub="Naeem Abu Nahel, 50, head of Hamas's internal security "
             "service, is killed in Gaza City; six others die in strikes "
             "across Gaza."),
    dict(tag="ASIA  ·  DISASTER", color=(168, 50, 30),
         icon="flame",
         head="INDONESIA FACTORY FIRE TOLL RISES TO 26",
         sub="Officials confirm 26 workers dead in the candy-plant blaze "
             "at Cikande, Banten; eight are still missing after "
             "Saturday's fire."),
    dict(tag="USA  ·  ECONOMY", color=(30, 107, 74),
         icon="chart",
         head="US CONSUMER CONFIDENCE JUMPS TO 103.3",
         sub="The Conference Board index rises from 91.9 in October to "
             "its highest in nearly two years as gas prices fall."),
    dict(tag="PACIFIC  ·  DIPLOMACY", color=(20, 85, 122),
         icon="globe",
         head="SOLOMONS TO END CHINA SECURITY PACT",
         sub="Honiara tells Beijing it will let the 2022 security deal "
             "lapse in April and plans a new treaty with Australia "
             "instead."),
    dict(tag="ASIA  ·  POWER", color=(91, 58, 142),
         icon="medal",
         head="INDIA NOW ASIA'S No. 3 POWER",
         sub="The Lowy Institute's 2026 Asia Power Index puts India "
             "third, ahead of Japan and Russia, behind the US and China."),
]

# ---- grid --------------------------------------------------------------------
GX, GY = 18, 132
GW, GH = 487, 264
GUT = 14
for i, st in enumerate(STORIES):
    px = GX + (i % 2) * (GW + GUT)
    py = GY + (i // 2) * (GH + GUT)
    col = st["color"]
    d.rectangle([px, py, px + GW, py + GH], fill=PANEL, outline=BORDER, width=1)
    d.rectangle([px, py, px + GW, py + 7], fill=col)
    ICONS[st["icon"]](px + 18, py + 20, 44, col)
    d.text((px + 74, py + 30), st["tag"], font=font(BOLD, 17), fill=col)
    # headline
    lines = wrap(d, st["head"], font(BOLD, 30), GW - 36)
    y = py + 76
    for ln in lines:
        d.text((px + 18, y), ln, font=font(BOLD, 30), fill=INK)
        y += 36
    # sub-line
    slines = wrap(d, st["sub"], font(REG, 19), GW - 36)
    y += 6
    for ln in slines:
        d.text((px + 18, y), ln, font=font(REG, 19), fill=SUB)
        y += 26

# ---- footer ------------------------------------------------------------------
d.text((W // 2, 1006),
       "Every story above happened or was first reported on 24 November 2026.",
       font=font(REG, 17), fill=FOOT, anchor="mb")

img.save("entry.png", optimize=True)
print("saved entry.png")
