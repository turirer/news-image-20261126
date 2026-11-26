#!/usr/bin/env python3
"""Draw entry.png for the news-image-20261126 bounty.

The picture sums up Thursday 26 November 2026: a masthead naming the day,
one hero panel (the new US tariffs), and 44 further stories grouped into
seven region columns. Everything is drawn with PIL primitives and DejaVu
fonts; the output is a deterministic 1024x1024 PNG.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

INK = (14, 22, 38)          # page background
PANEL = (22, 33, 58)        # region panel fill
EDGE = (42, 58, 95)         # panel border
PAPER = (244, 239, 228)     # masthead band
PAPER_INK = (24, 28, 40)
TEXT = (236, 238, 245)
MUTED = (168, 178, 198)
FAINT = (120, 132, 158)

REGION_COLOURS = {
    "MIDDLE EAST": (201, 138, 45),
    "EUROPE": (63, 111, 181),
    "NORTH AMERICA": (181, 68, 60),
    "SOUTH AMERICA": (61, 153, 112),
    "AFRICA": (138, 95, 176),
    "ASIA": (194, 77, 122),
    "OCEANIA": (45, 157, 181),
}

# (headline, detail) pairs, all reported on 26 November 2026.
STORIES = {
    "MIDDLE EAST": [
        ("Houthis strike Saudi refinery and port",
         "Ras Tanura and Jizan hit; Riyadh says drones intercepted"),
        ("Ships hit Iranian mines near Hormuz",
         "Two vessels struck; oil prices climb on supply fears"),
        ("Blast near tanker west of Dubai",
         "Unknown projectile explodes; crew reported safe"),
        ("Iran rejects Israel chemical-arms claim",
         "Tehran calls it a ploy to deceive Washington"),
        ("Pezeshkian: sanctions failed to stop Iran",
         "President says war and pressure did not halt progress"),
        ("Libya's Haftar meets Erdogan in Ankara",
         "Eastern commander signals warmer Turkey ties"),
    ],
    "EUROPE": [
        ("Ukraine damages five Russian jets",
         "MiG-31s and Su-34s hit at Savasleyka airbase"),
        ("Kerch Bridge hit third time in a week",
         "Russia says 600 drones intercepted over Moscow"),
        ("Russian missiles hit Kyiv mall, toll 10",
         "Ballistic strikes injure seven in the capital"),
        ("Abu Dhabi peace talks stall",
         "Moscow insists on territorial claims; power grid hit"),
        ("EU leaders clash over \u20ac45bn Ukraine loan",
         "Brussels summit split on budget and funding"),
        ("Spain snap election on Sunday",
         "S\u00e1nchez fights to keep power after eight years"),
        ("London Tube strike hits Thursday\u2013Friday",
         "Severe disruption across the Underground"),
        ("Estonia shuts border with Russia",
         "Move follows GRU-linked sabotage attack"),
        ("Liverpool win 3\u20130 at Club Brugge",
         "Isak brace in Champions League matchday five"),
        ("Lille shock Bayern 2\u20131",
         "Comeback hands Bayern a first away defeat"),
    ],
    "NORTH AMERICA": [
        ("AI sell-off drags Nasdaq toward bear market",
         "Chip and AI stocks slide; futures down about 3%"),
        ("S&P puts Nvidia on downgrade watch",
         "Ratings agency flags board oversight worries"),
        ("FedEx jet overruns Miami runway",
         "FAA ground stop on Thanksgiving Eve; delays 214 min"),
        ("US Q3 GDP revised sharply higher",
         "Consumer spending and AI investment power growth"),
        ("CDC: nine measles deaths in 2026",
         "US health agency reports the year's toll"),
        ("Macy's parade postponed by storm",
         "100th Thanksgiving parade moved to Saturday, a first"),
        ("Rams beat Packers 26\u201313",
         "Thanksgiving Day win at SoFi Stadium"),
    ],
    "SOUTH AMERICA": [
        ("Colombia frees about 30 hostages",
         "18-hour standoff in Cartagena ends; gunman killed"),
        ("Venezuela to close quake camps by Dec 31",
         "2,200 families rehoused in La Guaira state"),
        ("Banco Macro profit falls 64%",
         "Margin squeeze and restructuring costs bite"),
        ("Mexico thrash Cameroon 4\u20130",
         "Second-half rout at the Under-17 World Cup"),
    ],
    "AFRICA": [
        ("Cairo tanker fire kills 31",
         "Fuel-truck blaze on the ring road injures 21"),
        ("Nigeria seizes $227M of meth",
         "1.5 tonnes found; five Mexicans arrested in Enugu"),
        ("Militants kill 30 in Niger State",
         "Homes burned in retaliation attacks in Nigeria"),
        ("DR Congo Ebola passes 12,000 cases",
         "Nearly 6,000 deaths as conflict hampers response"),
        ("Ramaphosa cleared in Phala Phala case",
         "Court sets aside report; impeachment avoided"),
        ("IMF approves $425M Guinea programme",
         "Economic and financial package agreed"),
    ],
    "ASIA": [
        ("Kim urges wider tactical-nuke use",
         "Pyongyang tours nuclear sites; \u201cdeclaration of war\u201d"),
        ("Pakistani astronaut reaches Tiangong",
         "Muhammad Zeeshan Ali first foreigner aboard"),
        ("US jury convicts Huawei",
         "Guilty of trade-secret theft and bank fraud"),
        ("China warns of measures on tariffs",
         "Beijing urges dialogue, reserves right to reply"),
        ("Shanghai party chief probed",
         "Chen Jining under anti-graft investigation"),
        ("Indonesia VP Gibran resigns",
         "Steps down amid eligibility questions"),
        ("Bangkok oil-depot blast hurts seven",
         "Four in critical condition after the explosion"),
        ("Joshua Wong jailed for 10 years",
         "Hong Kong activist sentenced for foreign collusion"),
    ],
    "OCEANIA": [
        ("NZ final count could flip government",
         "Official results Friday; four seats in the balance"),
        ("Australia\u2013Fiji security pact in force",
         "Alliance begins after a Pacific diplomacy week"),
        ("Australia green-lights gas reserve",
         "Plan approved despite opposition concerns"),
    ],
}

# Three columns of region blocks, balanced by story count.
COLUMNS = [
    ["EUROPE", "SOUTH AMERICA"],
    ["ASIA", "MIDDLE EAST"],
    ["NORTH AMERICA", "AFRICA", "OCEANIA"],
]

HERO_HEADLINE = "US UNVEILS NEW TARIFFS ON 14 TRADING PARTNERS"
HERO_SUB = ("China 40% \u00b7 Vietnam 35% \u00b7 India 25% \u00b7 EU & Japan hit \u2014 "
            "Beijing warns of counter-measures")

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
_font_cache = {}


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _font_cache:
        if serif:
            name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
        else:
            name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        _font_cache[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _font_cache[key]


def text_w(draw, s, fnt):
    box = draw.textbbox((0, 0), s, font=fnt)
    return box[2] - box[0]


def wrap(draw, s, fnt, max_w):
    """Split s into lines that fit max_w pixels at the given font."""
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(s, n=1):
    """Letter-space a short label with thin gaps between characters."""
    return ("\u2009" * n).join(s)


def draw_price_tag(draw, cx, top, label, pct, colour):
    """A hanging shop-style price tag: string, card, country, rate."""
    card_w, card_h = 118, 64
    x0, y0 = cx - card_w // 2, top + 26
    draw.line([(cx, top), (cx, y0 + 8)], fill=(230, 230, 235), width=2)
    draw.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=8,
                           fill=(250, 248, 240), outline=(30, 34, 48), width=2)
    draw.ellipse([cx - 5, y0 + 4, cx + 5, y0 + 14], outline=(30, 34, 48), width=2)
    f_pct = font(26, bold=True)
    f_lab = font(13, bold=True)
    draw.text((cx - text_w(draw, pct, f_pct) / 2, y0 + 15), pct, font=f_pct, fill=colour)
    draw.text((cx - text_w(draw, label, f_lab) / 2, y0 + 44), label, font=f_lab,
              fill=(52, 58, 74))


def draw_container(draw, x, y, w, h, colour):
    draw.rectangle([x, y, x + w, y + h], fill=colour, outline=(18, 24, 40), width=2)
    # door ribs
    for i in range(1, 6):
        rx = x + (w * i) // 6
        draw.line([(rx, y + 3), (rx, y + h - 3)], fill=(18, 24, 40), width=1)
    draw.rectangle([x + 4, y + 4, x + w - 4, y + 12], outline=(255, 255, 255), width=1)


def draw_hero_scene(draw, box):
    """Flat illustration for the hero panel: a container stack under a crane,
    with three tariff price tags hanging in front."""
    x0, y0, x1, y1 = box
    sea_y = y1 - 26
    # sky and sea bands
    draw.rectangle([x0, y0, x1, sea_y], fill=(38, 62, 102))
    draw.rectangle([x0, sea_y, x1, y1], fill=(22, 44, 78))
    for i in range(6):  # wave ticks
        wx = x0 + 14 + i * 52
        draw.arc([wx, sea_y + 6, wx + 26, sea_y + 18], start=200, end=340,
                 fill=(120, 165, 215), width=2)
    # crane: mast, jib, cable
    mast_x = x0 + 34
    draw.rectangle([mast_x, y0 + 8, mast_x + 10, sea_y], fill=(24, 30, 46))
    draw.rectangle([mast_x, y0 + 8, x1 - 40, y0 + 18], fill=(24, 30, 46))
    draw.line([(mast_x + 5, y0 + 18), (x1 - 60, sea_y - 40)], fill=(24, 30, 46), width=3)
    hook_x = x1 - 84
    draw.line([(hook_x, y0 + 18), (hook_x, y0 + 52)], fill=(24, 30, 46), width=2)
    # stacked containers on a hull
    hull_y = sea_y - 16
    draw.polygon([(x0 + 52, hull_y), (x1 - 30, hull_y), (x1 - 48, sea_y + 8),
                  (x0 + 70, sea_y + 8)], fill=(146, 44, 38), outline=(18, 24, 40))
    cw, ch = 86, 34
    base_y = hull_y - ch
    palette = [(196, 120, 44), (62, 110, 168), (84, 148, 92), (170, 62, 62),
               (110, 84, 160), (46, 140, 150)]
    for row in range(3):
        for col in range(3):
            cx = x0 + 62 + col * (cw + 4)
            cy = base_y - row * (ch + 3)
            draw_container(draw, cx, cy, cw, ch, palette[(row * 3 + col) % len(palette)])
    # the lifted container on the hook
    draw_container(draw, hook_x - cw // 2, y0 + 52, cw, ch, (214, 164, 52))
    # tariff price tags along the front
    tag_y = y0 + 10
    draw_price_tag(draw, x0 + 120, tag_y, "CHINA", "40%", (176, 44, 40))
    draw_price_tag(draw, x0 + 262, tag_y + 6, "VIETNAM", "35%", (176, 44, 40))
    draw_price_tag(draw, x0 + 404, tag_y, "INDIA", "25%", (176, 44, 40))


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 92], fill=PAPER)
    draw.rectangle([0, 92, W, 96], fill=(176, 44, 40))
    f_kicker = font(15, bold=True)
    draw.text((22, 12), spaced("WORLD NEWS IN ONE IMAGE"), font=f_kicker,
              fill=(150, 40, 36))
    f_title = font(40, bold=True, serif=True)
    draw.text((20, 34), "THURSDAY 26 NOVEMBER 2026", font=f_title, fill=PAPER_INK)
    f_meta = font(15, bold=True)
    meta = "45 stories \u00b7 7 regions"
    draw.text((W - 22 - text_w(draw, meta, f_meta), 16), meta, font=f_meta,
              fill=(90, 96, 112))
    meta2 = "one day, one picture"
    draw.text((W - 22 - text_w(draw, meta2, f_meta), 40), meta2, font=f_meta,
              fill=(90, 96, 112))


def draw_hero(draw):
    top, bottom = 106, 310
    draw.rounded_rectangle([14, top, W - 14, bottom], radius=10,
                           fill=(120, 30, 28), outline=(70, 16, 14), width=2)
    scene_box = (24, top + 10, 560, bottom - 10)
    draw_hero_scene(draw, scene_box)
    tx = 584
    f_hero = font(29, bold=True)
    y = top + 20
    for line in wrap(draw, HERO_HEADLINE, f_hero, W - 14 - tx - 14):
        draw.text((tx, y), line, font=f_hero, fill=(252, 244, 230))
        y += 35
    y += 8
    f_sub = font(15)
    for line in wrap(draw, HERO_SUB, f_sub, W - 14 - tx - 14):
        draw.text((tx, y), line, font=f_sub, fill=(244, 214, 200))
        y += 20
    f_tag = font(13, bold=True)
    tag = "TOP STORY \u00b7 ECONOMY"
    tw = text_w(draw, tag, f_tag) + 18
    draw.rounded_rectangle([tx, y + 4, tx + tw, y + 28], radius=6,
                           fill=(252, 244, 230))
    draw.text((tx + 9, y + 9), tag, font=f_tag, fill=(140, 30, 26))


def region_height(draw, name, scale):
    """Pixel height one region block needs at the given type scale."""
    f_head = font(max(11, int(16 * scale)), bold=True)
    f_det = font(max(9, int(12 * scale)))
    inner = COL_W - 20
    total = int(30 * scale) + 6
    for head, det in STORIES[name]:
        total += len(wrap(draw, head, f_head, inner)) * int(19 * scale)
        total += len(wrap(draw, det, f_det, inner)) * int(15 * scale)
        total += int(7 * scale)
    return total + 6


COL_W = (W - 32 - 24) // 3
GRID_TOP, GRID_BOT = 322, 992


def draw_region(draw, name, x, y, scale):
    colour = REGION_COLOURS[name]
    f_head = font(max(11, int(16 * scale)), bold=True)
    f_det = font(max(9, int(12 * scale)))
    f_reg = font(max(12, int(16 * scale)), bold=True)
    h = region_height(draw, name, scale)
    draw.rounded_rectangle([x, y, x + COL_W, y + h], radius=8, fill=PANEL,
                           outline=EDGE, width=1)
    draw.rounded_rectangle([x, y, x + COL_W, y + int(30 * scale)], radius=8,
                           fill=colour)
    draw.rectangle([x, y + int(18 * scale), x + COL_W, y + int(30 * scale)],
                   fill=colour)
    draw.text((x + 10, y + int(6 * scale)), spaced(name), font=f_reg,
              fill=(255, 255, 255))
    count = f"{len(STORIES[name])} stories"
    f_cnt = font(max(9, int(11 * scale)), bold=True)
    draw.text((x + COL_W - 10 - text_w(draw, count, f_cnt), y + int(8 * scale)),
              count, font=f_cnt, fill=(255, 255, 255))
    cy = y + int(30 * scale) + 6
    inner = COL_W - 20
    for i, (head, det) in enumerate(STORIES[name]):
        for line in wrap(draw, head, f_head, inner):
            draw.text((x + 10, cy), line, font=f_head, fill=TEXT)
            cy += int(19 * scale)
        for line in wrap(draw, det, f_det, inner):
            draw.text((x + 10, cy), line, font=f_det, fill=MUTED)
            cy += int(15 * scale)
        cy += int(7 * scale)
        if i < len(STORIES[name]) - 1:
            draw.line([(x + 10, cy - int(4 * scale)), (x + COL_W - 10, cy - int(4 * scale))],
                      fill=(44, 58, 92), width=1)
    return h


def build():
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero(draw)

    # Pick the largest type scale whose three columns all fit the grid.
    avail = GRID_BOT - GRID_TOP
    scale = 1.0
    for cand in (1.0, 0.95, 0.9, 0.85, 0.8):
        ok = True
        for col in COLUMNS:
            need = sum(region_height(draw, n, cand) for n in col) + 12 * (len(col) - 1)
            if need > avail:
                ok = False
                break
        if ok:
            scale = cand
            break
    else:
        scale = 0.8

    for ci, col in enumerate(COLUMNS):
        x = 16 + ci * (COL_W + 12)
        y = GRID_TOP
        for name in col:
            y += draw_region(draw, name, x, y, scale) + 12

    f_foot = font(12)
    foot = ("All 45 stories happened or were first reported on Thursday 26 November 2026 "
            "\u00b7 drawn with Python PIL")
    draw.text(((W - text_w(draw, foot, f_foot)) / 2, 1000), foot, font=f_foot, fill=FAINT)
    return img


if __name__ == "__main__":
    build().save("entry.png", format="PNG", optimize=False)
    print("wrote entry.png")
