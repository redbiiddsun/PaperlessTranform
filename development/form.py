from enum import Enum
import re
import string

from text_utill import LineContext


class FormType(Enum):
    DASH = "-"
    UNDERSCORE = "_"
    DOT = "."

    def all_value():
        return [member.value for member in FormType]



class Form:
    def __init__(self):
        pass

    def __identify_form_type(self, form_text: str) -> FormType:
        """
        Args:
            form_text (str): The string to identify.

        Returns:
            FormType: The identified form type.
        """

        underscore_count = form_text.count(FormType.UNDERSCORE.value)
        dots_count = form_text.count(FormType.DOT.value)
        dash_count = form_text.count(FormType.DASH.value)

        # Find the character with the maximum count
        counts = {
            FormType.UNDERSCORE: underscore_count,
            FormType.DOT: dots_count,
            FormType.DASH: dash_count
        }

        # Return the FormType with the highest count
        most_common_form = max(counts, key=counts.get)

        return most_common_form
    
    def __remove_numbering(self, text):
        """Removes numbering from strings formatted as '1. Name' or '(1) Name'."""
        return re.sub(r"^\(?\d+\)?\.\s*|\(?\d+\)\s*", "", text)
    
    def get_last_non_blank_char(self, text: str) -> str:
        # Remove trailing whitespace
        trimmed = text.rstrip()
    
        # Return the last character, or empty string if none exist
        return trimmed[-1] if trimmed else ""
    
    def split_line_text(self, text: str) -> list[str]:
        return [line for line in text.splitlines() if line.strip()]

    def extract_labels_old(self, text: str) -> list[str]:

        form_type = self.__identify_form_type(text).value
    
        label = []

        # Split text into lines and remove empty lines
        spilt_line_text = self.split_line_text(text)

        for prev_line, curr_line in zip(spilt_line_text, spilt_line_text[1:]):

            # Check if the current line has the form type
            if(form_type not in curr_line):
                continue
            
            # Check if the current line has start dots/underscore/dash but the prvious line ends with a dots/underscore/dash
            if re.match(r"^\.{3,}", curr_line) and (bool(prev_line) and prev_line[-1] in string.punctuation):
                continue

            # Check if the current start line has 3 or more dots and the previous line is end with a character
            # EX of the case.
            #        ข้าพเจ้านาย/นาง/นางสาว......................พนักงานตำแหน่ง
            #        .......................มีความประสงค์ขอลาออกจากการเป็นพนักงานจ้างเหมา
            #
            if (re.match(r"^" + re.escape(form_type) + r"{3,}", curr_line) 
                and (bool(prev_line)
                and prev_line[-1] not in string.punctuation)):

                match = re.search(r'([^.\n]+)\.?$', prev_line)

                value = match.group(1).strip() if match else None

                label.append(value)

                continue

            matches = re.findall(r"(.*?)" + re.escape(form_type) + r"{3,}", curr_line)

            for match in matches:

                clear_text = match.strip()

                if(len(clear_text) == 1 and clear_text in string.punctuation or clear_text == ""):
                    continue

                clear_text = self.__remove_numbering(clear_text)

                label.append(clear_text)

        return label
    

    def extract_labels(self, text: str) -> list[str]:

        form_type = self.__identify_form_type(text).value
    
        label = []

        # Split text into lines and remove empty lines
        spilt_line_text = self.split_line_text(text)

        lines = LineContext(spilt_line_text)

        for index, ctx in enumerate(lines):

            # Check if the current line has the form type
            if(form_type not in ctx.current()):
                continue
                       
            # Check if the current line has start dots/underscore/dash but the prvious line ends with a dots/underscore/dash
            # Support this case
            #     Name............Surname...................... (prev)
            #     .............................................. (curr)
            if re.match(r"^"+ re.escape(form_type) + r"{3,}", ctx.current()) and (bool(ctx.previous())):

                # Check a prev line if it has a form type text or not
                check_prev = re.search(r"\S(?=\s*$)", self.get_last_non_blank_char(ctx.previous()))

                # Check None to prevent error
                if check_prev:
                    check_prev = check_prev.group()

                    if check_prev in form_type:
                        continue
            
                continue
            

            # Check if the current line has start dots/underscore/dash but the prvious line ends with a dots/underscore/dash
            # Support this case
            #  3. Permanent Address    
            #
            #  : ______________________________________________ 
            #
            if re.match(r"^:\s*" + re.escape(form_type) + r"+", ctx.current()):
                print("Found from case 1 : ", ctx.current())
                label.append(ctx.previous())

            # Check if the current line has start dots/underscore/dash but the prvious line ends with single colon, it will look back 2 previous lines and get the value
            # Support this case
            #  3. Permanent Address    
            #  :
            #  ______________________________________________ 
            #
            if re.match(r"^"+ re.escape(form_type) + r"{3,}", ctx.current()) and (re.search(r'\s*:\s*', text)):
                print("Found from case 2 : ", ctx.current())
                label.append(ctx.previous(2))

            # Check if the current start line has 3 or more dots and the previous line is end with a character
            # EX of the case.
            #        ข้าพเจ้านาย/นาง/นางสาว......................พนักงานตำแหน่ง
            #        .......................มีความประสงค์ขอลาออกจากการเป็นพนักงานจ้างเหมา
            #
            if (re.match(r"^" + re.escape(form_type) + r"{3,}", ctx.current())
                and (bool(ctx.previous())
                and ctx.previous()[-1] not in string.punctuation)):

                match = re.search(r'([^'+ re.escape(form_type) + r'\n]+)\.?$', ctx.previous())

                value = match.group(1).strip() if match else None

                label.append(value)

                continue

            # Check if the current start line has 3 or more dots and the previous line is end with a character
            # EX of the case.
            #        ข้าพเจ้านาย/นาง/นางสาว......................พนักงานตำแหน่ง
            #        .......................มีความประสงค์ขอลาออกจากการเป็นพนักงานจ้างเหมา
            #
            if (re.match(r"^" + re.escape(form_type) + r"{3,}", ctx.current())
                and (bool(ctx.previous())
                and ctx.previous()[-1] not in string.punctuation)):

                match = re.search(r'([^'+ re.escape(form_type) + r'\n]+)\.?$', ctx.previous())

                value = match.group(1).strip() if match else None

                label.append(value)

                continue

            matches = re.findall(r"(.*?)" + re.escape(form_type) + r"{3,}", ctx.current())

            for match in matches:

                clear_text = match.strip()

                if(len(clear_text) == 1 and clear_text in string.punctuation or clear_text == ""):
                    continue

                clear_text = self.__remove_numbering(clear_text)

                label.append(clear_text)

        # filtered_list = [item for item in label if item.strip() != ""]

        # for index, text in enumerate(filtered_list):
        #     filtered_list[index] = self.remove_private_use_characters(text)
        #         
        return self.clean_all_nonlabel_text(label)

    
    def remove_private_use_characters(self, text):
        return ''.join(c for c in text if not ('\uE000' <= c <= '\uF8FF'))
    
    def is_all_underscores_or_dots(self, text):
        return set(text).issubset(FormType.all_value())
    
    def remove_trailing_semicolon(text):
        stripped = text.rstrip()  # Remove trailing whitespace temporarily
        if stripped.endswith(';'):
            stripped = stripped[:-1]  # Remove the semicolon
            # Add back the original number of trailing spaces (if any)
            return stripped + text[len(stripped)+1:]
        return text
    
    def clean_trailing_colon_and_spaces(self, text):
        text = text.rstrip()  # Remove trailing spaces
        if text.endswith(':'):
            text = text[:-1]  # Remove the semicolon
        return text
    
    def clean_all_nonlabel_text(self, list_text: list[str]) -> str:

        for index, text in enumerate(list_text):

            if text.strip() == "":
                list_text.pop(index)
                continue

            if self.is_all_underscores_or_dots(text):
                list_text.pop(index)
                continue
            
            list_text[index] = self.remove_private_use_characters(text)

            list_text[index] = self.clean_trailing_colon_and_spaces(text)

            return list_text
