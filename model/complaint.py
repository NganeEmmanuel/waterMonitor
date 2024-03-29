import datetime

from sqlalchemy.orm import relationship

from Database.database import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey


class Complaint(Base):
    __tablename__ = "complaint"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    details = Column(String(5000), nullable=False)
    source_id = Column(Integer, ForeignKey("source.id"), nullable=False)  # user making compliant, customer authority
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # user making compliant, customer authority
    added_date = Column(Date, default=datetime.datetime.utcnow())
