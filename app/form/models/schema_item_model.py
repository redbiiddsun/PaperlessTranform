from pydantic import BaseModel, Field


class SchemaItem(BaseModel):
    id: int

    formkit: str = Field(alias="$formkit")

    name: str

    desciption: str | None = None

    label: str

    value: str
    
    outerClass: str
    
    help: str | None = None

    width: str
