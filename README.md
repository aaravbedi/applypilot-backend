# ApplyPilot – Backend Sketch

This repo is a backend sketch for ApplyPilot – a job search co-pilot that I tried working on previously:
- scrapes job postings on a schedule (will try 24/7),
- keeps track of a user’s applications like a mini ATS,
- and stores referral leads / warm intros in one place.

The goal here isn’t to ship a full production system in one repo, but to have a clean, realistic backend structure that shows how the core pieces fit together:

- an API layer (FastAPI),
- a job scraping layer,
- an ATS-style application tracking layer,
- and a referral engine for managing who to reach out to at which company.
  
## Project Layout

```text
applypilot-backend/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py          
│   ├── models.py        
│   ├── schemas.py         
│   └── services/
│       ├── __init__.py
│       ├── job_scraper.py   
│       ├── ats_tracker.py   
│       └── referral_engine.py
└── scripts/
    └── run_scraper_once.py  
