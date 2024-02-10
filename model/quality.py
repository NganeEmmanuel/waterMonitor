import datetime

from sqlalchemy.orm import relationship

from Database.database import Base
from sqlalchemy import Column, Integer, Date, Double


class Quality(Base):
    """
        provides quality of different water sources and
        has a many-to-one relationship with sources.
    """
    __tablename__ = "quality"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    ph_level = Column(Double)  # Dimensionless (pH scale)
    temperature = Column(Double)  # Celsius (°C)
    turbidity = Column(Double)  # Nephelometric Turbidity Unit (NTU)
    dissolved_0xygen = Column(Double)  # Milligrams per liter (mg/L)
    conductivity = Column(Double)  # Millisiemens per meter (mS/m)
    total_dissolved_solids = Column(Double)  # Milligrams per liter (mg/L)
    biochemical_oxygen_demand = Column(Double)  # Milligrams per liter (mg/L)
    chemical_oxygen_demand = Column(Double)  # Milligrams per liter (mg/L)
    total_suspended_solids = Column(Double)  # Milligrams per liter (mg/L)
    chlorine_residual = Column(Double)  # Milligrams per liter (mg/L)
    source = relationship("Source", back_populates="quality_readings")
    added_date = Column(Date, default=datetime.datetime.utcnow())
    modified_date = Column(Date, default=datetime.datetime.utcnow())
