from typing import Any, Dict, Optional
from pydantic import BaseModel, Json

from app.form.models.schema_item_model import SchemaItem

class AddFormModel(BaseModel):

    name: str

    schemas: list[SchemaItem]
    
    requiredLogin: Optional[bool] = False