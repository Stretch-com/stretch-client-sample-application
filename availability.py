import os
from typing import List

from fastapi import Depends, APIRouter
import requests
import datetime
from typing import Optional
from uuid import UUID
from enum import Enum
from pydantic import Field

from base_app_model import BaseAppModel


# Models


class TimezoneOptions(str, Enum):
    UTC = "utc"
    AUTO = "auto"


class AvailabilityIn(BaseAppModel):
    service_id: UUID = Field(examples=["cae6a37d-fab6-4242-b1a5-4b8eb3a00efa"])
    start_search: Optional[datetime.date] = Field(default=None, examples=["2024-05-05 07:00:00.608 +0400"])
    end_search: Optional[datetime.date] = Field(default=None, examples=["2024-05-05 07:00:00.608 +0400"])
    timezone: Optional[TimezoneOptions] = Field(default=TimezoneOptions.AUTO)


class AvailabilityOut(BaseAppModel):
    slot_start: datetime.datetime = Field()

# -------------------------------------------------------------------------------------------------


router = APIRouter()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'https://api.stretch.com/api/v1/public')
session = requests.Session()
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })


@router.get(
    "/availability/{service_id}",
    response_model=List[AvailabilityOut]
)
async def get_availability(
    dto_in: AvailabilityIn = Depends(),
):
    """
    Get availability for service by coach/business
    :param dto_in:
    service_id: id of the coach/business
    start_search: Optional[datetime] start search from, must be >= now
    end_search: Optional[datetime] end search from, must be >= start_search
    """
    service_id = dto_in.service_id
    dto = dto_in.dict()
    del dto["service_id"]
    resp = session.get(f"{base_url}/availability/{service_id}", params=dto)
    return resp.json()
