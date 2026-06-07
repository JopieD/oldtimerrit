import xml.etree.ElementTree as ET
import json
import sys
from pathlib import Path
import re

if len(sys.argv) != 2:
    print("Gebruik: python3 gpx_to_json.py <ritnaam>")
    sys.exit(1)

ritnaam = sys.argv[1]

gpx_file = Path("input") / f"{ritnaam}.gpx"
output_dir = Path("ritten") / ritnaam

output_dir.mkdir(parents=True, exist_ok=True)

tree = ET.parse(gpx_file)
root = tree.getroot()

ns = {
    "g": "http://www.topografix.com/GPX/1/1"
}

waypoints = []

for wpt in root.findall(".//g:wpt", ns):

    lat = float(wpt.attrib["lat"])
    lon = float(wpt.attrib["lon"])

    name = wpt.find("g:name", ns).text

    match = re.search(r"_(\d+)$", name)

    nr = int(match.group(1))

    waypoints.append({
        "nr": nr,
        "name": name,
        "lat": lat,
        "lon": lon
    })

waypoints.sort(key=lambda x: x["nr"])

with open(output_dir / "route.json", "w") as f:    
    json.dump(
        waypoints,
        f,
        indent=2
    )

print(f"{len(waypoints)} waypoints opgeslagen")

track = []

for trkpt in root.findall(".//g:trkpt", ns):

    track.append([
        float(trkpt.attrib["lat"]),
        float(trkpt.attrib["lon"])
    ])

with open(output_dir / "track.json", "w") as f:    
    json.dump(
        track,
        f,
        indent=2
    )

print(f"{len(track)} trackpunten opgeslagen")