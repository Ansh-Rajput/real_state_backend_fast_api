from pydantic import BaseModel

class PropertyCreate(BaseModel):
    property_name: str
    locality: str
    owner_name: str

class PropertyUpdate(BaseModel):
    property_id: str
    locality_id: str
    owner_name: str
