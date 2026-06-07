import re
import json
import pdfplumber

PDF_FILE = "DGR 2026-1.pdf"


def clean_info(info):
    info = info.strip()

    # Alleen een afstand? Dan is het geen info.
    if re.match(r"^\d+,\d+$", info):
        return ""

    return info


roadbook = []

with pdfplumber.open(PDF_FILE) as pdf:

    for page_num, page in enumerate(pdf.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            # Zoek regels die beginnen met:
            # 0,05 0,05
            # 6,61 2,46 Ensinkgoorsdijk 34,53
            # etc.

            m = re.match(
                r"^(\d+,\d+)\s+(\d+,\d+)(.*)",
                line
            )

            if not m:
                continue

            total = float(
                m.group(1).replace(",", ".")
            )

            partial = float(
                m.group(2).replace(",", ".")
            )

            rest = m.group(3).strip()

            info = ""

            # Verwijder laatste regress-afstand
            # Voorbeeld:
            # "Ensinkgoorsdijk 34,53"
            # -> "Ensinkgoorsdijk"

            m2 = re.match(
                r"^(.*?)\s+(\d+,\d+)$",
                rest
            )

            if m2:
                info = m2.group(1).strip()
            else:
                info = rest

            info = clean_info(info)

            nr = len(roadbook) + 1
            
            roadbook.append({
                "nr": len(roadbook) + 1,
                "total": total,
                "partial": partial,
                "info": info,
			    "symbol": f"{nr:03d}.png"
            })

print(f"{len(roadbook)} records gevonden")

with open(
    "roadbook.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        roadbook,
        f,
        indent=2,
        ensure_ascii=False
    )

print("roadbook.json geschreven")