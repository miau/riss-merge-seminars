import requests
from PyPDF2 import PdfReader, PdfMerger
import os

# 1. 指定 PDF をダウンロード
SRC_URL = "https://www.meti.go.jp/policy/it_policy/jinzai/tokutei_file/koushu_r7/250401_ichiran.pdf"
SRC_FILE = "ichiran.pdf"

print(f"Downloading source PDF: {SRC_URL}")
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    ),
}
resp = requests.get(SRC_URL, headers=headers, timeout=10)
resp.raise_for_status()  # エラー時例外
with open(SRC_FILE, "wb") as f:
    f.write(resp.content)

# 2. PDF 内のリンクから .pdf のみ抽出
reader = PdfReader(SRC_FILE)
pdf_links = set()

for page in reader.pages:
    if "/Annots" in page:
        for annot in page["/Annots"]:
            obj = annot.get_object()
            if "/A" in obj and "/URI" in obj["/A"]:
                uri = obj["/A"]["/URI"]
                if uri.lower().endswith(".pdf"):
                    pdf_links.add(uri)

print(f"Found {len(pdf_links)} PDF links.")

# 3. 各リンク先 PDF をダウンロード
downloaded_files = []
os.makedirs("downloads", exist_ok=True)

for i, url in enumerate(pdf_links, start=1):
    try:
        print(f"Downloading {i}/{len(pdf_links)}: {url}")
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        local_path = os.path.join("downloads", f"file_{i}.pdf")
        with open(local_path, "wb") as f:
            f.write(r.content)
        downloaded_files.append(local_path)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# 4. PDF を結合
if downloaded_files:
    merger = PdfMerger()
    for file in downloaded_files:
        print(f"Adding {file}")
        merger.append(file)
    output_file = "merged.pdf"
    merger.write(output_file)
    merger.close()
    print(f"Merged PDF saved as {output_file}")
else:
    print("No PDFs downloaded, skipping merge.")
