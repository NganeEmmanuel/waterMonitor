import datetime

from sqlalchemy.orm import relationship

from Database.database import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey, Double
from sqlalchemy.ext.mutable import MutableList


class Source(Base):
    """
        provides information on different water sources and
        has a one-to-many relationship with quality.
    """
    __tablename__ = "source"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)  # name or tag of the water source
    location = Column(String(100))  # Country and city
    type = Column(String(50))  # river, lake, well, or reservoir
    capacity = Column(Double)  # The maximum capacity or volume of water that the source can hold
    Status = Column(String(20))  # status of the water source, such as active, inactive, or under maintenance.
    water_level = Column(Double)  # The current water level or depth in the source.
    quality_id = Column(Integer, ForeignKey("quality.id"), nullable=True)
    quality_readings = relationship("Quality", back_populates="source")
    user_id = Column(MutableList.as_mutable(Integer), ForeignKey("user.id"), nullable=True)  # moderators that have approved this reading
    users = relationship("User", back_populates="source")
    complaint = relationship("Complaint", back_populates="source")
    added_date = Column(Date, default=datetime.datetime)  # date when the water source's condition was initially added
    modified_date = Column(Date, default=datetime.datetime)  # date when the water source's condition was last monitored
