import os
import json
import requests
import datetime
from fastapi import APIRouter
from typing import List, Optional, Union, Tuple
from uuid import UUID
from pydantic import Field, BaseModel
from enum import Enum

# Enums


class PaginationIn(BaseModel):
    offset: int = Field()
    limit: int = Field()


class PaginationOut(PaginationIn):
    total: int = Field()


class SortOptions(str, Enum):
    RATING = "rating"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"




# Models


class GalleryItemOut(BaseModel):
    url: str = Field()
    thumbnail_url: str = Field()
    type: str = Field()


class Service(BaseModel):
    id: UUID = Field()
    name: str = Field()
    description: str = Field()
    price: float = Field()
    price_per_session: float = Field(alias="pricePerSession")
    price_currency: str = Field(alias="priceCurrency")


class Review(BaseModel):
    message: str = Field()
    label: str = Field()


class VendorIn(BaseModel):
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


class VendorDetailedOut(BaseModel):
    name: Optional[str] = Field(default=None)
    profile_image_url: Optional[str] = Field(default=None)
    gallery: List[GalleryItemOut] = Field(default=[])
    languages: Union[List[str], str] = Field(default=None)
    # coord: Optional[Tuple[float, float]] = Field(default=None)
    distance: Optional[float] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    reviews: List[Review] = Field(default=[])
    services: List[Service] = Field(default=[])


class VendorProfileDetailedIn(BaseModel):
    vendor_id: UUID


class Sort(BaseModel):
    sort_by: Optional[SortOptions] = Field(default=None, title="Sort by", description="Sort by specified field")
    sort_order: Optional[SortOrder] = Field(
        default=None, title="Sort order", description="Order of sorting (asc, desc)"
    )


class SearchInFilters(BaseModel):
    category_id: UUID = Field(title="Category id", description="Category id in our system")
    gender: Optional[str] = Field(default=None, title="Gender", description="Gender of an person")
    languages: List[str] = Field(default=[], examples=["en"])
    service_types: List[str] = Field(default=[], title="Service type", description="Service type")
    search_by_text: Optional[str] = Field(default=None, title="Search by text", description="Search by target text")
    coord: Optional[Tuple[float, float]] = (
        Field(  # TODO position is required, implement functionality to find user loc by ip
            default=None,
            title="Coordinates",
            description="Coordinates (latitude, longitude)",
            examples=[[42.3243, 54.646]],
        )
    )
    user_id: Optional[str] = Field(default=None, title="User id", description="User id in our system")


class SearchIn(BaseModel):
    filters: SearchInFilters = Field(default_factory=SearchInFilters)
    sort: Sort = Field(default_factory=Sort)
    pagination: PaginationIn = Field(default_factory=PaginationIn)


class SearchOut(PaginationIn, BaseModel):
    profiles: list[VendorShortOut] = Field(default=[])

# -------------------------------------------------------------------------------------------------


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'http://localhost:8000/api/v1/public')
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



@router.post("/search", response_model=SearchOut)
async def search(dto_in: SearchIn):
    return  session.post("/search", data=json.dumps(dto_in.dict(), cls=JSONEncoder))