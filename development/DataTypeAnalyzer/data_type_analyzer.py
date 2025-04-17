import json
from typing import List
from jsonschema import validate

from DataTypeAnalyzer.llama_wraper import LlamaWrapper

class DataTypeAnalyzer(LlamaWrapper):

    def __init__(self, model_name: str = 'llama3.2'):
        super().__init__()
        self.model_name = model_name
        self.system_prompt = """You are a data type analyzer. Your task is to analyze input fields and return their data types in a consistent JSON schema format. 
        Always return valid JSON as an array of objects with these exact fields for each input:
            - field: the input field name         
            - type: the fundamental data type (use only: text, number, boolean, date)

        Example output structure:
            [
                {
                    "field": "", 
                    "type": ""
                },
                {
                    "field": "",
                    "type": ""
                },
                {
                    "field": "",
                    "type": ""
                }
            ]

                Do not include any explanations, only output the JSON array."""

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

            fields_data = json.loads(self.cleaning_data(response['message']['content']))

            if not self.validate_schema(fields_data):
                raise Exception("Invalid schema")

            return fields_data
        
        except Exception as e:
            raise Exception(f"Error analyzing fields: {str(e)}")
        

    def cleaning_data(self, data: str) -> str:
        lines = data.strip().split('\n')

        for i in range(len(lines)):
            if not lines[i].startswith('['):
                lines.pop(i)
            break

        for i in range(len(lines)-1, -1, -1):
            if not lines[i].startswith(']'):
                lines.pop(i)
            break

        cleaned_string = '\n'.join(lines)

        return cleaned_string

    def validate_schema(self, data: object) -> bool:

        json_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "type": {"type": "string"}
                },
                "required": ["field", "type"]
            }
        }
        
        try:
            validate(instance=data, schema=json_schema) 
            return True
        except:
            return False
