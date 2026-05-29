from pydantic import BaseModel


class SplitwiseConnectRequest(BaseModel):
    access_token: str
    token_type: str = "bearer"
