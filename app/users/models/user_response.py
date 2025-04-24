import uuid
from pydantic import BaseModel

class UserResponse(BaseModel):
    
    id: uuid.UUID

    email: str

    firstname: str
    
    lastname: str

    model_config = {
        "from_attributes": True
    }