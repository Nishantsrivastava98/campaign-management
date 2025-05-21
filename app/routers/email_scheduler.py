from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import db, models, schemas
from datetime import datetime, timedelta
import logging
import pytz

router = APIRouter(prefix="/simulate-email-scheduler", tags=["EmailScheduler"])

async def get_db():
    async with db.SessionLocal() as session:
        yield session


@router.post("/run", response_model=dict)
async def simulate_scheduler(session: AsyncSession = Depends(get_db)):

    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    weekday = now.weekday()
    hour = now.hour
    if weekday > 4 or hour < 10 or hour >= 17:
        return {"scheduled": 0, "message": "Outside allowed scheduling window"}

    result = await session.execute(select(models.Campaign))
    campaigns = result.scalars().all()
    scheduled_count = 0
    for campaign in campaigns:

        q = select(models.EmailSequence).join(models.Lead).where(
            models.Lead.campaign_id == campaign.id,
            models.EmailSequence.status == models.EmailStatus.pending
        ).limit(8)
        emails = (await session.execute(q)).scalars().all()
        for email in emails:
            email.status = models.EmailStatus.sent
            email.sent_at = now
            scheduled_count += 1
    await session.commit()
    logging.info(f"Simulated sending {scheduled_count} emails at {now}")
    return {"scheduled": scheduled_count, "timestamp": now.isoformat()}
