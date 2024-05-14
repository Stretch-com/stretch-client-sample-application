import os
import requests
from fastapi import APIRouter
from typing import List, Optional, Union
from uuid import UUID
from pydantic import Field
from enum import Enum

from base_app_model import BaseAppModel


# Enums
class PaginationIn(BaseAppModel):
    offset: int = Field()
    limit: int = Field()


class PaginationOut(PaginationIn):
    total: int = Field()


class SortOptions(str, Enum):
    RATING = "rating"
    DISTANCE = "distance"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


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


class Sort(BaseAppModel):
    sort_by: Optional[SortOptions] = Field(default=None, title="Sort by", description="Sort by specified field")
    sort_order: Optional[SortOrder] = Field(
        default=None, title="Sort order", description="Order of sorting (asc, desc)"
    )


class Coordinates(BaseAppModel):
    latitude: float = Field(examples=[42.3243])
    longitude: float = Field(examples=[58.7123])


class UserGender(str, Enum):
    male = "male"
    female = "female"
    trans_man = "transman"
    trans_woman = "transwoman"


class SearchInFilters(BaseAppModel):
    gender: Optional[UserGender] = Field(default=None, title="Gender", description="Gender of an person", example=UserGender.male.value)
    languages: List[str] = Field(default=[], examples=[["en"]])
    service_types: List[str] = Field(default=[], title="Service type", description="Service type")
    search_by_text: Optional[str] = Field(default=None, title="Search by text", description="Search by target text")
    user_id: Optional[str] = Field(default=None, title="User id", description="User id in our system")


class SearchIn(BaseAppModel):
    category_id: UUID = Field(title="Category id", description="Category id in our system")
    coord: Coordinates = Field(
        title="Coordinates",
        description="Coordinates (latitude, longitude)",
        examples=[Coordinates(latitude=42.3243, longitude=54.646)],
    )
    filters: SearchInFilters = Field(default_factory=SearchInFilters)
    sort: Sort = Field(default_factory=Sort)
    pagination: PaginationIn = Field(default_factory=PaginationIn)


class SearchOut(PaginationIn, BaseAppModel):
    profiles: list[VendorShortOut] = Field(default=[])

# -------------------------------------------------------------------------------------------------


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'https://api.stretch.com/api/v1/public')
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })


@router.post("/search", response_model=SearchOut)
async def search(dto_in: SearchIn):
    return session.post(f"{base_url}/search", data=dto_in.model_dump_json()).json()
