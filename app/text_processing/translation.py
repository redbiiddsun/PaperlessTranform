import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

class Translation:
    def __init__(self, source_language='tha_Thai', target_language='eng_Latn', model_name="wtarit/nllb-600M-th-en"):
        self.source_language = source_language
        self.target_language = target_language
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else "cpu"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.translation_pipeline = pipeline(
            "translation",
            model=self.model,
            tokenizer=self.tokenizer,
            src_lang=self.source_language,
            tgt_lang=self.target_language,
            max_length=1024,
            device=self.device
        )

    def translate(self, text):

        result = []

        if(type(text) == list):
            for original_text in text:

                translated_text = self.translation_pipeline(original_text)

                result.append({"original_field": original_text, "translated_field": translated_text[0]['translation_text']})
                
            return result

        single_translated_text = self.translation_pipeline(text)
        return single_translated_text[0]['translation_text']

    def __str__(self):
        return f"Translation from {self.source_language} to {self.target_language}"