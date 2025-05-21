from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .csv_processor import process_csv_uploads
import logging

scheduler = AsyncIOScheduler()


scheduler.add_job(process_csv_uploads, 'interval', minutes=5)

def start_scheduler():
    try:
        scheduler.start()
        logging.info("Scheduler started.")
    except Exception as e:
        logging.error(f"Scheduler error: {e}")
