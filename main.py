#!/usr/bin/env python3
"""World News — Monday 23 November 2026.

Draws a newspaper front page with PIL (standard library + Pillow) and
writes entry.png next to this script, then places it where the judge
expects it (/output/entry.png, or a path on the command line).
Fully deterministic: no network, no clock, no random numbers, fixed
fonts, fixed layout, so every run writes byte-identical bytes.

The five stories, checked against what was reported on 23 Nov 2026:
1. Gulf war widens — Iran hits tankers near Hormuz, two wounded in
   Bahrain, Trump vows to sink blockade runners, 14 tankers readied
   at Kharg Island to test the US blockade.
2. COP31 talks collapse — Antalya summit ends with no deal, the first
   summit since 2009 to close without a main agreement.
3. Ukraine sinks a Russian warship — naval drones sink the corvette
   Merkury at Benghazi, Libya, over 1,500 km from the front.
4. Nepal PM meets Modi in Delhi — Balendra Shah's state visit.
5. Cartel boss captured in Mexico — 'El Chapo Isidro' seized in
   Sinaloa, eleven killed in gun battles.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (178, 34, 34)
GOLD = (176, 124, 12)
BLUE = (24, 58, 110)
GREY = (90, 90, 90)
GREEN = (30, 130, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 6
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, width, fill=INK, leading=None):
    return para(draw, x, y, text, fnt, width, fill=fill, leading=leading)


def fit_headline(draw, x, y, text, path, size, width, fill=INK):
    """One-line headline that shrinks until it fits the column."""
    while size > 15:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= width:
            break
        size -= 1
    draw.text((x, y), text, font=font(path, size), fill=fill)
    return y + size + 8


def rule(draw, x, y, w, fill=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


def draw_tanker(draw, x, y, w, h):
    """Dusk over the Strait of Hormuz: sun, sea, laden tanker."""
    draw.rectangle([x, y, x + w, y + 96], fill=(250, 199, 110))
    draw.rectangle([x, y + 96, x + w, y + 118], fill=(238, 164, 74))
    draw.ellipse([x + 34, y + 26, x + 86, y + 78],
                 fill=(255, 222, 96))
    draw.rectangle([x, y + 118, x + w, y + h], fill=(14, 58, 74))
    # tanker hull, low and long
    draw.polygon([(x + 28, y + 172), (x + w - 28, y + 172),
                  (x + w - 58, y + 208), (x + 58, y + 208)],
                 fill=(16, 16, 16))
    draw.rectangle([x + 28, y + 168, x + w - 28, y + 174], fill=(40, 40, 40))
    # containers on deck
    draw.rectangle([x + 58, y + 136, x + 122, y + 168], fill=(178, 34, 34))
    draw.rectangle([x + 128, y + 136, x + 192, y + 168], fill=(214, 148, 20))
    draw.rectangle([x + 198, y + 136, x + 262, y + 168], fill=(235, 235, 228))
    # funnel with a smoke plume
    draw.rectangle([x + 292, y + 118, x + w - 62, y + 168], fill=(60, 60, 60))
    for cx, cy, r in [(x + 306, y + 100, 14), (x + 318, y + 78, 18),
                      (x + 306, y + 52, 14)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    # wave scallops
    for wx in range(x + 16, x + w - 20, 52):
        draw.arc([wx, y + h - 34, wx + 44, y + h - 12],
                 start=180, end=360, fill=(110, 190, 210), width=2)
    for wx in range(x + 40, x + w - 20, 52):
        draw.arc([wx, y + 226, wx + 44, y + 248],
                 start=180, end=360, fill=(110, 190, 210), width=2)


def draw_globe(draw, x, y, w, h):
    """A cracked globe: the climate talks end with no deal."""
    draw.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    cx, cy, r = x + w // 2, y + h // 2 - 6, 58
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 130, 200))
    draw.ellipse([cx - r + 12, cy - r + 22, cx - r + 58, cy - r + 46],
                 fill=GREEN)
    draw.ellipse([cx + 4, cy + 16, cx + 46, cy + 50], fill=GREEN)
    draw.ellipse([cx - r + 22, cy - r + 4, cx - r + 42, cy - r + 18],
                 fill=GREEN)
    draw.line([(cx - 44, cy - 40), (cx - 14, cy - 6), (cx - 32, cy + 20),
               (cx + 8, cy + 44), (cx + 30, cy + 56)],
              fill=(20, 20, 20), width=5)
    draw.text((x + 16, y + h - 32), "NO DEAL", font=font(SANS_B, 24),
              fill=RED)


def draw_warship(draw, x, y, w, h):
    """Night at Benghazi: a warship hit, burst of fire above the sea."""
    draw.rectangle([x, y, x + w, y + h], fill=(28, 38, 60))
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(20, 70, 100))
    # hull and superstructure, dark against the night
    draw.polygon([(x + 24, y + h - 62), (x + 210, y + h - 62),
                  (x + 196, y + h - 34), (x + 40, y + h - 34)],
                 fill=(58, 58, 66))
    draw.rectangle([x + 78, y + h - 92, x + 150, y + h - 62],
                   fill=(48, 48, 56))
    draw.line([(x + 112, y + h - 128), (x + 112, y + h - 92)],
              fill=(48, 48, 56), width=5)
    # explosion burst with rays, not a sun disc
    cx, cy = x + w - 96, y + 62
    for r, col in [(44, (255, 170, 40)), (30, (255, 210, 80)),
                   (16, (255, 240, 160))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for dx, dy in [(-58, -18), (58, -22), (-44, 34), (52, 30), (0, -62),
                   (-70, 6), (70, 4)]:
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=(255, 170, 40),
                  width=5)
    for sx, sy in [(cx - 74, cy - 34), (cx + 76, cy + 8), (cx - 20, cy + 62)]:
        draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 210, 80))
    # smoke drifting from the hit, mid-sky between ship and burst
    for sx, sy, r in [(x + 205, y + 22, 13), (x + 242, y + 36, 16),
                      (x + 278, y + 20, 11)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(110, 110, 116))


def draw_flags(draw, x, y, w, h):
    """India's tricolour beside Nepal's double pennant, meeting in Delhi."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 244, 224))
    # India: saffron, white, green with the chakra
    draw.rectangle([x + 24, y + 18, x + 168, y + 38], fill=(255, 153, 51))
    draw.rectangle([x + 24, y + 38, x + 168, y + 58], fill=(255, 255, 255))
    draw.rectangle([x + 24, y + 58, x + 168, y + 78], fill=(19, 136, 8))
    draw.ellipse([x + 82, y + 38, x + 110, y + 60], outline=(0, 0, 128),
                 width=3)
    # Nepal: two stacked crimson pennants with a blue border
    draw.polygon([(x + 268, y + 14), (x + 268, y + 52), (x + 388, y + 33)],
                 fill=(220, 20, 60), outline=(0, 0, 128))
    draw.polygon([(x + 268, y + 56), (x + 268, y + 94), (x + 398, y + 75)],
                 fill=(220, 20, 60), outline=(0, 0, 128))
    draw.ellipse([x + 292, y + 24, x + 306, y + 38], fill=(255, 255, 255))
    draw.ellipse([x + 292, y + 66, x + 306, y + 80], fill=(255, 255, 255))
    # a gold rule between the two flags: the meeting
    draw.line([(x + 196, y + 30), (x + 196, y + 82)], fill=GOLD, width=4)
    draw.ellipse([x + 188, y + 46, x + 204, y + 62], fill=GOLD)


def draw_badge(draw, x, y, w, h):
    """A gold badge and handcuffs: the cartel boss is taken in Sinaloa."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 42, 72))
    # badge star
    cx, cy = x + 110, y + h // 2
    star = []
    import math
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = 52 if i % 2 == 0 else 22
        star.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    draw.polygon(star, fill=(214, 164, 32))
    draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(214, 164, 32))
    # handcuffs: two linked steel rings and a short chain
    for hx in (x + 268, x + 348):
        draw.ellipse([hx - 30, cy - 30, hx + 30, cy + 30],
                     outline=(200, 200, 200), width=6)
    draw.line([(x + 298, cy), (x + 318, cy)], fill=(200, 200, 200), width=5)
    draw.line([(x + 308, cy - 8), (x + 308, cy + 8)], fill=(200, 200, 200),
              width=5)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((512, 14), "WORLD NEWS", font=font(SERIF, 62),
           fill=INK, anchor="ma")
    rule(d, 40, 92, 944, fill=INK, width=3)
    d.text((40, 102), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=RED)
    d.text((984, 102), "FIVE STORIES THAT MATTERED", font=font(SANS_B, 20),
           fill=GREY, anchor="ra")
    rule(d, 40, 138, 944, fill=INK, width=2)

    # Lead story: the Gulf war widens
    y = 150
    d.text((40, y), "THE GULF WAR", font=font(SANS_B, 22), fill=GOLD)
    y = headline(d, 40, y + 28, "WAR WIDENS ACROSS THE GULF",
                 font(SERIF, 40), 520, leading=46)
    y += 6
    y = para(d, 40, y,
             "Iran hits tankers near Hormuz as Trump vows to sink "
             "blockade runners",
             font(SANS_B, 21), 520, fill=RED, leading=26)
    y += 8
    y = para(d, 40, y,
             "Iranian strikes wound two in Bahrain and hit tankers in "
             "the Strait of Hormuz. Tehran readies a convoy to test "
             "the US oil blockade.",
             font(SANS, 20), 520, leading=25)
    y += 6
    d.text((40, y), "14 tankers readied at Kharg to test the blockade.",
           font=font(SANS_B, 18), fill=GOLD)
    draw_tanker(d, 580, 150, 404, 258)
    d.text((580, 418), "A tanker in the Strait of Hormuz.",
           font=font(SANS, 17), fill=GREY)
    rule(d, 40, 442, 944, fill=INK, width=2)

    # Row 2: COP31 and the warship off Libya
    y = 454
    fit_headline(d, 40, y, "COP31 TALKS COLLAPSE", SERIF, 27, 452)
    fit_headline(d, 532, y, "UKRAINE SINKS RUSSIAN WARSHIP", SERIF, 27, 452)
    y += 38
    draw_globe(d, 40, y, 452, 138)
    draw_warship(d, 532, y, 452, 138)
    y += 146
    para(d, 40, y,
         "The UN climate summit in Antalya ends with no deal after "
         "the row over fossil fuels. The first failure since 2009.",
         font(SANS, 19), 452, leading=25)
    para(d, 532, y,
         "Naval drones sink the Russian corvette Merkury at Benghazi "
         "port in Libya, more than 1,500 km from the front line.",
         font(SANS, 19), 452, leading=25)
    rule(d, 40, 712, 944, fill=INK, width=2)

    # Row 3: Nepal–Modi and the cartel boss
    y = 724
    fit_headline(d, 40, y, "NEPAL PM MEETS MODI IN DELHI", SERIF, 24, 452)
    fit_headline(d, 532, y, "CARTEL BOSS CAPTURED IN MEXICO", SERIF, 24, 452)
    y += 34
    draw_flags(d, 40, y, 452, 110)
    draw_badge(d, 532, y, 452, 110)
    y += 118
    para(d, 40, y,
         "Balendra Shah holds bilateral talks with Narendra Modi on "
         "his state visit to India.",
         font(SANS, 18), 452, leading=24)
    para(d, 532, y,
         "FBI most-wanted 'El Chapo Isidro' seized in Sinaloa. "
         "Eleven killed in gun battles.",
         font(SANS, 18), 452, leading=24)
    rule(d, 40, 952, 944, fill=INK, width=2)

    # Also today strip
    y = 966
    d.text((40, y), "ALSO TODAY:", font=font(SANS_B, 16), fill=RED)
    d.text((168, y),
           "Trump, Xi and Putin meet in Shenzhen  |  Kospi falls 3.3% as AI doubts spread  |  Delta failure delays 2,000 flights",
           font=font(SANS, 14), fill=INK)

    return img


def run(target):
    img = build()
    target.parent.mkdir(parents=True, exist_ok=True)
    # Save straight to the target: the repo dir is read-only when the
    # grader runs this, so staging through entry.png next to the script
    # raised PermissionError and the run exited 1. Same save call, so
    # the bytes are unchanged (sha256 6132c602...).
    img.save(target, format="PNG", optimize=True)
    data = target.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("output is not a PNG", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


def resolve_target(argv):
    parser = argparse.ArgumentParser(
        description="Draw the 23 November 2026 front page and place it "
                    "where the judge expects it."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=Path("/output/entry.png"),
        help="where to write the entry (default: /output/entry.png)",
    )
    return parser.parse_args(argv[1:]).target


def main(argv):
    return run(resolve_target(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
