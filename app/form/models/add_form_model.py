from typing import Optional
from pydantic import BaseModel

from app.form.models.schema_item_model import SchemaItem

class AddFormModel(BaseModel):

    name: str

    schemas: list[SchemaItem]
        
    requiredLogin: Optional[bool] = False