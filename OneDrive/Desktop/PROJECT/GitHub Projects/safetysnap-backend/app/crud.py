from sqlalchemy.orm import Session
from . import models, schemas
import hashlib

def get_image_by_id(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def get_image_by_hash(db: Session, file_hash: str):
    return db.query(models.Image).filter(models.Image.detections_hash == file_hash).first()

def get_images(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Image).offset(skip).limit(limit).all()

def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(
        filename=image.filename,
        detections_hash=image.detections_hash,
        detections=[det.model_dump() for det in image.detections]
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image