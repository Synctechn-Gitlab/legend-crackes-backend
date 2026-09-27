from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.logging import audit_logger
from app.repositories.admin_repo import admin_repo
from app.schemas.admin import TokenResponse, AdminResponse


class AuthService:
    def authenticate_admin(self, db: Session, identifier: str, plain_password: str) -> TokenResponse:
        admin = admin_repo.get_by_username_or_email(db, identifier)
        if not admin or not verify_password(plain_password, admin.password_hash):
            audit_logger.warning(f"Failed login attempt for identifier: {identifier}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username/email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not admin.is_active:
            audit_logger.warning(f"Deactivated admin login attempt: {admin.username}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin account is inactive. Please contact system administrator."
            )

        access_token = create_access_token(subject=admin.id)
        refresh_token = create_refresh_token(subject=admin.id)
        
        audit_logger.info(f"Successful admin login: {admin.username} (ID: {admin.id})")

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
            user=AdminResponse.model_validate(admin)
        )

    def refresh_access_token(self, db: Session, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type for refresh."
            )

        admin_id = int(payload.get("sub"))
        admin = admin_repo.get(db, admin_id)
        if not admin or not admin.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive."
            )

        new_access_token = create_access_token(subject=admin.id)
        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            refresh_token=refresh_token,
            user=AdminResponse.model_validate(admin)
        )


auth_service = AuthService()
