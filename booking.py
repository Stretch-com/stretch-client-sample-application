import os
from fastapi import APIRouter, status
from typing import List, Optional
import datetime
from uuid import UUID
from pydantic import BaseModel, Field
import requests
from enum import Enum
import json


# Enums
class PaymentStatus(str, Enum):
    COMPLETED: str = "completed"
    AWAITING: str = "awaiting"
    CANCELLED: str = "cancelled"


# Models


class SessionOut(BaseModel):
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


class Payment(BaseModel):
    url: Optional[str]
    status: PaymentStatus


class BookSlotsIn(BaseModel):
    user_id: UUID
    service_id: UUID
    slots: List[datetime.datetime]


class BookSlotsOut(BaseModel):
    payment: Payment
    sessions: List[SessionOut]

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
