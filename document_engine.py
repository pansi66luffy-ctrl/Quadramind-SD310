from pypdf import PdfReader
from docx import Document


def extract_document_text(uploaded_file):
    """
    Extract text from PDF, DOCX, or TXT files.
    Returns the extracted text as a string.
    """

    file_name = uploaded_file.name.lower()

    # --------------------------------------------------
    # PDF
    # --------------------------------------------------

    if file_name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text


    # --------------------------------------------------
    # DOCX
    # --------------------------------------------------

    elif file_name.endswith(".docx"):

        document = Document(uploaded_file)

        text = ""

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

        return text


    # --------------------------------------------------
    # TXT
    # --------------------------------------------------

    elif file_name.endswith(".txt"):

        return uploaded_file.getvalue().decode(
            "utf-8",
            errors="ignore"
        )


    # --------------------------------------------------
    # Unsupported
    # --------------------------------------------------

    else:

        raise ValueError(
            "Unsupported document type."
        )