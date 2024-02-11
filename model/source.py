import datetime

from sqlalchemy.orm import relationship

from Database.database import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey, Float


class Source(Base):
    """
    Provides information on different water sources and
    has a one-to-many relationship with quality.
    """
    __tablename__ = "source"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)  # name or tag of the water source
    location = Column(String(100))  # Country and city
    type = Column(String(50))  # river, lake, well, or reservoir
    capacity = Column(Float)  # The maximum capacity or volume of water that the source can hold
    status = Column(String(20))  # status of the water source, such as active, inactive, or under maintenance.
    water_level = Column(Float)  # The current water level or depth in the source.
    quality_id = Column(Integer, nullable=False)
    approvers = Column(String(200))
    complaints = Column(String(2000))
    # date when the water source's condition was initially added
    added_date = Column(Date, default=datetime.datetime.utcnow())
    # date when the water source's condition was last monitored
    modified_date = Column(Date, default=datetime.datetime.utcnow)
