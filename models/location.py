from pydantic import Field, BaseModel
from typing import Optional, Tuple


class LocationIn(BaseModel):
    coord: Optional[Tuple[float, float]] = Field()
    country: str = Field(example="United Arab Emirates", description="Country")
    state: str = Field(example="Dubai", description="state")
    city: str = Field(example="Dubai", description="city")
    line1: str = Field(example="Jumeirah Lake Towers", description="line 1")
    line2: str = Field(default="", description="line 2")
    zip: str = Field(example=None, description="zip (po box)")