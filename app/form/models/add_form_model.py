from typing import Optional
from pydantic import BaseModel

from app.form.models.schema_item_model import SchemaItem

class AddFormModel(BaseModel):

    name: str

    description: str

    width: str
       
    requiredLogin: Optional[bool] = False

    schemas: list[SchemaItem]