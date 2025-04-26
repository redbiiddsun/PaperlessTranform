import pprint
from text_extraction.PDF import PDFExtractor
from parse.parse import TextParse
from translation.translation import Translation
from DataTypeAnalyzer.data_type_analyzer import DataTypeAnalyzer

def print_section(title: str):
    print(f"\n{'=' * 40}")
    print(f"{title}")
    print(f"{'=' * 40}")

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4, width=100, compact=False)

    print_section("1. Extracting Text from PDF")
    pdf_text = PDFExtractor().extract_text("./file/Government/th/ใบคําร้องขอเลขรหัสประจําบ้าน.pdf")
    # pdf_text = PDFExtractor().extract_text("./file/ใบลาออก.pdf")
    pp.pprint(pdf_text)

    print_section("2. Parsing Labels from Extracted Text")
    extracted_labels = TextParse.extract_labels(pdf_text)
    pp.pprint(extracted_labels)

    print_section("3. Translating Parsed Labels")
    translated_labels = Translation().translate(extracted_labels)
    pp.pprint(translated_labels)

    translated_fields = [item['translated_field'] for item in translated_labels]

    print_section("4. Extracted Translated Fields (for Analysis)")
    pp.pprint(translated_fields)

    print_section("5. Analyzing Data Types")
    try:
        data_types = DataTypeAnalyzer().analyze_fields(translated_fields)
        pp.pprint(data_types)
    except Exception as e:
        print(f"❌ Failed to analyze data types: {e}")
