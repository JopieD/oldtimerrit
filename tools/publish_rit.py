import sys
import shutil
import subprocess
from pathlib import Path

if len(sys.argv) != 2:
    print("Gebruik: python3 tools/publish_rit.py <ritnaam>")
    sys.exit(1)

ritnaam = sys.argv[1]

gpx_file = Path("input") / f"{ritnaam}.gpx"
pdf_file = Path("input") / f"{ritnaam}.pdf"

if not gpx_file.exists():
    print(f"FOUT: {gpx_file} niet gevonden")
    sys.exit(1)

if not pdf_file.exists():
    print(f"FOUT: {pdf_file} niet gevonden")
    sys.exit(1)

rit_dir = Path("ritten") / ritnaam

print(f"\nPubliceren van rit: {ritnaam}")

#
# Oude rit verwijderen
#
if rit_dir.exists():
    print("Bestaande rit verwijderen...")
    shutil.rmtree(rit_dir)

#
# Nieuwe ritmap
#
rit_dir.mkdir(parents=True)

#
# Templates kopiëren
#
print("Templates kopiëren...")

shutil.copy(
    "templates/index.html",
    rit_dir / "index.html"
)

shutil.copytree(
    "templates/css",
    rit_dir / "css"
)

shutil.copytree(
    "templates/js",
    rit_dir / "js"
)

#
# GPX verwerken
#
print("GPX verwerken...")

subprocess.run(
    ["python3", "tools/gpx_to_json.py", ritnaam],
    check=True
)

#
# Roadbook verwerken
#
print("Roadbook verwerken...")

subprocess.run(
    ["python3", "tools/roadbook_import.py", ritnaam],
    check=True
)

#
# Symbolen genereren
#
print("Symbolen genereren...")

subprocess.run(
    ["python3", "tools/extract_symbols.py", ritnaam],
    check=True
)

#
# Controle
#
required = [
    "index.html",
    "route.json",
    "track.json",
    "roadbook.json",
    "css",
    "js",
    "symbols"
]

missing = []

for item in required:

    if not (rit_dir / item).exists():
        missing.append(item)

if missing:

    print("\nFOUT: ontbrekende bestanden:")
    for item in missing:
        print(f" - {item}")

    sys.exit(1)

print("\n===================================")
print(f"Rit {ritnaam} succesvol gepubliceerd")
print(f"Locatie: {rit_dir}")
print("===================================\n")