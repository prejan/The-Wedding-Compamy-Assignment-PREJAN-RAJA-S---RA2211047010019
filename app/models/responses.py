from pydantic import BaseModel

class OrgCreateResponse(BaseModel):
    message: str
    organization: dict


class LoginResponse(BaseModel):
    token: str
