from pydantic import BaseModel


class PublicTokenExchangeRequest(BaseModel):
    public_token: str


class SyncRequest(BaseModel):
    item_id: int | None = None
from pydantic import BaseModel


class LinkTokenResponse(BaseModel):
    link_token: str


class TokenExchangeRequest(BaseModel):
    public_token: str
