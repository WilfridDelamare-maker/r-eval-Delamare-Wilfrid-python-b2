from typing import Literal

from pydantic import BaseModel, Field

class Station(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    status: Literal["open", "closed", "maintenance"] = "open"

class StationPatch(BaseModel):
    name: str | None = None
    status: Literal["open", "closed", "maintenance"] = "open"