from sqlalchemy import Column, Integer, String

from Database.database import Base


class AuthUser(Base):
    """
    Users with different authorities -- has a one-to-many relationship with authority
    """
    __tablename__ = "auth_user"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), unique=False, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    authority = Column(String(20), nullable=False)