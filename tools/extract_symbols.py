from pathlib import Path
import fitz
from PIL import Image
import re

PDF_FILE = "DGR 2026-1.pdf"

OUTDIR = Path("symbols")
OUTDIR.mkdir(exist_ok=True)

# Rally Navigator symbol extraction
#
# Definitief afgestemd op DGR 2026-1 PDF
#
# DIRECTION kolom
#
LEFT_PDF = 85
RIGHT_PDF = 220

#
# Verticale correctie
#
VERTICAL_OFFSET_PDF = 30
BOTTOM_EXTRA_PDF = 1

doc = fitz.open(PDF_FILE)

symbol_nr = 1

for page_index in range(1, len(doc) - 1):

    page = doc[page_index]

    pix = page.get_pixmap(
        matrix=fitz.Matrix(3, 3),
        alpha=False
    )

    img = Image.frombytes(
        "RGB",
        (pix.width, pix.height),
        pix.samples
    )

    scale_x = img.width / page.rect.width
    scale_y = img.height / page.rect.height

    print("\n" + "=" * 60)
    print(f"PAGE {page_index + 1}")
    print(f"PDF size : {page.rect.width:.2f} x {page.rect.height:.2f}")
    print(f"IMG size : {img.width} x {img.height}")
    print(f"Scale    : x={scale_x:.3f} y={scale_y:.3f}")

    #
    # Waypoints zoeken
    #
    wps = []

    for block in page.get_text("blocks"):

        txt = block[4].strip()

        if not re.fullmatch(r"\d+", txt):
            continue

        nr = int(txt)

        if not (1 <= nr <= 47):
            continue

        x = block[0]

        #
        # Echte waypointnummers
        #
        if not (90 <= x <= 105):
            continue

        wps.append({
            "nr": nr,
            "y": block[1]
        })

    #
    # Dubbele verwijderen
    #
    seen = set()
    clean_wps = []

    for wp in wps:

        if wp["nr"] in seen:
            continue

        seen.add(wp["nr"])
        clean_wps.append(wp)

    wps = sorted(
        clean_wps,
        key=lambda x: x["y"]
    )

    print(f"Waypoints gevonden: {len(wps)}")
    print(wps)

    if not wps:
        continue

    for i, wp in enumerate(wps):

        current_y = wp["y"]

        #
        # Celhoogte bepalen
        #
        if len(wps) == 1:

            half_height = 45

        elif i == 0:

            half_height = (
                wps[i + 1]["y"] - current_y
            ) / 2

        elif i == len(wps) - 1:

            half_height = (
                current_y - wps[i - 1]["y"]
            ) / 2

        else:

            half_height = min(
                current_y - wps[i - 1]["y"],
                wps[i + 1]["y"] - current_y
            ) / 2

        #
        # PDF coordinaten
        #
        y1_pdf = (
            current_y
            - half_height
            - VERTICAL_OFFSET_PDF
        )

        y2_pdf = (
            current_y
            + half_height
            - VERTICAL_OFFSET_PDF
            + BOTTOM_EXTRA_PDF
        )

        #
        # Pixel coordinaten
        #
        x1 = int(LEFT_PDF * scale_x)
        x2 = int(RIGHT_PDF * scale_x)

        y1 = int(y1_pdf * scale_y)
        y2 = int(y2_pdf * scale_y)

        #
        # Grenzen bewaken
        #
        y1 = max(0, y1)
        y2 = min(img.height, y2)

        if x2 <= x1:
            print(f"SKIP WP {wp['nr']} (x)")
            continue

        if y2 <= y1:
            print(f"SKIP WP {wp['nr']} (y)")
            continue

        print(
            f"WP {wp['nr']:2d} | "
            f"LEFT_PDF={LEFT_PDF} "
            f"RIGHT_PDF={RIGHT_PDF} | "
            f"x1={x1} "
            f"x2={x2} | "
            f"width={x2-x1}"
        )

        print(
            f"         "
            f"y_pdf={current_y:.2f} | "
            f"y1={y1} "
            f"y2={y2} | "
            f"height={y2-y1}"
        )

        crop = img.crop(
            (x1, y1, x2, y2)
        )

        filename = OUTDIR / f"{symbol_nr:03d}.png"

        crop.save(filename)

        print(f"         -> {filename}")

        symbol_nr += 1

print(f"\nKlaar. {symbol_nr - 1} symbolen opgeslagen.")