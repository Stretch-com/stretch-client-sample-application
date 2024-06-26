import json
import os
import datetime
from typing import List, Optional, Union
from uuid import UUID

import requests
from fastapi import APIRouter, Depends
from pydantic import Field

from base_app_model import BaseAppModel


# Models

class GalleryItemOut(BaseAppModel):
    url: str = Field()
    thumbnail_url: str = Field()
    type: str = Field()


class Service(BaseAppModel):
    id: UUID = Field()
    name: str = Field()
    description: str = Field()
    price: float = Field()
    price_per_session: float = Field()
    price_currency: str = Field()


class Review(BaseAppModel):
    message: str = Field()
    label: str = Field()


class VendorIn(BaseAppModel):
    vendor_id: UUID = Field(default=None)


class VendorShortOut(VendorIn):
    vendor_id: UUID = Field(default=None)
    name: Optional[str] = Field(default=None)
    profile_image_url: Optional[str] = Field(default=None)
    gallery: List[GalleryItemOut] = Field(default=[])
    languages: Union[List[str], str] = Field(default=None)
    # coord: Optional[Tuple[float, float]] = Field(default=None)
    distance: Optional[float] = Field(default=None)
    rating: Optional[float] = Field(default=None)


class VendorDetailedOut(BaseAppModel):
    name: Optional[str] = Field(default=None)
    profile_image_url: Optional[str] = Field(default=None)
    gallery: List[GalleryItemOut] = Field(default=[])
    languages: Union[List[str], str] = Field(default=None)
    # coord: Optional[Tuple[float, float]] = Field(default=None)
    distance: Optional[float] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    reviews: List[Review] = Field(default=[])
    services: List[Service] = Field(default=[])


class VendorProfileDetailedIn(BaseAppModel):
    vendor_id: UUID
# -------------------------------------------------------------------------------------------------


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'https://api.stretch.com/api/v1/public')
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return str(obj)
        return super().default(obj)
@router.get("/vendor/{vendorId}", response_model=VendorDetailedOut)
async def get_vendor(dto_in: VendorIn = Depends()):
    return session.get(f"{base_url}/vendor/{dto_in.vendor_id}", params=dto_in.dict()).json()
