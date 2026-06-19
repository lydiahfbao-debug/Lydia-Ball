# Rendering a deck for visual review

python-pptx writes `.pptx` but cannot render slides to images. To visually
verify layout, convert with LibreOffice (headless), then read the PNGs.

## Convert to PDF

```bash
soffice --headless --convert-to pdf --outdir /tmp out.pptx
# or: libreoffice --headless --convert-to pdf --outdir /tmp out.pptx
```

## Convert to per-slide PNGs

```bash
# First to PDF, then PDF -> PNG with pdftoppm (poppler) at 150 DPI
soffice --headless --convert-to pdf --outdir /tmp out.pptx
pdftoppm -png -r 150 /tmp/out.pdf /tmp/slide
# produces /tmp/slide-1.png, /tmp/slide-2.png, ...
```

Then use the Read tool on a PNG to inspect it visually and catch overflow,
misalignment, or contrast problems.

## If LibreOffice is unavailable

```bash
which soffice libreoffice || sudo apt-get install -y libreoffice poppler-utils
```

If it cannot be installed, fall back to a structural check: open the deck with
python-pptx and print each slide's title, shape count, and bounding boxes to
catch off-canvas or overlapping shapes.

```python
from pptx import Presentation
prs = Presentation("out.pptx")
for i, s in enumerate(prs.slides, 1):
    titles = [sh.text for sh in s.shapes if sh.has_text_frame and sh.text][:1]
    print(i, titles, f"{len(s.shapes)} shapes")
```
