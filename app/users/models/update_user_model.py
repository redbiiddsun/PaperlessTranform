from typing import Optional
from pydantic import BaseModel

class UpdateUserModel(BaseModel):

    firstname: Optional[str] = None
    
    lastname: Optional[str] = None
    
    email: Optional[str] = None