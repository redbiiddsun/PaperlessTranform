import pprint
from form import Form
from text_extraction.PDF import PDFExtractor
from parse.parse import TextParse
from translation.translation import Translation
from DataTypeAnalyzer.data_type_analyzer import DataTypeAnalyzer

if __name__ == '__main__':

    pdf_reader = PDFExtractor().extract_text("./file/dot_input/แบบฟอร์ม_ประกาศ.pdf")

    print(pdf_reader)

    extracted_text = Form().extract_labels(pdf_reader)
    
    print(extracted_text)

    # translated_text = Translation().translate(extracted_text)

    # # print(translated_text)

    # translated_fields = [item['translated_field'] for item in translated_text]

    # # print(translated_fields)

    # data_type = DataTypeAnalyzer().analyze_fields(translated_fields)

    # pprint.pprint(data_type)

    # mapping_value = DataTypeAnalyzer().mapping_value(data_type, translated_text)

    # print("------------------- Final Result -------------------")
    # pprint.pprint(mapping_value)