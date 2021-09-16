from typing import Optional
from pydantic import BaseModel


class Location(BaseModel):  # you can also nest the pydantic models
    city: str
    state: Optional[str] = None
    country: str = "US"
