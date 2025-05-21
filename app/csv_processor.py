import os
import csv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import db, models
from datetime import datetime
import logging

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

async def process_csv_uploads():
    async with db.SessionLocal() as session:
        # Find unprocessed uploads
        result = await session.execute(select(models.UploadLog))
        logs = result.scalars().all()
        for log in logs:
            file_path = os.path.join(UPLOAD_DIR, log.filename)
            if not os.path.exists(file_path):
                continue
            # Check if leads already exist for this upload (skip if so)
            lead_exists = await session.execute(select(models.Lead).where(models.Lead.campaign_id == log.campaign_id))
            if lead_exists.first():
                continue
            # Parse CSV and insert leads
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    lead = models.Lead(
                        name=row.get('name'),
                        email=row.get('email'),
                        company=row.get('company'),
                        job_title=row.get('job_title'),
                        linkedin_url=row.get('linkedin_url'),
                        campaign_id=log.campaign_id
                    )
                    session.add(lead)
            await session.commit()
            logging.info(f"Processed leads from {log.filename}")
