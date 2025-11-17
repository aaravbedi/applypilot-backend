import uuid
from datetime import datetime
from typing import List
import httpx
from bs4 import BeautifulSoup
from src.models import JobPosting

class JobScraperService:
    def __init__(self):
        self._jobs: List[JobPosting] = []

    @property
    def jobs(self) -> List[JobPosting]:
        return list(self._jobs)

    def scrape_greenhouse_board(self, board_url: str, company_name: str) -> List[JobPosting]:
        now = datetime.utcnow()
        resp = httpx.get(board_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        job_cards = soup.select("div.opening") or []

        scraped_jobs: List[JobPosting] = []

        for card in job_cards:
            title_el = card.select_one("a")
            location_el = card.select_one(".location")

            if not title_el:
                continue

            title = title_el.text.strip()
            url = title_el.get("href", "").strip()
            if url and not url.startswith("http"):
                url = board_url.rstrip("/") + "/" + url.lstrip("/")

            location = location_el.text.strip() if location_el else None

            job = JobPosting(
                id=str(uuid.uuid4()),
                title=title,
                company=company_name,
                location=location,
                source="greenhouse",
                url=url,
                created_at=now,
                scraped_at=now,
                tags=[],
            )
            scraped_jobs.append(job)

        self._jobs.extend(scraped_jobs)
        return scraped_jobs

    def get_jobs(self) -> List[JobPosting]:
        return list(self._jobs)
