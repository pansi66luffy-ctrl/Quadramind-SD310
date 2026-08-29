import pytesseract
from PIL import Image


# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image):
    """
    Takes an image and returns the text detected by OCR.
    """

    text = pytesseract.image_to_string(image)

    return text
