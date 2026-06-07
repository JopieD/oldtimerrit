import pdfplumber
import re
import json

waypoints = []

with pdfplumber.open("DGR 2026-1.pdf") as pdf:

    for page in pdf.pages:

        words = page.extract_words()

        current_wp = None

        for word in words:

            text = word["text"]

            # waypointnummer
            if re.fullmatch(r"\d{1,2}", text):

                nr = int(text)

                if 1 <= nr <= 99:

                    current_wp = {
                        "nr": nr,
                        "top": word["top"]
                    }

            # latitude
            elif current_wp and "°" in text and text.endswith("N"):

                current_wp["lat_raw"] = text

            # longitude
            elif current_wp and "°" in text and text.endswith("E"):

                current_wp["lon_raw"] = text

                waypoints.append(current_wp)
                current_wp = None

def convert(coord):

    m = re.match(
        r"(\d+)°(\d+\.\d+)'([NSEW])",
        coord
    )

    deg = float(m.group(1))
    mins = float(m.group(2))
    hemi = m.group(3)

    value = deg + mins / 60

    if hemi in ["S", "W"]:
        value *= -1

    return round(value, 6)

result = []

for wp in waypoints:

    result.append({
        "nr": wp["nr"],
        "lat": convert(wp["lat_raw"]),
        "lon": convert(wp["lon_raw"])
    })

with open("route.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"{len(result)} waypoints gevonden")