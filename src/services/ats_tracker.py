import uuid
from datetime import datetime
from typing import List, Optional

from src.models import Application


class ATSTrackerService:
    def __init__(self):
        self._applications: List[Application] = []

    def create_application(
        self,
        job_id: str,
        status: str = "applied",
        resume_version: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Application:
        now = datetime.utcnow()
        app = Application(
            id=str(uuid.uuid4()),
            job_id=job_id,
            status=status,
            resume_version=resume_version,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self._applications.append(app)
        return app

    def list_applications(self) -> List[Application]:
        return list(self._applications)

    def get_application(self, app_id: str) -> Optional[Application]:
        for app in self._applications:
            if app.id == app_id:
                return app
        return None

    def update_application(
        self,
        app_id: str,
        status: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[Application]:
        app = self.get_application(app_id)
        if not app:
            return None

        changed = False
        if status is not None and status != app.status:
            app.status = status
            changed = True
        if notes is not None and notes != app.notes:
            app.notes = notes
            changed = True

        if changed:
            app.updated_at = datetime.utcnow()

        return app
