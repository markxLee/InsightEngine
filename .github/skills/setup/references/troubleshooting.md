# Troubleshooting — InsightEngine Installation

Common errors and fixes when setting up InsightEngine dependencies.

---

## Python Issues

### Python version too old

```
Error: Python 3.8 detected. InsightEngine requires Python >= 3.10.
```

**Fix (macOS):**
```bash
brew install python@3.12
# Then use python3.12 or update your PATH
```

**Fix (Linux):**
```bash
sudo apt update && sudo apt install python3.12 python3.12-venv
```

---

### pip install fails with PermissionError

```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Fix:** Always use `--user` flag (InsightEngine does not require system-wide install):
```bash
pip3 install --user -r requirements.txt
```

If `--user` also fails, check that `~/.local/lib/python3.x/site-packages/` exists and is writable.

---

### pip install fails with "externally-managed-environment"

```
error: externally-managed-environment
× This environment is externally managed
```

This happens on newer macOS/Linux systems with PEP 668.

**Fix:** Use `--user` flag or `--break-system-packages`:
```bash
pip3 install --user -r requirements.txt
# Or if --user doesn't work:
pip3 install --break-system-packages -r requirements.txt
```

---

### Package version conflict

```
ERROR: pip's dependency resolver found conflicting dependencies
```

**Fix:** Install packages one at a time to isolate the conflict:
```bash
pip3 install --user markitdown[all]
pip3 install --user python-docx openpyxl pandas
pip3 install --user reportlab pypdf pdfplumber
pip3 install --user matplotlib seaborn jinja2
pip3 install --user httpx beautifulsoup4
```

---

## markitdown Issues

### markitdown returns empty/garbled output

Some file types (especially scanned PDFs or complex PPTX) can produce garbled output.

**Fix:** The thu-thap skill automatically falls back to format-specific readers. If you're
calling markitdown directly:
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("file.pdf")
if len(result.text_content) < 100:
    # Use pdfplumber as fallback
    import pdfplumber
    with pdfplumber.open("file.pdf") as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
```

---

### markitdown[all] fails to install

Some sub-dependencies (like `python-pptx`) may fail on certain systems.

**Fix:** Install markitdown without extras, then add what you need:
```bash
pip3 install --user markitdown
pip3 install --user python-pptx pdfplumber openpyxl
```

---

## Node.js / pptxgenjs Issues

### pptxgenjs not found

```
Error: Cannot find module 'pptxgenjs'
```

**Fix:**
```bash
npm install -g pptxgenjs
# Verify:
node -e "require('pptxgenjs'); console.log('OK')"
```

If `npm install -g` fails with permissions:
```bash
# macOS
sudo npm install -g pptxgenjs
# Or use npx (no global install needed):
npx pptxgenjs
```

---

### Node.js not installed

```
zsh: command not found: node
```

**Fix (macOS):**
```bash
brew install node
```

**Fix (Linux):**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## reportlab / Font Issues

### Vietnamese characters render as boxes in PDF

The font used doesn't support Vietnamese glyphs.

**Fix:** Register a Unicode-capable font:
```python
# Try system fonts first (macOS)
import os
system_fonts = "/System/Library/Fonts/Supplemental/"
if os.path.exists(system_fonts + "Arial Unicode.ttf"):
    pdfmetrics.registerFont(TTFont('ArialUnicode', system_fonts + 'Arial Unicode.ttf'))

# Fallback: DejaVu Sans (bundled with many systems)
# Usually at /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
```

---

## matplotlib Issues

### "No display name and no $DISPLAY environment variable"

matplotlib tries to open a GUI window in a headless environment.

**Fix:** Set Agg backend BEFORE importing pyplot:
```python
import matplotlib
matplotlib.use('Agg')  # MUST be before any other matplotlib import
import matplotlib.pyplot as plt
```

This is already enforced in InsightEngine's tao-hinh skill, but if you write custom scripts,
always include this line.

---

## Apple Silicon (M1/M2/M3) Issues

### torch/diffusers installation fails

```
ERROR: No matching distribution found for torch
```

**Fix:** Use the PyTorch Apple Silicon wheels:
```bash
pip3 install --user torch torchvision torchaudio
pip3 install --user diffusers transformers accelerate
```

If you get memory errors during installation, close other apps to free RAM.

### MPS (Metal) not available

```
RuntimeError: MPS backend is not available
```

**Fix:** Requires macOS 12.3+ and PyTorch 2.0+. Check:
```python
import torch
print(torch.backends.mps.is_available())  # Should be True
print(torch.backends.mps.is_built())      # Should be True
```

If `is_built()` is False, reinstall PyTorch. If `is_available()` is False, update macOS.

---

## General Tips

1. **Always check first:** Run `python3 scripts/check_deps.py` before installing anything
2. **Use requirements.txt:** `pip3 install --user -r requirements.txt` installs correct versions
3. **Don't use sudo pip:** This can break system Python. Always use `--user`
4. **Virtual env alternative:** If `--user` causes issues:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
