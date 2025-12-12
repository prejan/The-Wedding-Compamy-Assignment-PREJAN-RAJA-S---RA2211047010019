from pydantic import BaseModel

class OrgCreate(BaseModel):
    organization_name: str
    email: str
    password: str

class OrgUpdate(BaseModel):
    organization_name: str
    email: str
    password: str
