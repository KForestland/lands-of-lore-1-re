"""Draw the original My Game icon and startup panel for the Windows package."""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def draw_icon():
    image = Image.new("RGBA", (256, 256))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 247, 247), radius=49, fill="#193a37")
    draw.polygon(((51, 88), (101, 70), (155, 88), (205, 70), (205, 168),
                  (155, 186), (101, 168), (51, 186)), fill="#f3e5be")
    draw.line(((101, 70), (101, 168)), fill="#b7a778", width=5)
    draw.line(((155, 88), (155, 186)), fill="#b7a778", width=5)
    draw.line(((71, 147), (94, 135), (121, 146), (153, 131), (182, 119)),
              fill="#1b6256", width=9, joint="curve")
    draw.ellipse((172, 108, 194, 130), fill="#b4652f")
    return image


def font(name, size):
    windows = Path(os.environ.get("WINDIR", "C:/Windows"))
    try:
        return ImageFont.truetype(str(windows / "Fonts" / name), size)
    except OSError:
        return ImageFont.load_default(size=size)


def main():
    folder = Path("build/mygame-art")
    folder.mkdir(parents=True, exist_ok=True)
    icon = draw_icon()
    icon.save(folder / "mygame.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (256, 256)])

    splash = Image.new("RGB", (360, 112), "#fbf5e5")
    draw = ImageDraw.Draw(splash)
    draw.rectangle((0, 0, 359, 111), outline="#193a37", width=3)
    small = icon.resize((64, 64), Image.Resampling.LANCZOS)
    splash.paste(small, (23, 24), small)
    draw.text((104, 26), "Lands of Lore: My Game", font=font("segoeuib.ttf", 20), fill="#193a37")
    draw.text((104, 57), "Starting...", font=font("segoeui.ttf", 16), fill="#2a4c46")
    splash.save(folder / "starting.png")


if __name__ == "__main__":
    main()
