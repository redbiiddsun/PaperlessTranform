from typing import FrozenSet, List, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pythainlp.corpus.common import thai_words


import numpy as np
import re

class ErrorCorrection():

    def __init__(self):
        pass

    def __extract_error(self, text: str):

        matches = re.findall(r"<error>(.*?)</error>", text)

        return matches
    
    def __has_error(self, text: str):
        return bool(re.search(r'<error>(.*?)</error>', text))
    
    def replace_errors(self, text, corrected_values):
        error_tags = re.findall(r'<error>(.*?)</error>', text)
        for i, error in enumerate(error_tags):
            if i < len(corrected_values):
                text = text.replace(f'<error>{error}</error>', corrected_values[i], 1)
        return text

    def cosine_similarity_text_correction(self, text: str, dict: Union[List[str], FrozenSet[str]]):
        try:
            if isinstance(dict, FrozenSet):
                dict = list(dict)

            vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))

            tfidf_matrix = vectorizer.fit_transform([text] + dict)  

            cos_sim_values = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]

            text_ranking = np.argsort(cos_sim_values)[-3:][::-1]
            first_ranking = dict[text_ranking[0]]

            if first_ranking == text:
                return text
            else:
                return first_ranking

        except TypeError as e:
            print(f"TypeError: {e}")

    def correct(self, list_text: List[str]) -> List[str]:

        thai_word = thai_words()

        for index, text in enumerate(list_text):

            corrected_text = []

            error_text = self.__extract_error(text)

            if(len(error_text) > 0):

                for error in error_text:
                    corrected_text.append(self.cosine_similarity_text_correction(error, thai_word))

                print(corrected_text)

                list_text[index] = self.replace_errors(text, corrected_text)

        return list_text