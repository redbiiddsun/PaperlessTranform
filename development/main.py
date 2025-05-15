import pprint
from text_extraction.PDF import PDFExtractor
from parse.parse import TextParse
from translation.translation import Translation
from DataTypeAnalyzer.data_type_analyzer import DataTypeAnalyzer

if __name__ == '__main__':

    pdf_reader = PDFExtractor().extract_text("./file/dot_input/แบบฟอร์มผู้ป่วยใหม่.pdf")


    print("------------------- PDF Reader -------------------")
    pprint.pprint(pdf_reader)


    extracted_text = TextParse.extract_labels(pdf_reader)

    print("------------------- Extracted Label -------------------")
    pprint.pprint(extracted_text)

    translated_text = Translation().translate(extracted_text)

    print("------------------- Translation -------------------")
    pprint.pprint(translated_text)

    translated_fields = [item['translated_field'] for item in translated_text]

    data_type = DataTypeAnalyzer().analyze_fields(translated_fields)

    print("------------------- Llamma Result -------------------")
    pprint.pprint(data_type)

    mapping_value = DataTypeAnalyzer().mapping_value(data_type, translated_text)

    print("------------------- Final Result -------------------")
    pprint.pprint(mapping_value)