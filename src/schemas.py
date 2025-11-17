from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class JobBase(BaseModel):
    id: str
    title: str
    company: str
    location: Optional[str] = None
    source: str  
    url: HttpUrl
    created_at: datetime
    scraped_at: datetime


class JobOut(JobBase):
    tags: list[str] = []


class ApplicationCreate(BaseModel):
    job_id: str
    resume_version: Optional[str] = None
    status: str = "applied" 
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: str
    job_id: str
    status: str
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class ReferralContact(BaseModel):
    id: str
    name: str
    company: str
    role: Optional[str] = None
    relationship_strength: int = 1  
    email: Optional[str] = None
    linkedin: Optional[HttpUrl] = None


class ReferralLead(BaseModel):
    job: JobOut
    contacts: List[ReferralContact]
