from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import db, models, schemas
from typing import List

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

async def get_db():
    async with db.SessionLocal() as session:
        yield session

@router.post("/", response_model=schemas.CampaignOut, status_code=status.HTTP_201_CREATED)
async def create_campaign(campaign: schemas.CampaignCreate, session: AsyncSession = Depends(get_db)):
    client = await session.get(models.Client, campaign.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db_campaign = models.Campaign(name=campaign.name, client_id=campaign.client_id)
    session.add(db_campaign)
    await session.commit()
    await session.refresh(db_campaign)
    return db_campaign

@router.get("/by-client/{client_id}", response_model=List[schemas.CampaignOut])
async def list_campaigns_by_client(client_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Campaign).where(models.Campaign.client_id == client_id))
    return result.scalars().all()
