"""Genera el ícono de la aplicación (assets/icon.ico y assets/icon.png).

Diseño: cuadrado redondeado en verde azulado (teal) con una burbuja de
diálogo blanca y la inicial "M" — evoca comunicación/lenguaje, el dominio de
la app. Reproducible: correr `python tools/generate_icon.py`.
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = 512
TEAL = (13, 148, 136, 255)      # fondo
TEAL_DARK = (15, 118, 110, 255)  # borde inferior sutil
WHITE = (255, 255, 255, 255)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")


def _rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def _load_font(size):
    for name in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build():
    img = Image.new("RGBA", (BASE, BASE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fondo redondeado
    margin = 24
    _rounded(draw, (margin, margin, BASE - margin, BASE - margin), 96, TEAL)

    # Burbuja de diálogo blanca
    bx0, by0, bx1, by1 = 120, 110, 392, 330
    _rounded(draw, (bx0, by0, bx1, by1), 56, WHITE)
    # Cola de la burbuja
    draw.polygon([(180, 320), (150, 400), (250, 330)], fill=WHITE)

    # Letra "M" en teal centrada en la burbuja
    font = _load_font(180)
    text = "M"
    tb = draw.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    cx = (bx0 + bx1) / 2 - tw / 2 - tb[0]
    cy = (by0 + by1) / 2 - th / 2 - tb[1]
    draw.text((cx, cy), text, font=font, fill=TEAL_DARK)

    os.makedirs(ASSETS, exist_ok=True)
    png_path = os.path.join(ASSETS, "icon.png")
    ico_path = os.path.join(ASSETS, "icon.ico")
    img.save(png_path)
    img.save(
        ico_path,
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Generado: {png_path}")
    print(f"Generado: {ico_path}")


if __name__ == "__main__":
    build()
