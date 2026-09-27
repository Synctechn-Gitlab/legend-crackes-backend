from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.schemas.admin import AdminLoginRequest, TokenResponse, TokenRefreshRequest, AdminResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Admin Login",
    description="Authenticate an administrator with username/email and password to obtain a JWT access token."
)
def login(credentials: AdminLoginRequest, db: Session = Depends(get_db)):
    return auth_service.authenticate_admin(
        db=db,
        identifier=credentials.username,
        plain_password=credentials.password
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh Access Token",
    description="Obtain a refreshed access token using a valid refresh token."
)
def refresh_token(payload: TokenRefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(db=db, refresh_token=payload.refresh_token)


@router.get(
    "/me",
    response_model=AdminResponse,
    summary="Get Current Admin Profile",
    description="Returns profile details of the authenticated administrator."
)
def get_me(current_admin: AdminUser = Depends(get_current_admin)):
    return AdminResponse.model_validate(current_admin)


@router.post(
    "/logout",
    summary="Admin Logout",
    description="Client clears stored tokens. Server registers logout audit."
)
def logout(current_admin: AdminUser = Depends(get_current_admin)):
    return {"success": True, "message": "Successfully logged out."}
