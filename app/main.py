from fastapi import FastAPI
from . import db, models
from fastapi.middleware.cors import CORSMiddleware
from .routers import campaigns, uploads, leads, email_scheduler
from .scheduler import start_scheduler

app = FastAPI(title="Colca Campaign Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campaigns.router)
app.include_router(uploads.router)
app.include_router(leads.router)
app.include_router(email_scheduler.router)

@app.on_event("startup")
async def startup():
    # Create tables
    async with db.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    # Pre-seed Client if not exists
    async with db.SessionLocal() as session:
        result = await session.execute(db.Base.metadata.tables['clients'].select())
        if not result.first():
            session.add(models.Client(name="Default Client"))
            await session.commit()
    start_scheduler()

@app.get("/")
def root():
    return {"message": "Colca Campaign Management API"}
