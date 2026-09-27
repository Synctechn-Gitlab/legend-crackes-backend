from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProductImageBase(BaseModel):
    image_url: str
    sort_order: int = 0


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageResponse(ProductImageBase):
    id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)


def _normalize_product_dict(data: Any) -> Any:
    if not isinstance(data, dict):
        return data

    d = dict(data)

    # 1. Product code / code mapping & cleaning
    if "code" in d and "product_code" not in d:
        d["product_code"] = d.pop("code")
    if "product_code" in d:
        val = d["product_code"]
        d["product_code"] = str(val).strip() if val and str(val).strip() else None

    # 2. Original Price (MRP) mapping & numeric parsing
    if "originalPrice" in d and "original_price" not in d:
        d["original_price"] = d.pop("originalPrice")
    if "original_price" in d:
        val = d["original_price"]
        if val is None or val == "":
            d["original_price"] = 0.0
        else:
            try:
                d["original_price"] = float(val)
            except (ValueError, TypeError):
                pass

    # 2b. My Price (Cost Price) mapping & numeric parsing
    if "myPrice" in d and "my_price" not in d:
        d["my_price"] = d.pop("myPrice")
    if "my_price" in d:
        val = d["my_price"]
        if val is None or val == "":
            d["my_price"] = 0.0
        else:
            try:
                d["my_price"] = float(val)
            except (ValueError, TypeError):
                pass
    else:
        d["my_price"] = d.get("original_price", 0.0)

    # 3. Selling Price / Price mapping & numeric parsing
    if "sellingPrice" in d and "selling_price" not in d:
        d["selling_price"] = d.pop("sellingPrice")
    elif "price" in d and "selling_price" not in d:
        d["selling_price"] = d.pop("price")
    if "selling_price" in d:
        val = d["selling_price"]
        if val is None or val == "":
            d["selling_price"] = 0.0
        else:
            try:
                d["selling_price"] = float(val)
            except (ValueError, TypeError):
                pass

    # Auto-compute discount if original_price > selling_price
    orig_val = d.get("original_price", 0.0)
    sell_val = d.get("selling_price", 0.0)
    if orig_val > sell_val and orig_val > 0 and ("discount_percentage" not in d or d["discount_percentage"] in [0, None, ""]):
        d["discount_percentage"] = round(((orig_val - sell_val) / orig_val) * 100)

    # 4. Stock / Stock Quantity mapping & integer parsing (Default 99999 if not provided)
    if "stock" in d and "stock_quantity" not in d:
        d["stock_quantity"] = d.pop("stock")
    if "stock_quantity" in d:
        val = d["stock_quantity"]
        if val is None or val == "":
            d["stock_quantity"] = 99999
        else:
            try:
                d["stock_quantity"] = int(float(val))
            except (ValueError, TypeError):
                d["stock_quantity"] = 99999
    else:
        d["stock_quantity"] = 99999

    # 5. Discount / Discount Percentage mapping & rounding
    if "discount" in d and "discount_percentage" not in d:
        d["discount_percentage"] = d.pop("discount")
    if "discount_percentage" in d:
        val = d["discount_percentage"]
        if val is None or val == "":
            d["discount_percentage"] = 0
        else:
            try:
                d["discount_percentage"] = round(float(val))
            except (ValueError, TypeError):
                pass

    # 6. Image / Image URL mapping
    if "image" in d and "image_url" not in d:
        d["image_url"] = d.pop("image")
    if "image_url" in d:
        val = d["image_url"]
        d["image_url"] = str(val).strip() if val and str(val).strip() else None

    # 6b. Pieces Per Box / Packing (unit) mapping
    if "piecesPerBox" in d and "unit" not in d:
        d["unit"] = d.pop("piecesPerBox")
    elif "pieces_per_box" in d and "unit" not in d:
        d["unit"] = d.pop("pieces_per_box")
    if "unit" in d and d["unit"]:
        d["unit"] = str(d["unit"]).strip()

    # 7. isFeatured & isActive boolean casting
    if "isFeatured" in d and "is_featured" not in d:
        d["is_featured"] = d.pop("isFeatured")
    if "is_featured" in d and d["is_featured"] is not None:
        d["is_featured"] = bool(d["is_featured"])

    if "isActive" in d and "is_active" not in d:
        d["is_active"] = d.pop("isActive")
    if "is_active" in d and d["is_active"] is not None:
        d["is_active"] = bool(d["is_active"])

    # 8. Category Resolution (categoryId / category / category_id)
    if "categoryId" in d and "category_id" not in d:
        d["category_id"] = d.pop("categoryId")

    if "category_id" in d:
        cid = d["category_id"]
        if isinstance(cid, str):
            if cid.isdigit():
                d["category_id"] = int(cid)
            else:
                if "category" not in d or d["category"] is None:
                    d["category"] = cid
                d["category_id"] = None

    if "category" in d:
        cat_val = d["category"]
        if isinstance(cat_val, dict):
            if "id" in cat_val and not d.get("category_id"):
                try:
                    d["category_id"] = int(cat_val["id"])
                except (ValueError, TypeError):
                    pass
            d["category"] = cat_val.get("slug") or cat_val.get("name") or str(cat_val)
        elif isinstance(cat_val, int):
            if not d.get("category_id"):
                d["category_id"] = cat_val
            d["category"] = str(cat_val)
        elif isinstance(cat_val, str) and cat_val.isdigit():
            if not d.get("category_id"):
                d["category_id"] = int(cat_val)

    return d


class ProductBase(BaseModel):
    name: str
    product_code: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    original_price: float = Field(default=0.0, ge=0)
    my_price: Optional[float] = Field(default=0.0, ge=0)
    selling_price: float = Field(default=0.0, ge=0)
    discount_percentage: int = Field(default=0, ge=0, le=100)
    stock_quantity: int = Field(default=99999, ge=0)
    unit: str = "Box"
    is_featured: bool = False
    is_active: bool = True

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        return _normalize_product_dict(data)


class ProductCreate(ProductBase):
    images: Optional[List[str]] = None
    category: Optional[str] = None


class ProductUpdate(BaseModel):
    product_code: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    original_price: Optional[float] = Field(default=None, ge=0)
    my_price: Optional[float] = Field(default=None, ge=0)
    selling_price: Optional[float] = Field(default=None, ge=0)
    discount_percentage: Optional[int] = Field(default=None, ge=0, le=100)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    unit: Optional[str] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        return _normalize_product_dict(data)


class ProductStockUpdate(BaseModel):
    stock_quantity: int = Field(default=99999, ge=0, description="Updated stock quantity")

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        return _normalize_product_dict(data)


class ProductResponse(BaseModel):
    id: int
    product_code: str
    name: str
    slug: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    original_price: float = 0.0
    my_price: Optional[float] = 0.0
    selling_price: float = 0.0
    profit: Optional[float] = 0.0
    discount_percentage: int = 0
    stock_quantity: int = 99999
    unit: str = "Box"
    is_featured: bool = False
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    # Aliases / Convenience fields for seamless React UI consumption
    code: Optional[str] = None
    price: Optional[float] = None
    sellingPrice: Optional[float] = None
    myPrice: Optional[float] = None
    originalPrice: Optional[float] = None
    discount: Optional[int] = None
    stock: Optional[int] = 99999
    isFeatured: Optional[bool] = None
    isActive: Optional[bool] = None
    category: Optional[str] = None
    categoryName: Optional[str] = None
    piecesPerBox: Optional[str] = None
    pieces_per_box: Optional[str] = None
    image: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProductPaginatedResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    limit: int
    total_pages: int
