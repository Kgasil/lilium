"""Rasterize the official lily mark for the Windows executable."""
from pathlib import Path
from PIL import Image, ImageDraw

SCALE = 12
SIZE = 48 * SCALE


def point(p):
    return tuple(round(v * SCALE) for v in p)


def curve(start, *segments):
    result = [start]
    a = start
    for b, c, d in segments:
        for i in range(1, 41):
            t = i / 40
            u = 1 - t
            result.append(tuple(u**3*a[k] + 3*u*u*t*b[k] + 3*u*t*t*c[k] + t**3*d[k] for k in (0, 1)))
        a = d
    return result


def create(path):
    img = Image.new("RGBA", (SIZE, SIZE))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, SIZE-1, SIZE-1), radius=8*SCALE, fill="#23252C")
    paths = [
        curve((24,39), ((22,25),(9,20),(9,8)), ((19,9),(24,17),(24,27)),
              ((24,17),(29,9),(39,8)), ((39,20),(26,25),(24,39))),
        [(24,39),(24,13)],
        curve((24,39), ((17,39),(11,34),(9,28))),
        curve((24,39), ((31,39),(37,34),(39,28))),
    ]
    for line in paths:
        draw.line([point(p) for p in line], fill="#E78CB1", width=round(1.8*SCALE), joint="curve")
    draw.ellipse((*point((21.4,8.4)),*point((26.6,13.6))), fill="#E8BA53")
    img = img.resize((256,256), Image.Resampling.LANCZOS)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="ICO", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])


if __name__ == "__main__":
    create(Path(__file__).resolve().parent.parent / "build" / "lilium.ico")
