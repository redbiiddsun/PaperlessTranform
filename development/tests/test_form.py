from pprint import pprint
import unittest

from ..parse.parse import TextParse
from ..text_extraction.PDF import PDFExtractor
from ..tests.test_suite import test_suit

def compare_dicts(detail, arr1, arr2):

    """
    Compare two dictionaries and return the keys that are in arr2 but not in arr1.
    """

    missing_value = []

    for compare_value in arr2:
        if compare_value not in arr1:
            missing_value.append(compare_value)


    print("---------------------------------------------------------------------------")
    print("File:", detail)
    print("Result:")
    pprint(arr1)
    print()

    print("Expected result:")
    pprint(arr2)
    print()

    print("Missing values:", missing_value)
 
class TestFormParse(unittest.TestCase):

    def test_form_1(self):
        
        pdf_reader = PDFExtractor().extract_text(test_suit["form_1"]["file_path"])

        extracted_text = TextParse.extract_labels(pdf_reader)

        excepted_text = test_suit["form_1"]["expected_labels"]

        compare_dicts(test_suit["form_1"]["file_path"], extracted_text, excepted_text)
   
    def test_form_2(self):
        
        pdf_reader = PDFExtractor().extract_text(test_suit["form_2"]["file_path"])

        extracted_text = TextParse.extract_labels(pdf_reader)

        excepted_text = test_suit["form_2"]["expected_labels"]

        compare_dicts(test_suit["form_2"]["file_path"], extracted_text, excepted_text)

    def test_form_3(self):
        
        pdf_reader = PDFExtractor().extract_text(test_suit["form_3"]["file_path"])

        extracted_text = TextParse.extract_labels(pdf_reader)

        excepted_text = test_suit["form_3"]["expected_labels"]

        compare_dicts(test_suit["form_3"]["file_path"], extracted_text, excepted_text)

      
    def test_form_4(self):
        
        pdf_reader = PDFExtractor().extract_text(test_suit["form_4"]["file_path"])

        extracted_text = TextParse.extract_labels(pdf_reader)

        excepted_text = test_suit["form_4"]["expected_labels"]

        compare_dicts(test_suit["form_4"]["file_path"], extracted_text, excepted_text)

    def test_form_5(self):
        
        pdf_reader = PDFExtractor().extract_text(test_suit["form_5"]["file_path"])

        extracted_text = TextParse.extract_labels(pdf_reader)

        excepted_text = test_suit["form_5"]["expected_labels"]

        compare_dicts(test_suit["form_5"]["file_path"], extracted_text, excepted_text)

if __name__ == '__main__':
   unittest.main()