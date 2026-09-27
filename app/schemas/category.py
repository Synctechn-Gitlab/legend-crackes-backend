from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, model_validator


class CategoryBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "image" in data and not data.get("image_url"):
                data["image_url"] = data["image"]
            if "isActive" in data and "is_active" not in data:
                data["is_active"] = data["isActive"]
        return data


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "image" in data and "image_url" not in data:
                data["image_url"] = data["image"]
            if "isActive" in data and "is_active" not in data:
                data["is_active"] = data["isActive"]
        return data


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    product_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
