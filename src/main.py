from fastapi import FastAPI, HTTPException
from typing import List

from src.schemas import (
    JobOut,
    ApplicationCreate,
    ApplicationOut,
    ApplicationUpdate,
    ReferralLead,
    ReferralContact,
)
from src.models import JobPosting, Contact
from src.services.job_scraper import JobScraperService
from src.services.ats_tracker import ATSTrackerService
from src.services.referral_engine import ReferralEngineService


app = FastAPI(title="ApplyPilot Backend Sketch")

job_scraper = JobScraperService()
ats_tracker = ATSTrackerService()
referral_engine = ReferralEngineService()


def job_to_out(job: JobPosting) -> JobOut:
    return JobOut(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        source=job.source,
        url=job.url,
        created_at=job.created_at,
        scraped_at=job.scraped_at,
        tags=job.tags,
    )


@app.get("/jobs", response_model=List[JobOut])
def list_jobs():
    jobs = job_scraper.get_jobs()
    return [job_to_out(j) for j in jobs]


@app.post("/applications", response_model=ApplicationOut)
def create_application(payload: ApplicationCreate):
    app_obj = ats_tracker.create_application(
        job_id=payload.job_id,
        status=payload.status,
        resume_version=payload.resume_version,
        notes=payload.notes,
    )
    return ApplicationOut(
        id=app_obj.id,
        job_id=app_obj.job_id,
        status=app_obj.status,
        resume_version=app_obj.resume_version,
        notes=app_obj.notes,
        created_at=app_obj.created_at,
        updated_at=app_obj.updated_at,
    )


@app.get("/applications", response_model=List[ApplicationOut])
def list_applications():
    apps = ats_tracker.list_applications()
    return [
        ApplicationOut(
            id=a.id,
            job_id=a.job_id,
            status=a.status,
            resume_version=a.resume_version,
            notes=a.notes,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )
        for a in apps
    ]


@app.patch("/applications/{app_id}", response_model=ApplicationOut)
def update_application(app_id: str, payload: ApplicationUpdate):
    app_obj = ats_tracker.update_application(
        app_id=app_id,
        status=payload.status,
        notes=payload.notes,
    )
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    return ApplicationOut(
        id=app_obj.id,
        job_id=app_obj.job_id,
        status=app_obj.status,
        resume_version=app_obj.resume_version,
        notes=app_obj.notes,
        created_at=app_obj.created_at,
        updated_at=app_obj.updated_at,
    )


@app.get("/referrals", response_model=List[ReferralLead])
def list_referral_leads():
    jobs = job_scraper.get_jobs()
    mapping = referral_engine.recommend_referrals(jobs)

    results: List[ReferralLead] = []
    for job in jobs:
        contacts = mapping.get(job.id, [])
        if not contacts:
            continue
        results.append(
            ReferralLead(
                job=job_to_out(job),
                contacts=[
                    ReferralContact(
                        id=c.id,
                        name=c.name,
                        company=c.company,
                        role=c.role,
                        relationship_strength=c.relationship_strength,
                        email=c.email,
                        linkedin=c.linkedin,
                    )
                    for c in contacts
                ],
            )
        )
    return results
