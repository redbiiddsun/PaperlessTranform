import pymupdf

class PDFExtractor:
    def __init__(self):
        pass

    def extract_text(self, file_path: str) -> str:
        if not file_path:
            raise ValueError("File path must be provided")

        try:
            doc = pymupdf.open(file_path)

            for page in doc:

                text = page.get_text()

                return text
        except Exception as e:
            raise RuntimeError(f"Error extracting text: {e}")