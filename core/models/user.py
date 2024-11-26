from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base
from .mixins import IDMixin


class User(IDMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
        }
