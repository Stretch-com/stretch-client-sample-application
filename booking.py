import os
from fastapi import APIRouter, status
from typing import List, Optional, Tuple
import datetime
from uuid import UUID
from pydantic import Field, EmailStr
import requests
from enum import Enum

from base_app_model import BaseAppModel


# Enums
class PaymentStatus(str, Enum):
    COMPLETED: str = "completed"
    AWAITING: str = "awaiting"
    CANCELLED: str = "cancelled"


# Models
class Coordinates(BaseAppModel):
    latitude: float = Field(examples=[42.3243], description="Latitude on the map")
    longitude: float = Field(examples=[58.7123], description="Longitude on the map")


class SessionOut(BaseAppModel):
    price: float = Field()
    # state: SessionState = Field()
    # currency: str = Field(default="USD")
    # client: ClientDetails | None = Field(default=None)
    # coach: CoachDetails | None = Field(default=None)
    # coach_review: bool = Field(default=False)
    # client_review: bool = Field(default=False)
    # updated_by_user_id: UUID | None = Field(default=None)
    # # client: UserNotificationDetails | None = Field(default=None)
    # # coach: UserNotificationDetails | None = Field(default=None)
    # direction_id: UUID | None = Field(default=None)
    # payment: PaymentSessionOut | None = Field(default=None)
    # properties: Dict[str, Any] | None = Field(
    #     default=None, example={"property_name": "property_value"}, description="Extra property for user"
    # )
    # allow_booking: bool = Field(default=True)
    # booking_reason: BookingReasonOut | None = Field(default=None)
    # chat_url: str | None = Field(default=None)
    # report: PublicReportOut | None = Field(default=None)


class Payment(BaseAppModel):
    url: Optional[str]
    status: PaymentStatus


class BookSlotsOut(BaseAppModel):
    payment: Payment
    sessions: List[SessionOut]


class LocationIn(BaseAppModel):
    coord: Coordinates = Field(default_factory=Coordinates)
    country: str = Field(example="United Arab Emirates", description="Country")
    state: str = Field(example="Dubai", description="state")
    city: str = Field(example="Dubai", description="city")
    line1: str = Field(example="Jumeirah Lake Towers", description="line 1")
    line2: Optional[str] = Field(default="", description="line 2")
    zip: str = Field(example=None, description="zip (po box)")


class EditCustomerIn(BaseAppModel):
    customer_id: str = Field()
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    phone: str = Field()
    location: Optional[LocationIn] = Field(default_factory=LocationIn)


class CreateCustomerIn(EditCustomerIn):
    customer_id: Optional[str] = Field()


class EditCustomerProfileIn:
    customer_id: str = Field(description="Id of a user in your system")
    username: str = Field(description="Username of the user")
    first_name: str = Field(description="First name of the user")
    last_name: str = Field(description="Last name of the user")
    email: EmailStr = Field(description="Email of the user")
    phone: str = Field(description="Last name of the user")
    location: LocationIn = Field(default_factory=LocationIn, description="Location of the user")


class BookSlotsIn(CreateCustomerIn):
    service_id: UUID
    slots: List[datetime.datetime]

# -------------------------------------------------------------------------------------------------


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'https://api.stretch.com/api/v1/public')
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })


@router.post(
    "/booking",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    response_model=BookSlotsOut,
)
async def book_slots(params_in: BookSlotsIn):
    """
    Book corresponding slot foo customer
    :param params_in: id of the coach/business
    """
    return session.post(f"{base_url}/booking", data=params_in.model_dump_json()).json()
