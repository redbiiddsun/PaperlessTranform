from typing import Optional
from pydantic import BaseModel

class AddFormModel(BaseModel):

    name: str

    schemas: str
    
    requiredLogin: Optional[bool] = False