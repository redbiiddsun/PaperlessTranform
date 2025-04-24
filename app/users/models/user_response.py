import uuid
from pydantic import BaseModel

from typing import Optional


class UserResponse(BaseModel):
    
    id: uuid.UUID
    email: str
    firstname: str
    lastname: str

    model_config = {
        "from_attributes": True
    }

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    
    last_name: Optional[str] = None
    
    email: Optional[str] = None