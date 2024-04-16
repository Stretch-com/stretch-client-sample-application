from typing import Optional
from pydantic import Field, BaseModel, EmailStr
from .location import LocationIn


class EditClientIn(BaseModel):
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    phone: str = Field()
    location: LocationIn = Field(default_factory=LocationIn)


class CreateClientIn(EditClientIn):
    external_id: Optional[str] = Field()