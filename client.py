import os
from fastapi import APIRouter, Depends
import requests
from pydantic import Field, EmailStr
from typing import Optional, Tuple

from base_app_model import BaseAppModel


# Models


class LocationIn(BaseAppModel):
    coord: Optional[Tuple[float, float]] = Field()
    country: str = Field(example="United Arab Emirates", description="Country")
    state: str = Field(example="Dubai", description="state")
    city: str = Field(example="Dubai", description="city")
    line1: str = Field(example="Jumeirah Lake Towers", description="line 1")
    line2: Optional[str] = Field(default="", description="line 2")
    zip: str = Field(example=None, description="zip (po box)")


class EditClientIn(BaseAppModel):
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    phone: str = Field()
    location: Optional[LocationIn] = Field(default_factory=LocationIn)


class CreateClientIn(EditClientIn):
    external_id: Optional[str] = Field()


class CreateClientOut(BaseAppModel):
    external_id: Optional[str] = Field()
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    phone: str = Field()
    location: Optional[LocationIn] = Field(default_factory=LocationIn)


class CreateClientDTO(BaseAppModel):
    external_id: str = Field(...)
    username: str
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str
    phone: str
    country: str
    latitude: str
    longitude: str
    state: str
    city: str
    line1: str
    line2: Optional[str] = ""
    zip: str

# -------------------------------------------------------------------------------------------------


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'https://api.stretch.com/api/v1/public')
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })


@router.put("/client", response_model=CreateClientOut)
async def edit_client(dto_in: CreateClientDTO = Depends()):
    dto_in = CreateClientIn(
        external_id=dto_in.external_id,
        username=dto_in.username,
        first_name=dto_in.first_name,
        last_name=dto_in.last_name,
        email=dto_in.email,
        phone=dto_in.phone,
        location=LocationIn(
            coord=[dto_in.latitude, dto_in.longitude],
            country=dto_in.country,
            city=dto_in.city,
            state=dto_in.state,
            line1=dto_in.line1,
            line2=dto_in.line2,
            zip=dto_in.zip
        )
    )
    res = session.post(f"{base_url}/client", json=dto_in.dict())
    res.raise_for_status()
    res = res.json()
    return res

