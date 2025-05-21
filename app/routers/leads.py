from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import db, models, schemas
from typing import List

router = APIRouter(prefix="/leads", tags=["Leads"])

async def get_db():
    async with db.SessionLocal() as session:
        yield session

@router.get("/by-campaign/{campaign_id}", response_model=List[schemas.LeadOut])
async def list_leads_by_campaign(campaign_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Lead).where(models.Lead.campaign_id == campaign_id))
    return result.scalars().all()
