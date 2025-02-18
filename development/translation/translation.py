from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

class Translation:
    def __init__(self, source_language, target_language):
        self.source_language = source_language
        self.target_language = target_language

    def __init__(self):
        self.source_language = 'tha_Thai'
        self.target_language = 'eng_Latn'

    def translate(self, text):
        # ------- MODEL SELECTION -------
        # Choose one of the following options to specify the model to use:

        # Option 1: Use an online model source
        # Uncomment the line below to download and use the online model
        # MODEL_NAME = "wtarit/nllb-600M-th-en"

        # Option 2: Use a local model
        # Uncomment the line below to specify the path to your local model
        MODEL_NAME = "wtarit/nllb-600M-th-en"

        # -------------------------------

        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        device = 0

        translation_pipeline = pipeline(
            "translation",
            model=model,
            tokenizer=tokenizer,
            src_lang=self.source_language,
            tgt_lang=self.target_language,
            max_length=1024,
            device=device
        )

        # HERE IS THE EXAMPLE OF HOW TO USE THE TRANSLATION PIPELINE
        result = translation_pipeline(text)

        return result[0]['translation_text']

    def __str__(self):
        return f"Translation from {self.source_language} to {self.target_language}: {self.source_text}"