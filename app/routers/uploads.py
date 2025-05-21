from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .. import db, models
from datetime import datetime
import os
import shutil

router = APIRouter(prefix="/uploads", tags=["Uploads"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get_db():
    async with db.SessionLocal() as session:
        yield session

@router.post("/csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(
    campaign_id: int = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db)
):

    campaign = await session.get(models.Campaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    filename = f"{datetime.utcnow().isoformat()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_log = models.UploadLog(filename=filename, campaign_id=campaign_id)
    session.add(upload_log)
    await session.commit()
    return {"filename": filename, "campaign_id": campaign_id}
