import os
from fastapi import Form, APIRouter
import requests
from pydantic import Field, BaseModel, EmailStr
from typing import Optional, Tuple

# Models


class LocationIn(BaseModel):
    coord: Optional[Tuple[float, float]] = Field()
    country: str = Field(example="United Arab Emirates", description="Country")
    state: str = Field(example="Dubai", description="state")
    city: str = Field(example="Dubai", description="city")
    line1: str = Field(example="Jumeirah Lake Towers", description="line 1")
    line2: Optional[str] = Field(default="", description="line 2")
    zip: str = Field(example=None, description="zip (po box)")


class EditClientIn(BaseModel):
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    phone: str = Field()
    location: Optional[LocationIn] = Field(default_factory=LocationIn)


class CreateClientIn(EditClientIn):
    external_id: Optional[str] = Field()


class CreateClientOut(BaseModel):
    external_id: Optional[str] = Field(alias="externalId")
    username: str = Field()
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: EmailStr = Field()
    phone: str = Field()
    location: Optional[LocationIn] = Field(default_factory=LocationIn)

# -------------------------------------------------------------------------------------------------


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'https://api.stretch.com/api/v1/public')
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })


@router.post("/client", response_model=CreateClientOut)
async def create_client(
        external_id: str = Form(...),
        username: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        country: str = Form(...),
        latitude: str = Form(...),
        longitude: str = Form(...),
        state: str = Form(...),
        city: str = Form(...),
        line1: str = Form(...),
        line2: Optional[str] = Form(""),
        zip: str = Form(...)
    ):
    dto_in = CreateClientIn(
        external_id=external_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        location=LocationIn(
            coord=[latitude, longitude],
            country=country,
            city=city,
            state=state,
            line1=line1,
            line2=line2,
            zip=zip
        )
    )
    res = session.post(f"{base_url}/client", json=dto_in.dict())
    res.raise_for_status()
    res = res.json()
    return res

