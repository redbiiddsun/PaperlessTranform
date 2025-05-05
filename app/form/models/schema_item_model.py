from pydantic import BaseModel, Field


class SchemaItem(BaseModel):
    id: int

    formkit: str = Field(alias="$formkit")

    name: str

    description: str | None = None

    label: str

    value: str
    
    outerClass: str

    validation: str | None = None
    
    help: str | None = None