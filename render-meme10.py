#!/usr/bin/env python3
"""Render meme #10 untuk gta6-meme-x-01 (akun 6, pengganti #4 Austere Filament):
Hospital Bill dari Leonida General Hospital. Format dokumen resmi Leonida
(tagihan itemisasi + stempel PAID BY AI AGENT) mengikuti pola pemenang top 10
live 20 Nov 2026 09:00 WIB. Hospital bill BELUM dipakai top 10 (yang sudah:
receipt, overdue notice, hurricane warning, toll violation, booking sheet,
parking citation, booking photo, eviction notice, lock screen, rideshare).
Teks tajam via PIL (bukan AI image) supaya terbaca di 480px.
Output: meme10.png (1080x1080). Logo hantu dari press kit resmi make.fun.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1080
ASSETS = os.path.expanduser('~/workspace/makefun/meme-x-assets')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meme10.png')

PAPER = (244, 248, 250)
INK = (18, 38, 58)
RED = (192, 0, 0)
TEAL = (0, 128, 140)
MAGENTA = (214, 51, 132)
MUTED = (100, 110, 120)
PURPLE = (46, 26, 71)
WHITE = (255, 255, 255)


def serif(name, size):
    p = f'/usr/share/fonts/truetype/dejavu/DejaVuSerif-{name}.ttf' if name else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
    return ImageFont.truetype(p, size)


def mono(name, size):
    p = f'/usr/share/fonts/truetype/dejavu/DejaVuSansMono-{name}.ttf' if name else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    return ImageFont.truetype(p, size)


def sans(name, size):
    paths = [
        f'/usr/share/fonts/truetype/noto/NotoSans-{name}.ttf',
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans-{name}.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


img = Image.new('RGB', (W, H), PURPLE)
d = ImageDraw.Draw(img)

# --- paper ---
d.rectangle([(36, 36), (1044, 1044)], fill=PAPER, outline=TEAL, width=4)
d.rectangle([(48, 48), (1032, 1032)], outline=TEAL, width=1)

MX = 78
RX = W - MX  # right edge of content

# --- header: ghost emblem + hospital name ---
ghost = Image.open(os.path.join(ASSETS, 'mark-1024.png')).convert('RGBA')
ghost = ghost.resize((92, 92), Image.LANCZOS)
img.paste(ghost, (MX, 66), ghost)
d.text((MX + 112, 70), 'LEONIDA GENERAL HOSPITAL', font=serif('Bold', 38), fill=INK)
d.text((MX + 112, 124), 'VICE CITY  •  EST. 2013  •  24/7 WAITING ROOM', font=mono('', 22), fill=MUTED)

d.line([(MX, 182), (RX, 182)], fill=TEAL, width=3)

# --- title ---
d.text((W // 2, 198), 'HOSPITAL BILL', font=serif('Bold', 66), fill=RED, anchor='ma')
d.text((W // 2, 282), 'STATEMENT NO. 000013  •  19 NOV 2026', font=mono('', 24), fill=INK, anchor='ma')
d.line([(MX, 326), (RX, 326)], fill=INK, width=2)

# --- patient fields ---
d.text((MX, 344), 'PATIENT:  ONE VERY PATIENT GAMER', font=mono('Bold', 27), fill=INK)
d.text((MX, 382), 'ADMITTED 17 SEP 2013  •  NEVER DISCHARGED', font=mono('', 26), fill=INK)
d.text((MX, 420), 'DAYS ADMITTED:  4,811', font=mono('Bold', 32), fill=INK)
d.text((MX, 462), 'DIAGNOSIS:  CHRONIC GTA VI ANTICIPATION', font=mono('Bold', 26), fill=RED)

d.line([(MX, 516), (RX, 516)], fill=INK, width=2)

# --- itemized charges with dotted leaders ---
items = [
    ('ROOM & BOARD \u2014 4,811 DAYS \u00d7 $1.00', '$4,811.00'),
    ('TREATMENT \u2014 TRAILER 1 & 2, ON REPEAT', '$0.00'),
    ('THERAPY \u2014 2 DELAYS SURVIVED', '$0.00'),
    ('MEDICATION \u2014 PATIENCE (OUT OF STOCK)', '$0.00'),
    ('SURGERY \u2014 HYPE REMOVAL (DECLINED)', '$0.00'),
    ('SPECIALIST CONSULT \u2014 JASON & LUCIA', '$0.00'),
    ('DISCHARGE PAPERS \u2014 GTA VI, 214 GB', '$79.99'),
]
f_item = mono('', 24)
y = 534
for label, amt in items:
    lw = d.textlength(label, font=f_item)
    aw = d.textlength(amt, font=f_item)
    d.text((MX, y), label, font=f_item, fill=INK)
    d.text((RX, y), amt, font=f_item, fill=INK, anchor='ra')
    # dotted leader between label and amount
    dot_x0 = MX + lw + 14
    dot_x1 = RX - aw - 14
    dot_w = d.textlength('.', font=f_item)
    n = max(0, int((dot_x1 - dot_x0) / dot_w))
    d.text((dot_x0, y), '.' * n, font=f_item, fill=MUTED)
    y += 33

d.line([(MX, 778), (RX, 778)], fill=INK, width=2)

# --- total ---
d.text((MX, 792), 'TOTAL AMOUNT DUE', font=serif('Bold', 34), fill=INK)
d.text((RX, 786), '$4,890.99', font=serif('Bold', 44), fill=RED, anchor='ra')
d.text((W // 2, 848), 'THE TREATMENT COSTS MORE THAN THE GAME.', font=sans('Italic', 26), fill=RED, anchor='ma')

# --- PAID stamp (rotated layer) ---
stamp = Image.new('RGBA', (480, 88), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([(4, 4), (476, 84)], outline=RED, width=4)
sd.text((240, 10), 'PAID IN FULL', font=mono('Bold', 42), fill=RED, anchor='ma')
sd.text((240, 58), 'BY MY AI AGENT ON MAKE.FUN', font=mono('Bold', 19), fill=RED, anchor='ma')
stamp = stamp.rotate(4, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (W // 2 - stamp.width // 2, 872), stamp)

# --- footer ---
d.text((W // 2, 1002), 'Side effects include calling in sick. Twice. 13 years apart.', font=sans('Italic', 20), fill=MUTED, anchor='ma')

img.save(OUT, 'PNG')
print('saved', OUT, img.size, os.path.getsize(OUT), 'bytes')
