from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil
import os

from .. import crud, schemas
from ..database import get_db
from ..services.ppe_detector import detect_ppe

router = APIRouter(
    prefix="/api",
    tags=["images"],
)

UPLOAD_DIRECTORY = "./uploads"

@router.post("/images", response_model=schemas.ImageResponse)
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detections_list, detections_hash = detect_ppe(file_path)

    existing_image = crud.get_image_by_hash(db, file_hash=detections_hash)
    if existing_image:
        os.remove(file_path)
        image_url = f"/uploads/{existing_image.filename}"
        return schemas.ImageResponse(**existing_image.__dict__, image_url=image_url)

    image_data = schemas.ImageCreate(
        filename=file.filename,
        detections_hash=detections_hash,
        detections=detections_list
    )
    db_image = crud.create_image(db=db, image=image_data)
    image_url = f"/uploads/{db_image.filename}"
    return schemas.ImageResponse(**db_image.__dict__, image_url=image_url)

@router.get("/images", response_model=List[schemas.ImageResponse])
def read_images(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    images = crud.get_images(db, skip=skip, limit=limit)
    response = [schemas.ImageResponse(**img.__dict__, image_url=f"/uploads/{img.filename}") for img in images]
    return response

@router.get("/images/{image_id}", response_model=schemas.ImageResponse)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image_by_id(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    image_url = f"/uploads/{db_image.filename}"
    return schemas.ImageResponse(**db_image.__dict__, image_url=image_url)