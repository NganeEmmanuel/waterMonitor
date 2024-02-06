import datetime

from sqlalchemy.orm import relationship

from Database.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.mutable import MutableList


class User(Base):
    """
        users with different authorities -- has a one-to-many relationship with authority
    """
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), unique=False, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    authority_id = Column(MutableList.as_mutable(Integer), ForeignKey("authority.id"), nullable=False)
    authorities = relationship("Authority", back_populates="user")
    source = relationship("Source", back_populates="users")
    complaint = relationship("Complaint", back_populates="user")
    date_joined = Column(Date, default=datetime.datetime.now())
    updated_date = Column(Date, default=datetime.datetime.now())
