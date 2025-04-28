import json
import re
from typing import List
from jsonschema import validate

from DataTypeAnalyzer.llama_wraper import LlamaWrapper


class DataTypeAnalyzer(LlamaWrapper):

    def __init__(self, model_name: str = 'llama3.2'):
        super().__init__()
        self.model_name = model_name
        self.system_prompt = """You are a data type analyzer.

Your task is to analyze input fields and return a structured JSON response. Follow this exact format:

Output:
A JSON array containing a single object with these keys:
- "form_name": The name of the form. If the input labels are in Thai, use the Thai form name.
- "fields": An array of objects, where each object describes a single form field.

Each object in "fields" must have (all object is required):
- "field": The label or name of the input field (as provided).
- "type": The data type from the supported list (only use the 8 types below).
- "validation": Validation rules as a string.
- "outerClass": Use `"col-span-1"` if the field label is short, or `"col-span-2"` if it is long.

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

Output Format:

Return **only** a valid JSON array with objects having this structure:
```json
[
    "form_name": "Registration Form",
    "fields": [
        {
            "field": "Name",
            "type": "text",
            "validation": "required|length:1,255"
            "outerClass": "col-span-1"
        },
        {
            "field": "Last Name",
            "type": "text",
            "validation": "required|length:1,255"
            "outerClass": "col-span-1"
        },
        {
            "field": "Email",
            "type": "email",
            "validation": "required|email"
            "outerClass" : "col-span-2"

        },
        {
            "field": "Date Of Birth",
            "type": "date"
            "validation": "required|date_before:today"
            "outerClass" : "col-span-2"
        },
        ...
    ]
]

*** Do not include any explanations,  only output the JSON array. ***
*** Do not use other types except 8 types above.***
"""

    def analyze_fields(self, fields: str | List[str]) -> object:

        if isinstance(fields, list):
            fields = ', '.join(fields)

        user_prompt = f"Generate a JSON schema for these fields: {fields}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = super().chat(
                messages=messages
            )

            cleaned_data = self.cleaning_data(response['message']['content'])
            fields_data = json.loads(cleaned_data)

            if not self.validate_schema(fields_data):
                raise Exception("Invalid schema")

            return fields_data

        except json.JSONDecodeError as e:
            raise Exception(
                f"Error decoding JSON: {str(e)}. Raw response: '{response['message']['content']}'")
        except Exception as e:
            raise Exception(f"Error analyzing fields: {str(e)}")

    def cleaning_data(self, data: str) -> str:
        match = re.search(r'\[(.*)\]', data, re.DOTALL)
        if match:
            json_string = f"[{match.group(1)}]"
            json_string = json_string.replace('\\', '\\\\')
            return json_string
        return ""

    def validate_schema(self, data: object) -> bool:
        json_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "form_name": {"type": "string"},
                    "fields": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "field": {"type": "string"},
                                "type": {"type": "string"},
                                "validation": {"type": "string"},
                                "outerClass": {"type": "string"}
                            },
                            "required": ["field", "type", "validation", "outerClass"]
                        }
                    }
                },
                "required": ["form_name", "fields"]
            }
        }

        try:
            validate(instance=data, schema=json_schema)
            return True
        except Exception as e:
            print(f"Validation failed: {e}")
            return False
