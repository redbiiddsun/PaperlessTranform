import re
import string

class TextParse():

    @DeprecationWarning
    def extract_labels_deprecated(text: str) -> list[str]:
        # Define a regex pattern to capture field labels
        pattern = r'([\u0E00-\u0E7F]+)(?=\s{0,2}[\.\:])'  # Thai words before . or :, allowing 0-2 spaces

        labels = re.findall(pattern, text)

        for i in range(1, len(labels)):
            if len(labels[i]) == 1 and len(labels[i-1]) == 1:
                labels[i-1] = labels[i-1] + '.' + labels[i] + '.'
                labels[i] = ''
            
        labels = [label for label in labels if label != '']
        
        return labels
    
    def __remove_numbering(text):
        """Removes numbering from strings formatted as '1. Name' or '(1) Name'."""
        return re.sub(r"^\(?\d+\)?\.\s*|\(?\d+\)\s*", "", text)
    
    def extract_labels(text: str) -> list[str]:
    
        label = []

        # Split text into lines and remove empty lines
        spilt_line_text = [line for line in text.splitlines() if line.strip()]

        for prev_line, curr_line in zip(spilt_line_text, spilt_line_text[1:]):

            if('.' not in curr_line):
                continue
            
            # Check if the current line has 3 or more dots but the prvious line ends with a punctuation eg. [., (), {},]
            if re.match(r"^\.{3,}", curr_line) and (bool(prev_line) and prev_line[-1] in string.punctuation):
                continue

            # Check if the current line has 3 or more dots and the previous line is end with a character
            if re.match(r"^\.{3,}", curr_line) and (bool(prev_line) and prev_line[-1] not in string.punctuation):
                match = re.search(r'([^.\n]+)\.?$', prev_line)
                value = match.group(1).strip() if match else None
                label.append(value)
                continue    
    
            matches = re.findall(r"(.*?)\.{3,}", curr_line)

            for match in matches:

                clear_text = match.strip()

                if(len(clear_text) == 1 and clear_text in string.punctuation or clear_text == ''):
                    continue

                clear_text = TextParse.__remove_numbering(clear_text)

                label.append(clear_text)

            filtered_list = [item for item in label if item.strip() != ""]


        return filtered_list

