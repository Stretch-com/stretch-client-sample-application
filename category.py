import os
import json
import datetime
from uuid import UUID
from typing import List
import requests
from fastapi import APIRouter
from pydantic import BaseModel, Field

# Models


class CategoryOut(BaseModel):
    id: UUID = Field(title="Category id", description="Category id in our system")
    name: str = Field(
        default=None,
        max_length=256,
        title="Category name",
        description="Category name in our system",
        examples=["Stretching"],
    )
    parent_id: UUID | None = Field(default=None, description="Parent category id")
    subcategories: List["CategoryOut"] | None = Field(  # type: ignore[type-arg]
        default=None,
        title="Subcategories",
        description="Subcategories of current directory",
        examples=[
            {
                "id": "e3e3e3e3-e3e3-e3e3-e3e3-e3e3e3e3e3e3",
                "name": "Stretching",
                "parent_id": "e3e3e3e3-e3e3-e3e3-e3e3-e3e3e3e3e3e3",
                "subcategories": [],
            }
        ],
    )

# -------------------------------------------------------------------------------------------------


router = APIRouter()
session = requests.Session()
base_url = os.getenv('STRETCH_PUBLIC_API_URL', 'https://api.stretch.com/api/v1/public')
session.headers.update({
            "Content-Type": "application/json",
            "Api-Token": os.getenv('CLIENT_ID')
        })


@router.get("/categories", response_model=List[CategoryOut])
async def get_categories():
    return session.get(f"{base_url}/categories").json()
