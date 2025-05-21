from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import enum

class CampaignCreate(BaseModel):
    name: str
    client_id: int

class CampaignOut(BaseModel):
    id: int
    name: str
    client_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class LeadOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    company: Optional[str]
    job_title: Optional[str]
    linkedin_url: Optional[str]
    campaign_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UploadLogOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    campaign_id: int
    class Config:
        orm_mode = True

class EmailStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"

class EmailSequenceOut(BaseModel):
    id: int
    lead_id: int
    subject: str
    body: str
    status: EmailStatus
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    class Config:
        orm_mode = True
