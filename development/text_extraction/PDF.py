import re
import pymupdf

class PDFExtractor:
    def __init__(self):
        pass

    # This function is used to normalize specific dot characters in the text.
    # It replaces the characters: . … · ․ with a standard dot '.'
    # Because some PDF files may contain these characters instead of a standard dot.
    # Such as
    # … Unicode ellipsis
    # · middle dot
    # ․ one dot leader
    # Rather than using the standard dot '.'
    def replace_non_standard_dots(self, text):
        return re.sub(r'[…·․]', '.', text)

    def extract_text_with_position(self, file_path: str) -> list:
        if not file_path:
            raise ValueError("File path must be provided")

        try:
            doc = pymupdf.open(file_path)
            words_with_positions = []

            for page in doc:
                # Get the text with position information as a dictionary
                page_text = page.get_text("dict")
                
                # Iterate through each block of text
                for block in page_text["blocks"]:
                    if block['type'] == 0:  # Only process text blocks
                        for line in block["lines"]:
                            for span in line["spans"]:
                                # Get the word and its position (x, y)
                                word = span['text']
                                x = span['bbox'][0]  # x-coordinate of the word's bounding box
                                y = span['bbox'][1]  # y-coordinate of the word's bounding box
                                # Normalize the word and add it to the list with its position
                                normalized_word = self.replace_non_standard_dots(word)
                                words_with_positions.append({"word": normalized_word, "position": {"x": x, "y": y}})

            return words_with_positions

        except Exception as e:
            raise RuntimeError(f"Error extracting text: {e}")
