from src.services.job_scraper import JobScraperService

if __name__ == "__main__":
    scraper = JobScraperService()
    url = "https://boards.greenhouse.io/example-company"
    jobs = scraper.scrape_greenhouse_board(url, company_name="Example Company")

    print(f"Scraped {len(jobs)} jobs from {url}")
    for job in jobs[:5]:
        print(f"- {job.title} @ {job.company} ({job.location})")
