import json
import os
from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
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

# -------------------------------------------------------------------------------------------------


class GenerateTemplate:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.templates = Jinja2Templates(directory=f"{dir_path}/templates")

    def execute(self, filename, content: dict):
        content["base_url"] = (
            f'{os.getenv("STRETCH_API_URL", "http://localhost/sample_application")}{os.getenv("STRETCH_API_PREFIX",  "/api/v1")}'  # noqa
        )
        try:
            return self.templates.TemplateResponse(
                filename,
                content,
            )
        except Exception as e:
            raise e


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'http://localhost:8000/api/v1/public')
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })

generate_template = GenerateTemplate()


@router.get("/client/form", response_class=HTMLResponse)
async def create_client_form(request: Request):
    template = generate_template.execute("client_form.html", content={"request": request})
    return template


@router.post("/client", response_class=Response)
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
    res = session.post(f"{base_url}/client", data=json.dumps(dto_in.dict()))
    res.raise_for_status()
    return res.json()
