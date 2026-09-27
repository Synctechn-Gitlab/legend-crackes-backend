from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    role: str = "superadmin"

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    user: AdminResponse


class TokenRefreshRequest(BaseModel):
    refresh_token: str
