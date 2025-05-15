import ast
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import re
import difflib
from typing import List
from jsonschema import validate

from DataTypeAnalyzer.llama_wraper import LlamaWrapper


class DataTypeAnalyzer(LlamaWrapper):

    def __init__(self, model_name: str = 'llama3:8b'):
        super().__init__()
        self.executor = ThreadPoolExecutor()
        self.model_name = model_name
        self.system_prompt = """You are a data type analyzer. Your task is to analyze input fields and return their data types in a consistent JSON schema format. 
        Always return valid JSON as an array of objects with these exact fields for each input:
            - field: the exact field name as provided by the user, including any punctuation or separators.     
            - type: the fundamental data type (use only: text, number, tel, email, textarea, time, datetime-local, date)
            - validation: the validation rules as a string (e.g., required|length:1,255)
        CONDITION:
            - length of output should be the same as the length of input.
            
    Here are the supported data types:
        ---
    Supported Data Types (***Only use these 8 types***):

    1. `"text"`
    - Description: A short line of alphanumeric characters (e.g., names, titles).
    - Schema Format:
        ```json
        {
            "type": "text",
            "validation": "required|length:1,255"
        }
        ```

    2. `"number"`
    - Description: A numeric input (e.g., age, quantity).
    - Schema Format:
        ```json
        {
        "type": "number",
        "validation": "required|number|min:0"
        }
        ```

    3. `"tel"`
    - Description: A phone number, can include international format.
    - Schema Format:
        ```json
        {
        "type": "tel",
        "validation": "required|matches:^\\+?[0-9\\s\\-]{7,15}$"
        }
        ```

    4. `"email"`
    - Description: An email address.
    - Schema Format:
        ```json
        {
        "type": "email",
        "validation": "required|email"
        }
        ```

    5. `"textarea"`
    - Description: A multi-line text input (e.g., bio, comments).
    - Schema Format:
        ```json
        {
        "type": "textarea",
        "validation": "length:0,500"
        }
        ```

    6. `"time"`
    - Description: Time-only value (e.g., 14:30).
    - Schema Format:
        ```json
        {
        "type": "time",
        "validation": "required"
        }
        ```

    7. `"datetime-local"`
    - Description: Date and time input (e.g., for appointments).
    - Schema Format:
        ```json
        {
        "type": "datetime-local",
        "validation": "required"
        }
        ```

    8. `"date"`
    - Description: Date-only input (e.g., birthdate, deadlines).
    - Schema Format:
        ```json
        {
        "type": "date",
        "validation": "required|date_before:today"
        }
        ```
    ---

            Example output structure:
                [
                    {
                        "field": "", 
                        "type": "",
                        "validation": ""
                    },
                    {
                        "field": "",
                        "type": "",
                        "validation": ""
                    },
                    {
                        "field": "",
                        "type": "",
                        "validation": ""
                    }
                ]

                Do not include any explanations, only output the JSON array."""

    def analyze_fields(self, fields: str | List[str]) -> object:

        if isinstance(fields, list):
            fields = ', '.join(fields)

        print(f"Analyzing fields: {fields}")

        user_prompt = f"Generate a JSON schema for these fields: {fields}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:

            response = super().chat(
                messages=messages
            )

            cleaned_data = self.extract_json_like_array(
                response['message']['content'])

            cleaned_data = self.cleaning_data(cleaned_data)

            fields_data = json.loads(cleaned_data)

            if not self.validate_schema(fields_data):
                raise Exception("Invalid schema")

            return fields_data

        except json.JSONDecodeError as e:
            raise Exception(
                f"Error decoding JSON: {str(e)}. Raw response: '{response['message']['content']}'")
        except Exception as e:
            raise Exception(f"Error analyzing fields: {str(e)}")

    async def analyze_fields_async(self, fields: str | List[str]) -> object:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.analyze_fields, fields)

    def cleaning_data(self, data: str) -> str:
        match = re.search(r'\[(.*)\]', data, re.DOTALL)
        if match:
            json_string = f"[{match.group(1)}]"
            # Ensure all backslashes are correctly escaped
            json_string = json_string.replace('\\', '\\\\')
            # Ensure proper JSON string formatting
            json_string = json_string.strip().replace("\n", "").replace("\r", "")
            return json_string
        raise Exception("Invalid JSON format: JSON array not found.")


    def extract_json_like_array(self, text):
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            json_like_str = match.group(0)

            return json_like_str

        raise Exception(f"Invalid JSON format: '{text}'")

    def validate_schema(self, data: object) -> bool:
        json_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "type": {"type": "string"},
                    "validation": {"type": "string"}

                },
                "required": ["field", "type", "validation"],
            }
        }

        try:
            validate(instance=data, schema=json_schema)

            return True

        except Exception as e:

            print(f"Validation failed: {e}")

            return False

    def mapping_value(self, data_type, translated_text):
        # Create a lookup dictionary for translated fields
        translated_fields = [t['translated_field'] for t in translated_text]
        translated_map = {t['translated_field']: t['original_field'] for t in translated_text}

        for item in data_type:
            # Find closest matches for item['field'] from translated_fields
            matches = difflib.get_close_matches(item['field'], translated_fields, n=1, cutoff=0.8)
            if matches:
                best_match = matches[0]
                item['original_field'] = translated_map[best_match]
            # else: do NOT assign original_field (no default)

        return data_type

    def find_closest_field(self, field_name, lookup_dict):
        for translated, original in lookup_dict.items():
            # If the translated field is a substring of the field name
            if translated.lower() in field_name.lower():
                return original
        return None

