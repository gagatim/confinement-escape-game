import os, sys
from PIL import Image, ImageDraw, ImageOps, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')

CARDS_DIR = "images/cards"
AVATARS_DIR = "images/avatars"
os.makedirs(CARDS_DIR, exist_ok=True)
os.makedirs(AVATARS_DIR, exist_ok=True)

def create_rounded_avatar(img, size=(512, 512), radius=72, border_color=(76, 214, 224, 220), border_width=5):
    """Takes an image, resizes/crops to square size, applies rounded corners and glowing border."""
    # Resize and crop to square
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    img_square = img.crop((left, top, left + min_dim, top + min_dim)).resize(size, Image.Resampling.LANCZOS).convert("RGBA")

    # Create mask for rounded corners
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size[0]-1, size[1]-1)], radius=radius, fill=255)

    # Apply mask
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(img_square, (0, 0), mask=mask)

    # Draw border
    draw_out = ImageDraw.Draw(out)
    draw_out.rounded_rectangle(
        [(border_width//2, border_width//2), (size[0]-1-border_width//2, size[1]-1-border_width//2)],
        radius=radius,
        outline=border_color,
        width=border_width
    )
    return out

# 1. Process Physical 16 from ca5a7ac7 and 0d82f530
img1 = Image.open('ca5a7ac7-72a3-4032-aeb2-e8b88a8e28cc.png') # 1254 x 1254
img2 = Image.open('0d82f530-ac88-4891-a83e-090f549a7c90.png') # 1254 x 1254

cw1, ch1 = img1.size[0] / 4.0, img1.size[1] / 2.0
cw2, ch2 = img2.size[0] / 4.0, img2.size[1] / 2.0

phys_grid1 = [
    [("shopper", "購物大媽", 160), ("climber", "攀岩者", 140), ("detective", "私家偵探", 150), ("geneFreak", "基因怪人", 150)],
    [("embalmer", "入殮師", 160), ("exorcist", "還魂師", 160), ("mediocre", "庸才", 160), ("lucky", "幸運兒", 150)]
]

phys_grid2 = [
    [("merc", "雇傭兵", 140), ("butcher", "屠夫", 150), ("vampire", "吸血鬼", 150), ("bomb", "橡膠人", 140)],
    [("tamer", "馴獸師", 140), ("bartender", "飲品師", 150), ("scavenger", "拾荒者", 140), ("engineer", "工程師", 140)]
]

print("Processing Physical 16 characters...")
for r, row in enumerate(phys_grid1):
    for c, (prof_id, name, y_offset) in enumerate(row):
        # Card crop
        x0, y0 = int(c * cw1), int(r * ch1)
        x1, y1 = int((c + 1) * cw1), int((r + 1) * ch1)
        card = img1.crop((x0, y0, x1, y1))
        card.save(f"{CARDS_DIR}/{prof_id}.png")

        # Avatar crop (focused on head & torso)
        margin = int(cw1 * 0.08)
        av_w = int(cw1 - margin * 2)
        av_crop = img1.crop((x0 + margin, y0 + y_offset, x1 - margin, y0 + y_offset + av_w))
        av = create_rounded_avatar(av_crop)
        av.save(f"{AVATARS_DIR}/{prof_id}.webp", quality=88, method=6)
        print(f"  Saved {name} ({prof_id})")

for r, row in enumerate(phys_grid2):
    for c, (prof_id, name, y_offset) in enumerate(row):
        # Card crop
        x0, y0 = int(c * cw2), int(r * ch2)
        x1, y1 = int((c + 1) * cw2), int((r + 1) * ch2)
        card = img2.crop((x0, y0, x1, y1))
        card.save(f"{CARDS_DIR}/{prof_id}.png")

        # Avatar crop
        margin = int(cw2 * 0.08)
        av_w = int(cw2 - margin * 2)
        av_crop = img2.crop((x0 + margin, y0 + y_offset, x1 - margin, y0 + y_offset + av_w))
        av = create_rounded_avatar(av_crop)
        av.save(f"{AVATARS_DIR}/{prof_id}.webp", quality=88, method=6)
        print(f"  Saved {name} ({prof_id})")

# 2. Process Classic Expansion Roles from aa205b77-8e49-4a00-8d91-5d756831caec.png (1024 x 1536)
img_classic = Image.open('禁閉逃殺圖片/aa205b77-8e49-4a00-8d91-5d756831caec.png')
cw_c, ch_c = img_classic.size[0] / 4.0, img_classic.size[1] / 4.0

classic_roles = {
    "fatty": ("肥宅", 0, 0, 70),
    "gambler": ("賭徒", 0, 2, 70),
    "trucker": ("貨車司機", 1, 0, 70),
    "chemist": ("化學家", 1, 2, 70),
    "hacker": ("黑客", 2, 0, 70),
    "tycoon": ("富豪", 2, 1, 70),
    "shade": ("暗影使者", 2, 2, 70),
    "outsider": ("邊緣人", 3, 2, 70)
}

print("\nProcessing Classic Expansion characters...")
for prof_id, (name, r, c, y_off) in classic_roles.items():
    x0, y0 = int(c * cw_c), int(r * ch_c)
    x1, y1 = int((c + 1) * cw_c), int((r + 1) * ch_c)
    card = img_classic.crop((x0, y0, x1, y1))
    if not os.path.exists(f"{CARDS_DIR}/{prof_id}.png"):
        card.save(f"{CARDS_DIR}/{prof_id}.png")

    margin = int(cw_c * 0.08)
    av_w = int(cw_c - margin * 2)
    av_crop = img_classic.crop((x0 + margin, y0 + y_off, x1 - margin, y0 + y_off + av_w))
    av = create_rounded_avatar(av_crop, border_color=(255, 180, 50, 220))
    av.save(f"{AVATARS_DIR}/{prof_id}.webp", quality=88, method=6)
    print(f"  Saved {name} ({prof_id})")

# 3. Process Newly AI-Generated Chibi Characters from images/characters/
ai_generated = {
    "sniper": ("狙擊手", "images/characters/sniper.jpg", 120),
    "sentinel": ("哨兵", "images/characters/sentinel.jpg", 100),
    "cardsharp": ("老千", "images/characters/cardsharp.jpg", 140),
    "janitor": ("清潔工", "images/characters/janitor.jpg", 100),
    "berserker": ("狂戰士", "images/characters/berserker.jpg", 120),
    "clerk": ("倉管員", "images/characters/clerk.jpg", 120),
}

print("\nProcessing AI-Generated characters...")
for prof_id, (name, fpath, top_offset) in ai_generated.items():
    if os.path.exists(fpath):
        src_img = Image.open(fpath)
        src_img.save(f"{CARDS_DIR}/{prof_id}.png")
        # Crop head & torso
        w, h = src_img.size
        side = int(w * 0.8)
        left = int(w * 0.1)
        top = top_offset
        av_crop = src_img.crop((left, top, left + side, top + side))
        av = create_rounded_avatar(av_crop, border_color=(76, 214, 224, 240))
        av.save(f"{AVATARS_DIR}/{prof_id}.webp", quality=88, method=6)
        print(f"  Saved {name} ({prof_id})")

# 4. StockCake mappings for remaining roles
stock_roles = {
    "courier": ("郵差", "新增資料夾 (5)/StockCake-Rushing_Anime_Courier-2212170-standard.png", 50, 700)
}

print("\nProcessing StockCake characters...")
for prof_id, (name, fpath, top, side) in stock_roles.items():
    if os.path.exists(fpath):
        src_img = Image.open(fpath)
        src_img.save(f"{CARDS_DIR}/{prof_id}.png")
        w, h = src_img.size
        left = (w - side) // 2
        av_crop = src_img.crop((left, top, left + side, top + side))
        av = create_rounded_avatar(av_crop, border_color=(255, 206, 107, 240))
        av.save(f"{AVATARS_DIR}/{prof_id}.webp", quality=88, method=6)
        print(f"  Saved {name} ({prof_id})")

# 5. Q版 sheet (2 rows x 4 cols, 1536 x 1024): expansion roles, name banner at the bottom of each cell
q_sheet = Image.open('職業Q版圖片未條整/職業Q版圖片.png')
qw, qh = q_sheet.size[0] // 4, q_sheet.size[1] // 2
q_roles = [
    ("warden", "看守長"), ("paramedic", "急救員"), ("mole", "地鼠"), ("lobbyist", "說客"),
    ("medic", "醫官"), ("leader", "團長"), ("scout", "偵察兵"), ("bountyhunter", "賞金獵人"),
]
print("\nProcessing Q-version sheet characters...")
for i, (prof_id, name) in enumerate(q_roles):
    x0, y0 = (i % 4) * qw, (i // 4) * qh
    card = q_sheet.crop((x0, y0, x0 + qw, y0 + 410))  # above the name banner
    card.save(f"{CARDS_DIR}/{prof_id}.png")
    av = create_rounded_avatar(q_sheet.crop((x0, y0, x0 + qw, y0 + qw)), border_color=(255, 206, 107, 240))
    av.save(f"{AVATARS_DIR}/{prof_id}.webp", quality=88, method=6)
    print(f"  Saved {name} ({prof_id})")

# 6. Q版 sheets (1024 x 559, 4 x 2 characters each): general / special roles. Boxes are hand-placed
# (cx, top) squares of SZ px around each head+torso so the printed labels stay out of frame.
SZ = 165
Q_DIR = '職業Q版圖片未條整'
Q_SHEETS = {  # filename prefix -> {prof_id: (cx, top)}
    "飛行員": {"pilot": (158, 68), "demolitions": (402, 68), "chef": (645, 68), "smuggler": (887, 68),
             "survivor": (180, 300), "runner": (415, 300), "herbalist": (655, 300), "veteran": (885, 300)},
    "神偷": {"pickpocket": (155, 68), "diver": (405, 68), "gourmet": (645, 68), "farmer": (870, 68),
           "miner": (185, 300), "hunter": (420, 300), "boss": (655, 300), "collector": (885, 300)},
    "守護者": {"guardian": (150, 68), "hermit": (395, 68), "prepper": (640, 68), "witch": (870, 68),
             "toxic": (180, 300)},
    "毒域": {"oracle": (162, 68), "arsonist": (415, 68), "assassin": (665, 68), "bodyguard": (890, 68),
           "suzhenchang": (182, 300), "jiangwanan": (410, 300), "shenboyang": (655, 300), "laiqingde": (885, 290)},
}
print("\nProcessing Q-version general/special sheets...")
for fname in sorted(os.listdir(Q_DIR)):
    key = next((k for k in Q_SHEETS if fname.startswith(k)), None)
    if not key:
        continue
    sheet = Image.open(f"{Q_DIR}/{fname}").convert("RGB")
    for prof_id, (cx, top) in Q_SHEETS[key].items():
        box = (cx - SZ // 2, top, cx + SZ // 2, top + SZ)
        crop = sheet.crop(box).resize((512, 512), Image.Resampling.LANCZOS)
        crop.save(f"{CARDS_DIR}/{prof_id}.png")
        create_rounded_avatar(crop, border_color=(255, 206, 107, 240)).save(f"{AVATARS_DIR}/{prof_id}.webp", quality=88, method=6)
        print(f"  Saved {prof_id}")

print("\nAll avatars and cards generated successfully!")
