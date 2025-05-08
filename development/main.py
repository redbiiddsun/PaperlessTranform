import pprint
from text_extraction.PDF import PDFExtractor
from parse.parse import TextParse
from translation.translation import Translation
from DataTypeAnalyzer.data_type_analyzer import DataTypeAnalyzer

if __name__ == '__main__':

    pdf_reader = PDFExtractor().extract_text_with_position("./file/dot_input/แบบฟอร์มผู้ป่วยใหม่.pdf")

    # extracted_text = TextParse.extract_labels(pdf_reader)

    # translated_text = Translation().translate(extracted_text)

    # print(translated_text)

    # translated_fields = [item['translated_field'] for item in translated_text]

    # print(translated_fields)

    # data_type = DataTypeAnalyzer().analyze_fields(translated_fields)

    pprint.pprint(pdf_reader)

