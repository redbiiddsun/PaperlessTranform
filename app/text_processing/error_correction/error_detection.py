
from typing import List, Literal, Union
from pythainlp.corpus.common import thai_words
from pythainlp import word_tokenize
import re

class ErrorDetection: 
    def __inti__(self):
        pass

    def detect_language(self, text: str) -> Literal["th", "en"]:
        thai_pattern = re.compile(r'[\u0E00-\u0E7F]+')
        english_pattern = re.compile(r'[A-Za-z]+')
        
        thai_count = len(thai_pattern.findall(text))
        english_count = len(english_pattern.findall(text))

        if thai_count > english_count:
            return "th"

        return "en"
    
    def is_number(self, text: str) -> bool:
        try:
            float(text)
            return True
        except ValueError:
            return False
        
    def english_words(self):
        with open('words_alpha.txt', 'r') as f1, open('words.txt', 'r') as f2:
            words1 = set(f1.read().split()) 
            words2 = set(f2.read().split())  

            combined_words = words1 | words2 
            return list(combined_words)
        
    def join_text(self, texts: List[str]) -> str:
        return ''.join(texts)

    def find(self, texts: List[str]) -> List[str]:

        thai_dict = thai_words()
        english_dict = self.english_words

        list_text = []

        for each_text in texts:

            tokenize_word = word_tokenize(each_text, keep_whitespace=True)

            for index, word in enumerate(tokenize_word):

                if(len(word) <= 1 or self.is_number(word)):
                    continue

                if self.detect_language(word) == "en":
                    if word not in english_dict:
                        tokenize_word[index] = '<error>' + word + '</error>'

                if word not in thai_dict:
                    tokenize_word[index] = '<error>' + word + '</error>'

            list_text.append(self.join_text(tokenize_word))

        return list_text