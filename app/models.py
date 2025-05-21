from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base
import enum

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    # Pre-seeded, no CRUD

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    client = relationship("Client", backref="campaigns")

class UploadLog(Base):
    __tablename__ = "upload_logs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    campaign = relationship("Campaign", backref="upload_logs")

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    company = Column(String)
    job_title = Column(String)
    linkedin_url = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    campaign = relationship("Campaign", backref="leads")

class EmailStatus(enum.Enum):
    pending = "pending"
    sent = "sent"

class EmailSequence(Base):
    __tablename__ = "email_sequences"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(Enum(EmailStatus), default=EmailStatus.pending, nullable=False)
    scheduled_at = Column(DateTime(timezone=True))
    sent_at = Column(DateTime(timezone=True))
    lead = relationship("Lead", backref="email_sequences")

Index("ix_lead_campaign", Lead.campaign_id)
Index("ix_email_lead", EmailSequence.lead_id)
