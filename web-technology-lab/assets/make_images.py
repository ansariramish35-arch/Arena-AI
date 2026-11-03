"""Generate the sample images used by Practicals 4, 5 and 6."""
from PIL import Image, ImageDraw

OUT = "/home/user/Arena-AI/web-technology-lab/programs"

# ---- campus-map.jpg : labelled blocks used by image-map practicals ----
img = Image.new("RGB", (600, 400), "#e8f0e4")
d = ImageDraw.Draw(img)
d.rectangle([0, 0, 599, 399], outline="#2e5d2e", width=3)
d.text((180, 8), "CAMPUS MAP", fill="#1f3864")

blocks = [
    ("Library",    (20, 40, 180, 160),  "#ffd966"),
    ("Computer Labs", (200, 40, 380, 160), "#9fc5e8"),
    ("Canteen",    (400, 40, 580, 160),  "#f6b26b"),
    ("Auditorium", (20, 180, 290, 300), "#c27ba0"),
    ("Sports Ground", (310, 180, 580, 300), "#93c47d"),
    ("Parking",    (20, 320, 580, 380),  "#cccccc"),
]
for label, box, color in blocks:
    d.rectangle(box, fill=color, outline="#333333", width=2)
    cx = (box[0] + box[2]) // 2
    cy = (box[1] + box[3]) // 2
    w = d.textlength(label)
    d.text((cx - w / 2, cy - 6), label, fill="#000000")

img.save(f"{OUT}/p04-image-map/campus-map.jpg", quality=90)
img.save(f"{OUT}/p05-hotspots/campus-map.jpg", quality=90)

# ---- lab-map.jpg : gridded image for the JavaScript coordinates demo ----
img2 = Image.new("RGB", (500, 350), "#ffffff")
d2 = ImageDraw.Draw(img2)
for x in range(0, 501, 50):
    d2.line([(x, 0), (x, 350)], fill="#bbbbbb", width=1)
    d2.text((x + 2, 332), str(x), fill="#666666")
for y in range(0, 351, 50):
    d2.line([(0, y), (500, y)], fill="#bbbbbb", width=1)
    d2.text((4, y + 2), str(y), fill="#666666")
d2.rectangle([0, 0, 499, 349], outline="#1f3864", width=2)
d2.text((150, 12), "Click anywhere on this map", fill="#1f3864")
img2.save(f"{OUT}/p06-image-coordinates/lab-map.jpg", quality=90)

# ---- photo.jpg : placeholder photo for the resume ----
img3 = Image.new("RGB", (110, 130), "#d9d9d9")
d3 = ImageDraw.Draw(img3)
d3.rectangle([0, 0, 109, 129], outline="#808080")
d3.text((28, 60), "PHOTO", fill="#595959")
img3.save(f"{OUT}/p01-resume-table/photo.jpg", quality=90)

print("images created")
