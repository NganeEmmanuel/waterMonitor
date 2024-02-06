import datetime

from sqlalchemy.orm import relationship

from Database.database import Base
from sqlalchemy import Column, Integer, Date, String


class Authority(Base):
    __tablename__ = "authority"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False, unique=True)  # ADMIN, MODERATOR, CUSTOMER
    user = relationship("User", back_populates="authorities")
    added_date = Column(Date, default=datetime)
