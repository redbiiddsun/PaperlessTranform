import re
import pymupdf

class PDFExtractor:
    def __init__(self):
        pass

    # This function is used to normalize specific dot characters in the text.
    # It replaces the characters: . … · ․ with a standard dot '.'
    # Becasue some PDF files may contain these characters instead of a standard dot.
    # Such as
    # … Unicode ellipsis
    # · middle dot
    # ․ one dot leader
    # Rather than using the standard dot '.'
    def replace_non_standard_dots(self, text):
        return re.sub(r'[…·․]', '.', text)

    def extract_text(self, file_path: str) -> str:
        if not file_path:
            raise ValueError("File path must be provided")

        try:
            doc = pymupdf.open(file_path)

            for page in doc:

                text = page.get_text()

                return self.replace_non_standard_dots(text)
        except Exception as e:
            raise RuntimeError(f"Error extracting text: {e}")
        
    def extract_text(self, file_bytes: bytes) -> str:

        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")

            for page in doc:

                text = page.get_text()

                return self.replace_non_standard_dots(text)
        except Exception as e:
            raise RuntimeError(f"Error extracting text: {e}")