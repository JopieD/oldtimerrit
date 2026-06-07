import fitz

doc = fitz.open("DGR 2026-1.pdf")
page = doc[2]

for block in page.get_text("dict")["blocks"]:

    if "lines" not in block:
        continue

    print("\nBLOCK")

    for line in block["lines"]:
        txt = ""

        for span in line["spans"]:
            txt += span["text"]

        print(txt)

    print("bbox =", block["bbox"])