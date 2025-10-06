from pydantic import BaseModel
from typing import List, Optional
import datetime

class DetectionBox(BaseModel):
    label: str
    confidence: float
    box: List[float] # [x1, y1, x2, y2] normalized

class ImageBase(BaseModel):
    filename: str
    detections_hash: str

class ImageCreate(ImageBase):
    detections: List[DetectionBox]

class ImageResponse(ImageBase):
    id: int
    upload_date: datetime.datetime
    detections: List[DetectionBox]
    image_url: str

    class Config:
        from_attributes = True