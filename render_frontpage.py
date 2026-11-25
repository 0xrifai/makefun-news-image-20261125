#!/usr/bin/env python3
"""Render the 25 November 2026 front page: THE WORLD IN ONE DAY.

Draws a 1024x1024 newspaper front page with PIL only -- no photos, no
network, no timestamps, no randomness -- so the output PNG is byte-identical
on every run. Run: python3 render_frontpage.py  (writes entry.png next to
this file, and prints its size + sha256).
"""

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 245)
INK = (17, 17, 17)
RED = (158, 27, 27)
SEA = (31, 58, 95)
SEA_DARK = (22, 44, 74)
GREY = (90, 88, 82)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; returns a list of lines."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_numbers_strip(draw, x, y, w, h):
    """The day in numbers: four big figures, each labelled, in ruled columns."""
    rule(draw, x, y, x + w, 1)
    figures = [
        ("700,000+", "Russian soldiers killed in the Ukraine war, a new analysis finds"),
        ("3", "oil tankers hit by naval mines in the Strait of Hormuz"),
        ("60 km", "how close Houthi forces have pushed to Aden, Yemen"),
        ("11", "injured in a Houthi drone attack on a Riyadh tower"),
    ]
    col_w = w // 4
    nf = font(SERIF_B, 28)
    lf = font(SANS, 13)
    for i, (num, label) in enumerate(figures):
        cx = x + i * col_w
        if i:
            draw.line([(cx - 12, y + 10), (cx - 12, y + h - 12)], fill=(200, 198, 190), width=1)
        draw.text((cx, y + 8), num, font=nf, fill=RED)
        ly = y + 42
        for li, line in enumerate(wrap(draw, label, lf, col_w - 24)[:2]):
            draw.text((cx, ly + li * 16), line, font=lf, fill=INK)
    rule(draw, x, y + h, x + w, 1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36                      # side margin
    CW = W - 2 * MX              # content width: 952

    # --- frame: double rule around the page ---
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=2)
    d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

    y = 30
    # --- top line ---
    top = "ONE DAY  ·  ONE PAGE  ·  ALL THE WORLD'S NEWS"
    tf = font(SANS_B, 13)
    d.text(((W - d.textlength(top, font=tf)) / 2, y), top, font=tf, fill=GREY)
    y = 52

    # --- masthead ---
    mf = font(SERIF_B, 60)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=mf)) / 2, y), title, font=mf, fill=INK)
    y = 118
    rule(d, MX, y, W - MX, 4)
    rule(d, MX, y + 7, W - MX, 1)
    y = 132

    # --- date line ---
    df = font(SANS_B, 30)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=df)) / 2, y), date, font=df, fill=RED)
    y = 168
    sf = font(SERIF_I, 17)
    sub = "Every story below happened, or was first reported, on this day."
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=INK)
    y = 194
    rule(d, MX, y, W - MX, 1)

    # --- lead story ---
    y = 206
    kf = font(SANS_B, 16)
    d.text((MX, y), "UKRAINE WAR  —  GULF OF FINLAND", font=kf, fill=RED)
    y = 228
    hf = font(SERIF_B, 40)
    y = draw_wrapped(d, "Zelenskiy: Ukraine struck a Russian cargo ship in the Gulf of Finland",
                     hf, MX, y, CW, leading=46)
    y += 6
    df2 = font(SERIF, 20)
    y = draw_wrapped(d, "Kyiv says its drones hit the vessel on Saturday; Norway urges caution "
                     "as tensions rise in the Baltic.", df2, MX, y, CW, leading=25)
    y = draw_wrapped(d, "Zelenskyy also confirmed Ukraine sank a Russian naval vessel in the "
                     "Libyan port of Benghazi on Sunday.", df2, MX, y, CW, leading=25)
    y += 10
    draw_numbers_strip(d, MX, y, CW, 78)
    y += 78 + 12

    # --- also-today strip: Australia CPI (verified: ABS, released 25 Nov) ---
    rule(d, MX, y, W - MX, 1)
    y += 8
    strip_k = font(SANS_B, 15)
    strip_t = font(SERIF, 17)
    label = "ALSO TODAY —  "
    d.text((MX, y), label, font=strip_k, fill=RED)
    lx = MX + d.textlength(label, font=strip_k)
    d.text((lx, y - 1), "Australia's inflation jumps to 4.9%, up from 4.3%, fuelling fears of "
           "another interest-rate rise.", font=strip_t, fill=INK)
    y += 26
    rule(d, MX, y, W - MX, 1)
    y += 12

    # --- grid: 8 stories, 2 columns x 4 rows ---
    stories = [
        ("UKRAINE WAR — THE TOLL",
         "More than 700,000 Russian soldiers killed, analysis finds",
         "A new study puts Russia's war dead past 700,000 — the grimmest toll yet of the invasion of Ukraine."),
        ("IRAN — STRAIT OF HORMUZ",
         "Three oil tankers hit by mines in the Strait of Hormuz",
         "Iran's Revolutionary Guard Navy claims the strikes, as Tehran braces for winter gas shortages and power rationing."),
        ("NATO — POLAND",
         "NATO to send early-warning aircraft to Poland",
         "The move follows missiles landing in Poland during an attack on Ukraine."),
        ("UNITED STATES — CHINA",
         "Huawei convicted in sprawling US criminal trial",
         "Guilty of stealing trade secrets over its Iran business; acquitted of racketeering."),
        ("UNITED STATES",
         "Trump honours Giuliani and pardons two turkeys",
         "The former mayor receives the Medal of Freedom; turkeys “Freedom” and “Feathers” are spared for Thanksgiving."),
        ("YEMEN — SAUDI ARABIA",
         "Houthis advance to within 60 km of Aden",
         "A Houthi drone attack on a Riyadh tower injures 11, Saudi civil defence says."),
        ("CUBA — HEALTH",
         "WHO chief: lift the US fuel blockade on Cuba",
         "Tedros warns children's lives are at risk as fuel runs short on the island."),
        ("UNITED STATES — AVIATION",
         "Radar outage delays flights at Chicago O'Hare",
         "The FAA says air traffic is disrupted after a radar failure at the airport."),
    ]
    gutter = 24
    col_w = (CW - gutter) // 2
    row_h = 106
    gk = font(SANS_B, 14)
    gh = font(SERIF_B, 22)
    gd = font(SERIF, 16)
    for i, (kicker, headline, deck) in enumerate(stories):
        cx = MX + (i % 2) * (col_w + gutter)
        cy = y + (i // 2) * row_h
        d.text((cx, cy), kicker, font=gk, fill=RED)
        hy = cy + 19
        lines = wrap(d, headline, gh, col_w)
        for li, line in enumerate(lines[:2]):
            d.text((cx, hy + li * 25), line, font=gh, fill=INK)
        dy = hy + min(len(lines), 2) * 25 + 2
        for li, line in enumerate(wrap(d, deck, gd, col_w)[:2]):
            d.text((cx, dy + li * 19), line, font=gd, fill=INK)
        # vertical divider between the two columns
        if i % 2 == 0:
            d.line([(MX + col_w + gutter // 2, cy + 2),
                    (MX + col_w + gutter // 2, cy + row_h - 12)], fill=(200, 198, 190), width=1)
    y += 4 * row_h + 4

    # --- footer: date again + the day's observance ---
    rule(d, MX, y, W - MX, 1)
    y += 8
    ff = font(SERIF_I, 15)
    foot = "Wednesday, 25 November 2026  ·  International Day for the Elimination of Violence against Women"
    d.text(((W - d.textlength(foot, font=ff)) / 2, y), foot, font=ff, fill=INK)
    y += 21
    ff2 = font(SERIF_I, 13)
    foot2 = "Every story on this page happened, or was first reported, on Wednesday 25 November 2026."
    d.text(((W - d.textlength(foot2, font=ff2)) / 2, y), foot2, font=ff2, fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    data = out.read_bytes()
    print(f"wrote {out}  {img.size[0]}x{img.size[1]}  {len(data)} bytes")
    print("sha256:", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
