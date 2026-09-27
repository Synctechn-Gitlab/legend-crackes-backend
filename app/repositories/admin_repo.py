from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.admin_user import AdminUser
from app.repositories.base import BaseRepository


class AdminRepository(BaseRepository[AdminUser]):
    def __init__(self):
        super().__init__(AdminUser)

    def get_by_username_or_email(self, db: Session, identifier: str) -> Optional[AdminUser]:
        clean_identifier = identifier.strip().lower()
        return db.query(AdminUser).filter(
            or_(
                AdminUser.username.ilike(clean_identifier),
                AdminUser.email.ilike(clean_identifier)
            )
        ).first()

    def get_by_username(self, db: Session, username: str) -> Optional[AdminUser]:
        return db.query(AdminUser).filter(AdminUser.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[AdminUser]:
        return db.query(AdminUser).filter(AdminUser.email.ilike(email.strip())).first()


admin_repo = AdminRepository()
