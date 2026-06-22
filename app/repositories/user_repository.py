from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from app.models.enums import UserRole

class UserRepository(BaseRepository[User]):
    """Repository مخصوص کاربران"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_role(self, role: UserRole) -> List[User]:
        return self.db.query(User).filter(User.role == role).all()
    
    def get_active_users(self) -> List[User]:
        return self.db.query(User).filter(User.is_active == True).all()
    
    def update_role(self, user_id: int, new_role: UserRole) -> Optional[User]:
        return self.update(user_id, role=new_role)
    
    def get_authors(self) -> List[User]:
        return self.db.query(User).filter(User.role.in_([UserRole.AUTHOR, UserRole.ADMIN])).all()