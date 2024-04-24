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


@router.get("/categories", response_model=List[CategoryOut])
async def get_categories():
    return session.get("/categories")
