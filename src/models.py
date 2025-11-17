from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class JobPosting:
    id: str
    title: str
    company: str
    location: Optional[str]
    source: str
    url: str
    created_at: datetime
    scraped_at: datetime
    tags: List[str] = field(default_factory=list)


@dataclass
class Application:
    id: str
    job_id: str
    status: str
    resume_version: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class Contact:
    id: str
    name: str
    company: str
    role: Optional[str]
    relationship_strength: int  
    email: Optional[str]
    linkedin: Optional[str]
