import pytesseract
from PIL import Image
import os


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

# Windows:
# Use the installed Tesseract path if it exists.
windows_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(windows_tesseract):
    pytesseract.pytesseract.tesseract_cmd = windows_tesseract


# ============================================================
# OCR
# ============================================================

def extract_text(image):
    """
    Takes a PIL image and returns the text detected by OCR.
    Works locally and on supported cloud environments.
    """

    if image is None:
        return ""

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    text = pytesseract.image_to_string(image)

    return text