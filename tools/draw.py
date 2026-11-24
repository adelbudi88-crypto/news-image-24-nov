#!/usr/bin/env python3
"""Draw the 24 November 2026 front-page poster (1024x1024 PNG).

A newspaper-style one-image summary of the day's world news: a navy
masthead names Tuesday 24 November 2026, a hero panel covers the COP31
collapse in Antalya, six panels cover the other top stories, and a
"MORE TODAY" strip adds three more. Ten stories in total, every one
checked against live reporting on 24 November 2026 before drawing.

VERIFIED FACTS (checked live 24 Nov 2026, ~12:30 WIB):
- HERO COP31: UN climate talks in Antalya ended Sunday 22 Nov with
  NO agreement -- the first COP to close without a deal since
  Copenhagen 2009. The final draft left out fossil fuels; the EU and
  Pacific island states refused it. Pacific islands went home with no
  new finance deal (PINA 24 Nov; Oceanographic Magazine; Hindu
  BusinessLine 23 Nov; Tonga Independent).
- PANEL 1 US-IRAN: Washington is preparing for a possible
  weeks-long campaign against Iran and has ordered a second aircraft
  carrier to the Gulf; Trump warned Iran faces "very traumatic"
  consequences if no nuclear deal is reached (Reuters via Sea and
  Job; Access24, 23 Nov). No casualty figures are claimed anywhere.
- PANEL 2 ZAPORIZHZHIA: A Russian attack killed 2 people and
  wounded 22, including 2 children, in Zaporizhzhia overnight
  (Reuters, 24 Nov, citing Ivan Fedorov, Zaporizhzhia Regional
  Defense Council, via Telegram; Reuters notes it could not
  independently confirm the report).
- PANEL 3 WAR DEAD: Independent Russian outlets Meduza and
  Mediazona, studying leaked Rosstat death records, estimate more
  than 700,000 Russian soldiers have died since Feb 2022 -- about
  490,000 deaths registered, the rest missing and presumed dead
  (published 23 Nov; reported by Kyiv Independent, NY Post,
  Nexus Europa). The figure is an estimate, labelled as such.
- PANEL 4 MERKURY + REFINERY: Ukrainian naval drones sank the
  Russian corvette Merkury at Benghazi, Libya, on 22 Nov (7 naval
  drones; a Ka-27 helicopter aboard destroyed; cargo ship MV Angara
  also hit). Ukrainian drones struck the Novoshakhtinsk refinery in
  Rostov region overnight 23 Nov; fires followed and the plant halted
  operations (Reuters / h.ua / Operbaza chronicle).
- PANEL 5 INDONESIA: Fire at the PT Fonusa Agung Mulia candy
  factory (Milkita) in Cikande, Serang, Banten, on Sat 21 Nov:
  at least 3 workers confirmed dead and 34 still missing in the
  latest AP report (23 Nov); 24 body bags recovered, DNA testing
  needed to identify victims; about 300 workers were on site.
- PANEL 6 EU SANCTIONS: The European Commission proposed its 22nd
  sanctions package on Russia on Mon 23 Nov: about 60 more banks cut
  from SWIFT, 70+ shadow-fleet ships listed, Russian teams barred
  from competing under the Russian flag at EU sports events, visa
  ban for ex-combatants (Reuters 23 Nov; European Commission
  statement). A proposal, not yet adopted.
- STRIP 1 MEXICO: Mexico will try "El Chapo Isidro" (Fausto Isidro
  Meza Flores) at home despite a US extradition request, Attorney
  General Ernestina Godoy said Mon 23 Nov (Reuters). He was captured
  20 Nov in Guasave, Sinaloa; the US says he faces six charges.
- STRIP 2 FIFA: FIFA's Extraordinary Congress on Mon 23 Nov
  appointed the USA, Mexico, Costa Rica and Jamaica as hosts of the
  2031 Women's World Cup (first 48-team edition) and England,
  Northern Ireland, Scotland and Wales for 2035 (FIFA; Reuters).
- STRIP 3 KOREA: South Korea scrambled fighter jets on Tue 24 Nov
  after several Russian military aircraft entered its air defence
  identification zone near Ulleung island; a shelter alert was
  lifted after 3 minutes. No airspace violation, Seoul said
  (Reuters, 24 Nov).

DROPPED AFTER VERIFICATION (do NOT appear on the poster):
- "Himalaya floods, 4 dead, ~100 missing" -- the only matches are
  the August 2025 Dharali (Uttarakhand) flood, recycled by
  aggregators. Not a 24 Nov 2026 story.
- "Bangladesh typhoid drive for 50 million children" -- that
  campaign launched 12 Oct 2025; the 24 Nov aggregator listing
  re-dates a 2025 story.
- "SoftBank $2bn Intel investment" -- the deal was signed in
  August 2025 ($23/share); the 24 Nov listing recycles it.
- ECB / Lagarde succession -- real, but announced 29 Oct 2026
  (she leaves 7 Feb 2027); not a 24 Nov development, so it was
  cut to keep the page fresh.
- The Democrats' 258-seat claim and the Nvidia/Huang story --
  conflicting sources, not used, per the brief.

Everything is flat vector-style geometry drawn with Pillow. The
script is fully deterministic: no randomness, no clock, no network,
fixed fonts, fixed palette, fixed layout -- re-running it always
writes the same bytes.

Run:  python3 tools/draw.py
Out:  entry.png in the repo root (one level up from tools/).
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 22
CONTENT_W = W - 2 * MARGIN

# --- palette: newsprint paper, navy ink, brick red, gold, teal --------
PAPER = (247, 242, 231)
CARD = (255, 253, 246)
INK = (20, 33, 61)
INK_SOFT = (48, 58, 82)
BRICK = (179, 64, 42)
BRICK_DARK = (146, 48, 30)
GOLD = (198, 152, 58)
GOLD_DARK = (168, 124, 38)
GOLD_PALE = (232, 205, 140)
TEAL = (31, 94, 98)
TEAL_DARK = (18, 66, 70)
TEAL_PALE = (186, 214, 208)
MUTED = (96, 90, 78)
BORDER = (214, 204, 188)
NAVY_PANEL = (24, 40, 74)
SKY = (214, 226, 238)
SKY_DARK = (178, 198, 220)
SEA = (38, 84, 124)
FIRE = (214, 96, 44)
SMOKE = (120, 118, 112)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
REG = f"{FONT_DIR}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw stacked lines; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag_chip(draw, x, y, text, fill=BRICK):
    """Small coloured tag chip; returns the chip width."""
    fnt = font(BOLD, 13)
    tw = draw.textlength(text, font=fnt)
    pad_x, pad_y = 8, 4
    w = int(tw + 2 * pad_x)
    h = 23
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=fill)
    draw.text((x + pad_x, y + pad_y + 1), text, font=fnt, fill=CARD)
    return w


def rule(draw, x0, y, x1, color=BORDER, width=1):
    draw.line([x0, y, x1, y], fill=color, width=width)


# ------------------------------------------------------------------ art
# Each art_* draws a flat illustration inside the box (x0, y0, x1, y1).
# Nothing here reads files or the network; every shape is fixed.

def art_cop31(draw, x0, y0, x1, y1):
    """A Pacific island under a harsh sun, sea rising, talks stalled."""
    draw.rectangle([x0, y0, x1, y1], fill=TEAL_DARK)
    # Sun, low and hard, top-right.
    cx, cy = x1 - 56, y0 + 48
    draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=GOLD)
    for k in range(8):
        ang = k * math.pi / 4
        sx, sy = cx + 40 * math.cos(ang), cy + 40 * math.sin(ang)
        ex, ey = cx + 52 * math.cos(ang), cy + 52 * math.sin(ang)
        draw.line([sx, sy, ex, ey], fill=GOLD, width=4)
    # Sea bands.
    for i, col in enumerate((TEAL, (36, 110, 112), (44, 126, 126))):
        yy = y0 + 108 + i * 16
        draw.rectangle([x0, yy, x1, yy + 16], fill=col)
    # Island: sand bar + two palms, bottom-left of the art box.
    draw.ellipse([x0 + 8, y1 - 44, x0 + 150, y1 - 6], fill=(224, 198, 138))
    draw.line([x0 + 52, y1 - 40, x0 + 46, y1 - 92], fill=(90, 60, 30), width=6)
    draw.line([x0 + 84, y1 - 40, x0 + 92, y1 - 88], fill=(90, 60, 30), width=6)
    for tx, ty in ((x0 + 46, y1 - 92), (x0 + 92, y1 - 88)):
        draw.arc([tx - 26, ty - 18, tx + 26, ty + 10], 200, 340,
                 fill=(52, 128, 74), width=5)
        draw.arc([tx - 22, ty - 6, tx + 22, ty + 18], 180, 20,
                 fill=(52, 128, 74), width=5)
    # Cracked-earth wedge: the deal that never closed.
    draw.polygon([(x1 - 118, y1 - 6), (x1 - 30, y1 - 6),
                  (x1 - 74, y1 - 58)], fill=(196, 164, 110))
    draw.line([x1 - 74, y1 - 58, x1 - 74, y1 - 20], fill=(120, 84, 50), width=3)
    draw.line([x1 - 74, y1 - 34, x1 - 52, y1 - 22], fill=(120, 84, 50), width=2)
    draw.line([x1 - 74, y1 - 34, x1 - 96, y1 - 24], fill=(120, 84, 50), width=2)
    # "NO DEAL" stamp, bottom-right over the sea.
    stamp = font(BOLD, 21)
    draw.rectangle([x1 - 132, y0 + 118, x1 - 14, y0 + 150], fill=BRICK)
    draw.text((x1 - 124, y0 + 123), "NO DEAL", font=stamp, fill=CARD)


def art_carrier(draw, x0, y0, x1, y1):
    """Aircraft carrier deck at dusk, two jets, second ship behind."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 214, 188))
    draw.rectangle([x0, y0, x1, y0 + 44], fill=(240, 178, 110))
    draw.ellipse([x1 - 34, y0 + 8, x1 - 6, y0 + 36], fill=(250, 220, 150))
    # Sea (two wave lines only -- the 92px band has no room for more).
    draw.rectangle([x0, y0 + 44, x1, y1], fill=SEA)
    for yy in (y0 + 62, y0 + 78):
        draw.line([x0 + 10, yy, x1 - 10, yy], fill=(90, 140, 175), width=2)
    # Carrier hull + deck.
    draw.polygon([(x0 + 8, y1 - 34), (x1 - 8, y1 - 34), (x1 - 26, y1 - 12),
                  (x0 + 26, y1 - 12)], fill=INK)
    draw.rectangle([x0 + 8, y1 - 52, x1 - 8, y1 - 34], fill=(58, 70, 96))
    # Island tower.
    draw.rectangle([x1 - 62, y1 - 84, x1 - 34, y1 - 52], fill=CARD)
    draw.rectangle([x1 - 58, y1 - 80, x1 - 38, y1 - 70], fill=INK)
    # Two jets on deck, seen from above.
    for jx in (x0 + 26, x0 + 96):
        draw.polygon([(jx, y1 - 62), (jx + 34, y1 - 54), (jx + 34, y1 - 48),
                      (jx, y1 - 50)], fill=GOLD_PALE)
        draw.polygon([(jx + 12, y1 - 66), (jx + 22, y1 - 54),
                      (jx + 18, y1 - 46)], fill=GOLD_PALE)
    # Second carrier on the horizon, small.
    draw.rectangle([x0 + 14, y0 + 52, x0 + 74, y0 + 60], fill=INK_SOFT)
    draw.rectangle([x0 + 52, y0 + 44, x0 + 60, y0 + 52], fill=INK_SOFT)


def art_zaporizhzhia(draw, x0, y0, x1, y1):
    """Damaged apartment block at night, rescue light, smoke."""
    draw.rectangle([x0, y0, x1, y1], fill=(32, 40, 66))
    # Stars / sparks.
    for sx, sy in ((x0 + 16, y0 + 12), (x0 + 96, y0 + 8), (x0 + 150, y0 + 20),
                   (x0 + 60, y0 + 26), (x0 + 130, y0 + 34)):
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=GOLD_PALE)
    # Building, left.
    draw.rectangle([x0 + 10, y0 + 30, x0 + 96, y1 - 10], fill=(58, 66, 96))
    draw.rectangle([x0 + 10, y0 + 30, x0 + 96, y0 + 40], fill=(44, 50, 76))
    for r in range(2):
        for c in range(3):
            wx, wy = x0 + 22 + c * 26, y0 + 50 + r * 26
            col = GOLD if (r, c) in ((0, 1), (1, 0)) else (24, 30, 52)
            draw.rectangle([wx, wy, wx + 14, wy + 14], fill=col)
    # Blast scar across the middle.
    draw.polygon([(x0 + 96, y0 + 44), (x0 + 150, y0 + 30), (x0 + 168, y0 + 70),
                  (x0 + 120, y0 + 84), (x0 + 96, y0 + 70)], fill=(18, 22, 40))
    draw.line([x0 + 100, y0 + 48, x0 + 158, y0 + 62], fill=FIRE, width=4)
    # Rescue beam + ladder, right.
    draw.polygon([(x1 - 18, y1 - 10), (x1 - 44, y0 + 58), (x1 - 30, y0 + 58)],
                 fill=(250, 220, 140))
    draw.line([x1 - 52, y1 - 10, x1 - 34, y0 + 44], fill=CARD, width=4)
    for k in range(4):
        yy = y1 - 22 - k * 12
        draw.line([x1 - 56, yy, x1 - 30, yy], fill=CARD, width=2)
    # Smoke curls.
    for sx, sy, r in ((x0 + 120, y0 + 16, 9), (x0 + 140, y0 + 8, 7)):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)


def art_toll(draw, x0, y0, x1, y1):
    """Rising bars of the death toll, the last one brick red."""
    draw.rectangle([x0, y0, x1, y1], fill=(246, 232, 228))
    for gy in (y0 + 28, y0 + 52, y0 + 76):
        draw.line([x0 + 8, gy, x1 - 8, gy], fill=(228, 200, 192), width=1)
    base = y1 - 10
    bars = [(16, 20), (48, 32), (80, 46), (112, 62)]
    for i, (bx, bh) in enumerate(bars):
        col = BRICK if i == 3 else (150, 160, 178)
        draw.rectangle([x0 + bx, base - bh, x0 + bx + 24, base], fill=col)
    # No text in the art: the headline below already says "near
    # 700,000", and the tag chip sits over this corner. The bars
    # alone carry the visual weight.


def art_ship(draw, x0, y0, x1, y1):
    """Corvette listing at Benghazi at night, drone overhead, fire."""
    draw.rectangle([x0, y0, x1, y1], fill=(18, 34, 58))
    draw.ellipse([x1 - 40, y0 + 6, x1 - 12, y0 + 34], fill=GOLD_PALE)
    # Sea (two wave lines only -- the 92px band has no room for more).
    draw.rectangle([x0, y0 + 62, x1, y1], fill=(24, 56, 88))
    for yy in (y0 + 70, y0 + 82):
        draw.line([x0 + 8, yy, x1 - 8, yy], fill=(70, 120, 155), width=2)
    # Corvette, listing to port, smoke and flame amidships.
    draw.polygon([(x0 + 14, y1 - 30), (x1 - 20, y1 - 30), (x1 - 40, y1 - 14),
                  (x0 + 34, y1 - 14)], fill=(120, 128, 142))
    draw.rectangle([x0 + 40, y1 - 52, x0 + 78, y1 - 30], fill=(90, 98, 114))
    draw.rectangle([x0 + 96, y1 - 46, x0 + 104, y1 - 30], fill=(90, 98, 114))
    draw.polygon([(x0 + 82, y1 - 40), (x0 + 94, y1 - 62), (x0 + 106, y1 - 40)],
                 fill=FIRE)
    draw.polygon([(x0 + 88, y1 - 44), (x0 + 94, y1 - 58), (x0 + 100, y1 - 44)],
                 fill=GOLD)
    draw.ellipse([x0 + 78, y1 - 78, x0 + 108, y1 - 52], fill=SMOKE)
    # Naval drone above, small quad silhouette.
    dx, dy = x1 - 52, y0 + 44
    draw.rectangle([dx - 12, dy - 3, dx + 12, dy + 3], fill=CARD)
    draw.ellipse([dx - 18, dy - 6, dx - 8, dy + 2], outline=CARD, width=2)
    draw.ellipse([dx + 8, dy - 6, dx + 18, dy + 2], outline=CARD, width=2)
    draw.line([dx, dy + 3, dx + 6, y1 - 62], fill=GOLD_PALE, width=1)


def art_factory(draw, x0, y0, x1, y1):
    """Three-storey factory in flames, smoke column, search light."""
    draw.rectangle([x0, y0, x1, y1], fill=(40, 36, 34))
    # Smoke column, right of the tag chip's corner.
    for sx, sy, r in ((x0 + 150, y0 + 12, 14), (x0 + 168, y0 + 24, 18),
                      (x0 + 148, y0 + 36, 12)):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)
    # Factory block: one row of windows only -- the 92px art band
    # has no room for a second row.
    draw.rectangle([x0 + 16, y0 + 52, x1 - 16, y1 - 12], fill=(96, 88, 80))
    draw.rectangle([x0 + 16, y0 + 52, x1 - 16, y0 + 62], fill=(70, 64, 58))
    for c in range(4):
        wx, wy = x0 + 28 + c * 34, y0 + 68
        col = FIRE if c in (1, 2) else (30, 28, 26)
        draw.rectangle([wx, wy, wx + 20, wy + 12], fill=col)
    # Flames licking the roofline.
    for fx in (x0 + 30, x0 + 70, x0 + 110, x0 + 142):
        draw.polygon([(fx, y0 + 54), (fx + 10, y0 + 30), (fx + 20, y0 + 54)],
                     fill=FIRE)
        draw.polygon([(fx + 5, y0 + 54), (fx + 10, y0 + 40), (fx + 15, y0 + 54)],
                     fill=GOLD)
    # Ground + search beam.
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(24, 22, 20))
    draw.polygon([(x1 - 14, y1 - 12), (x1 - 46, y0 + 40), (x1 - 30, y0 + 40)],
                 fill=(250, 220, 140))


def art_eu(draw, x0, y0, x1, y1):
    """EU circle of stars over a bank facade and a shadow-fleet ship."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 234, 246))
    # Stars circle, left, kept clear of the tag chip overhead.
    cx, cy = x0 + 48, y0 + 64
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        sx, sy = cx + 26 * math.cos(ang), cy + 26 * math.sin(ang)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD_DARK)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=INK)
    draw.text((cx - 7, cy - 9), "€", font=font(BOLD, 18), fill=GOLD_PALE)
    # Bank facade, right.
    draw.rectangle([x0 + 96, y0 + 34, x1 - 10, y1 - 14], fill=CARD)
    draw.polygon([(x0 + 92, y0 + 34), (x1 - 6, y0 + 34),
                  ((x0 + x1) // 2 - 4, y0 + 14)], fill=INK)
    for i in range(3):
        colx = x0 + 106 + i * 22
        draw.rectangle([colx, y0 + 48, colx + 8, y1 - 26], fill=INK)
    draw.rectangle([x0 + 96, y1 - 26, x1 - 10, y1 - 14], fill=INK)
    # Red ban slash across the facade corner.
    draw.line([x1 - 34, y0 + 40, x1 - 10, y0 + 64], fill=BRICK, width=5)
    draw.ellipse([x1 - 36, y0 + 38, x1 - 8, y0 + 66], outline=BRICK, width=3)


# ------------------------------------------------------------- strip art
def art_mexico(draw, x0, y0, x1, y1):
    """Courthouse columns + gavel, flat."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 226, 210))
    draw.polygon([(x0 + 8, y0 + 18), (x1 - 8, y0 + 18), ((x0 + x1) // 2, y0 + 4)],
                 fill=INK)
    for i in range(4):
        colx = x0 + 16 + i * 22
        draw.rectangle([colx, y0 + 22, colx + 8, y1 - 14], fill=INK)
    draw.rectangle([x0 + 8, y1 - 14, x1 - 8, y1 - 6], fill=INK)
    draw.rectangle([x0 + 66, y0 + 40, x0 + 86, y0 + 46], fill=BRICK)
    draw.line([x0 + 76, y0 + 46, x0 + 76, y0 + 50], fill=BRICK, width=4)


def art_fifa(draw, x0, y0, x1, y1):
    """Football on green, with a gold trophy cup."""
    draw.rectangle([x0, y0, x1, y1], fill=(36, 110, 70))
    for i in range(3):
        draw.line([x0, y0 + 14 + i * 14, x1, y0 + 14 + i * 14],
                  fill=(52, 132, 88), width=8)
    # Ball, kept below the tag chip's corner and inside the 52px band.
    bx, by = x0 + 36, y0 + 34
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=CARD)
    draw.polygon([(bx, by - 8), (bx + 8, by), (bx, by + 8), (bx - 8, by)],
                 fill=INK)
    # Trophy.
    tx = x1 - 34
    draw.polygon([(tx - 12, y0 + 14), (tx + 12, y0 + 14), (tx + 8, y0 + 34),
                  (tx - 8, y0 + 34)], fill=GOLD)
    draw.arc([tx - 20, y0 + 14, tx - 4, y0 + 30], 90, 270, fill=GOLD, width=3)
    draw.arc([tx + 4, y0 + 14, tx + 20, y0 + 30], 270, 90, fill=GOLD, width=3)
    draw.rectangle([tx - 3, y0 + 34, tx + 3, y0 + 46], fill=GOLD)
    draw.rectangle([tx - 10, y0 + 46, tx + 10, y0 + 52], fill=GOLD)


def art_korea(draw, x0, y0, x1, y1):
    """Jet climbing past a radar sweep over the East Sea."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # Radar sweep, sized to the 52px strip band.
    rx, ry = x1 - 28, y0 + 30
    draw.ellipse([rx - 16, ry - 16, rx + 16, ry + 16], outline=INK_SOFT, width=2)
    draw.line([rx, ry, rx + 11, ry - 11], fill=BRICK, width=3)
    draw.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=BRICK)
    # Island + sea.
    draw.ellipse([x0 + 6, y1 - 22, x0 + 62, y1 - 4], fill=(52, 128, 74))
    draw.rectangle([x0, y1 - 8, x1, y1], fill=SEA)
    # Jet climbing.
    jx, jy = x0 + 22, y0 + 44
    draw.polygon([(jx, jy), (jx + 36, jy - 12), (jx + 44, jy - 6),
                  (jx + 10, jy + 8)], fill=INK)
    draw.polygon([(jx + 14, jy - 10), (jx + 26, jy - 16), (jx + 26, jy - 6)],
                 fill=INK)
    for i in range(2):
        draw.line([jx - 6 - i * 8, jy + 10 + i * 4, jx - 12 - i * 8, jy + 12 + i * 4],
                  fill=INK_SOFT, width=2)


# ---------------------------------------------------------------- layout
def panel(draw, x0, y0, x1, y1, tag, headline, body, art, accent=BRICK,
          big=None):
    """One grid panel: art band on top (tag chip overlaid on the art),
    then headline and body in the space below. Nothing may pass y1:
    art 92 + headline (2 lines x 22) + body (2 lines x 16) fits a
    196px panel with room to spare; bodies are kept to two lines."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=CARD,
                           outline=BORDER, width=1)
    art_h = 92
    art(draw, x0 + 1, y0 + 1, x1 - 1, y0 + art_h)
    draw.line([x0, y0 + art_h, x1, y0 + art_h], fill=BORDER, width=1)
    tag_chip(draw, x0 + 10, y0 + 8, tag, fill=accent)
    tx = x0 + 12
    hy = y0 + art_h + 10
    hf = font(BOLD, 18)
    hl = wrap_text(draw, headline, hf, (x1 - x0) - 24)
    hy = draw_lines(draw, tx, hy, hl[:2], hf, INK, 21)
    bfnt = font(REG, 13)
    bl = wrap_text(draw, body, bfnt, (x1 - x0) - 24)
    draw_lines(draw, tx, hy + 4, bl[:2], bfnt, INK_SOFT, 16)


def strip_item(draw, x0, y0, x1, y1, tag, headline, body, art):
    """One column of the MORE TODAY strip: 52px art band with the tag
    chip overlaid on it, then headline (2 lines) and body (2 lines).
    Total content height stays inside the 144px strip box."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=CARD,
                           outline=BORDER, width=1)
    art(draw, x0 + 1, y0 + 1, x1 - 1, y0 + 52)
    draw.line([x0, y0 + 52, x1, y0 + 52], fill=BORDER, width=1)
    tag_chip(draw, x0 + 8, y0 + 7, tag, fill=INK)
    tx = x0 + 10
    hy = y0 + 60
    hf = font(BOLD, 15)
    hl = wrap_text(draw, headline, hf, (x1 - x0) - 20)
    hy = draw_lines(draw, tx, hy, hl[:2], hf, INK, 18)
    bfnt = font(REG, 12)
    bl = wrap_text(draw, body, bfnt, (x1 - x0) - 20)
    draw_lines(draw, tx, hy + 3, bl[:2], bfnt, INK_SOFT, 15)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer double border.
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)
    d.rectangle([14, 14, W - 15, H - 15], outline=BORDER, width=1)

    # ---- masthead ------------------------------------------------------
    # 90px tall: label + date only, so nothing can spill past the band.
    hx0, hy0, hx1, hy1 = MARGIN, MARGIN, W - MARGIN, 112
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=8, fill=INK)
    d.text((hx0 + 18, hy0 + 10), "THE WORLD IN ONE DAY",
           font=font(BOLD, 16), fill=GOLD)
    d.text((hx0 + 18, hy0 + 32), "24 NOVEMBER 2026",
           font=font(BOLD, 44), fill=CARD)
    # Right-hand masthead box: the day's verdict.
    bx0 = hx1 - 208
    d.rectangle([bx0, hy0, hx1, hy1], fill=BRICK)
    d.text((bx0 + 14, hy0 + 10), "TOP STORY", font=font(BOLD, 14),
           fill=GOLD_PALE)
    d.text((bx0 + 14, hy0 + 30), "COP31 FAILS", font=font(BOLD, 26),
           fill=CARD)
    d.text((bx0 + 14, hy0 + 62), "No deal in Antalya",
           font=font(REG, 14), fill=(250, 228, 210))

    # ---- hero: COP31 ---------------------------------------------------
    gx0, gy0, gx1, gy1 = MARGIN, 124, W - MARGIN, 332
    d.rounded_rectangle([gx0, gy0, gx1, gy1], radius=8, fill=NAVY_PANEL,
                        outline=BORDER, width=1)
    # Art on the right third.
    ax0 = gx1 - 330
    art_cop31(d, ax0, gy0 + 1, gx1 - 1, gy1 - 1)
    d.line([ax0, gy0, ax0, gy1], fill=BORDER, width=1)
    tx = gx0 + 20
    tag_chip(d, tx, gy0 + 14, "CLIMATE  •  HERO", fill=TEAL)
    hf = font(BOLD, 40)
    hl = wrap_text(d, "COP31 ENDS IN DEADLOCK", hf, ax0 - gx0 - 40)
    y = draw_lines(d, tx, gy0 + 48, hl, hf, CARD, 46)
    sub = ("No climate pact as talks collapse in Antalya — "
           "the draft left out fossil fuels.")
    sf = font(REG, 19)
    sl = wrap_text(d, sub, sf, ax0 - gx0 - 40)
    y = draw_lines(d, tx, gy0 + 102, sl, sf, (214, 226, 238), 24)
    # Callout bar inside the hero.
    cy = gy1 - 48
    d.rounded_rectangle([tx, cy, ax0 - 20, cy + 36], radius=6, fill=BRICK)
    d.text((tx + 12, cy + 8), "First COP with no deal since 2009",
           font=font(BOLD, 16), fill=CARD)

    # ---- six panels, 3 x 2 ---------------------------------------------
    # Bodies are kept short on purpose: at 13pt, two lines fit the
    # space below the headline; anything longer would be clipped.
    px0, py0 = MARGIN, 344
    gap = 12
    pw = (CONTENT_W - 2 * gap) // 3
    ph = 196
    panels = [
        ("US–IRAN", "US weighs weeks-long Iran campaign",
         "Second carrier sails to the Gulf as Trump warns of "
         "'very traumatic' fallout.",
         art_carrier, BRICK, None),
        ("UKRAINE", "Strike kills 2, wounds 22 in Zaporizhzhia",
         "Overnight attack hits homes; 2 children among the "
         "wounded, officials say.",
         art_zaporizhzhia, INK, None),
        ("WAR TOLL", "Russian war dead near 700,000",
         "Meduza–Mediazona estimate; 490,000 deaths "
         "registered.",
         art_toll, BRICK_DARK, None),
        ("SEA WAR", "Ukraine sinks Russian corvette off Libya",
         "Drones hit the Merkury at Benghazi; Novoshakhtinsk "
         "refinery ablaze, halted.",
         art_ship, SEA, None),
        ("INDONESIA", "Candy factory fire: 3 dead, 34 missing",
         "Fire guts the Milkita factory in Cikande, Banten; "
         "DNA tests to identify victims.",
         art_factory, FIRE, None),
        ("EUROPE", "EU unveils 22nd Russia sanctions package",
         "60 banks cut from SWIFT; 70+ shadow-fleet ships "
         "listed; Russian flag barred.",
         art_eu, INK, None),
    ]
    for i, (tag, head, body, art, accent, big) in enumerate(panels):
        col, row = i % 3, i // 3
        x0 = px0 + col * (pw + gap)
        y0 = py0 + row * (ph + gap)
        panel(d, x0, y0, x0 + pw, y0 + ph, tag, head, body, art,
              accent=accent, big=big)

    # ---- MORE TODAY strip ----------------------------------------------
    sy0 = py0 + 2 * ph + gap + 12
    d.text((MARGIN, sy0), "MORE TODAY", font=font(BOLD, 20), fill=INK)
    rule(d, MARGIN + 148, sy0 + 13, W - MARGIN, color=INK, width=2)
    sx0, sy1 = MARGIN, sy0 + 30
    sh = 144
    strip = [
        ("MEXICO", "Mexico to try 'El Chapo Isidro' at home",
         "Despite a US extradition request, the attorney "
         "general says he faces trial in Mexico.", art_mexico),
        ("SPORT", "Women's World Cup hosts set",
         "2031: USA, Mexico, Costa Rica, Jamaica, 48 teams. "
         "2035: the UK.", art_fifa),
        ("KOREA", "Russian jets enter Korea's air zone",
         "Seoul scrambles fighters off Ulleung; alert lifted "
         "in 3 minutes. No violation.", art_korea),
    ]
    for i, (tag, head, body, art) in enumerate(strip):
        x0 = sx0 + i * (pw + gap)
        strip_item(d, x0, sy1, x0 + pw, sy1 + sh, tag, head, body, art)

    # ---- footer ----------------------------------------------------------
    fy = sy1 + sh + 12
    rule(d, MARGIN, fy, W - MARGIN, color=BORDER, width=1)
    d.text((MARGIN, fy + 8),
           "Sources: Reuters • AP • FIFA • European Commission • PINA • "
           "Mediazona / Meduza — all figures verified 24 Nov 2026.",
           font=font(REG, 11), fill=MUTED)
    d.text((MARGIN, fy + 24),
           "news-image-20261124  •  $100 bounty  •  Drawn from scratch "
           "with Python + Pillow. No photos, no AI images.",
           font=font(REG, 11), fill=MUTED)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"Wrote {out} ({out.stat().st_size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
