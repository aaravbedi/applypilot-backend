from typing import List, Dict
from src.models import JobPosting, Contact

class ReferralEngineService:
    def __init__(self):
        self._contacts: List[Contact] = []

    def add_contact(self, contact: Contact) -> Contact:
        self._contacts.append(contact)
        return contact

    def list_contacts(self) -> List[Contact]:
        return list(self._contacts)

    def contacts_for_company(self, company: str) -> List[Contact]:
        return [
            c for c in self._contacts
            if c.company.lower() == company.lower()
        ]

    def recommend_referrals(self, jobs: List[JobPosting]) -> Dict[str, List[Contact]]:
        results: Dict[str, List[Contact]] = {}
        for job in jobs:
            contacts = self.contacts_for_company(job.company)
            if contacts:
                results[job.id] = contacts
        return results
