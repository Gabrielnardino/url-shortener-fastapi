from pydantic import BaseModel
from typing import Optional # NOVO

class URLBase(BaseModel):
    long_url: str

class URLRequest(URLBase):
    custom_code: Optional[str] = None # NOVO CAMPO OPCIONAL

class URLResponse(URLBase):
    short_code: str

    class Config:
        from_attributes = True