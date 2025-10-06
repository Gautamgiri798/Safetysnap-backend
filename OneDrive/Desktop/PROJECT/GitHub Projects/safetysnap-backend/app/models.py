from sqlalchemy import Column, Integer, String, JSON, DateTime
from .database import Base
import datetime

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    detections_hash = Column(String, unique=True)
    detections = Column(JSON)