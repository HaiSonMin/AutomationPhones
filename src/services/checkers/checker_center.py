"""
Checker Center - Main service for all checking operations
Coordinates various checker services including phone sync
"""

from .phone.sync import ServicePhoneSync


class CheckerCenter:
    def __init__(self, user_id: str = None):
        """Initialize the checker center with all services"""
        self.user_id = user_id
        self.phone_sync = ServicePhoneSync(user_id=user_id)

    def phones(self, user_id: str = None):
        """
        Start phone checking/syncing services

        Args:
            user_id: Optional user identifier for the sync operations

        Returns:
            ServicePhoneSync instance for further control
        """
        # Start the phone sync service
        self.phone_sync.start()

        # Optionally trigger immediate sync with user_id
        if user_id:
            self.phone_sync.run_sync_now(user_id)
            self.phone_sync.run_setup_now(user_id)

        return self.phone_sync

    def stop_all(self):
        """Stop all checker services"""
        if hasattr(self, "phone_sync"):
            self.phone_sync.stop()

    def get_status(self):
        """Get status of all checker services"""
        status = {
            "phone_sync": {"running": self.phone_sync.scheduler.running, "jobs": []}
        }

        # Get phone sync job details
        for job in self.phone_sync.get_jobs():
            status["phone_sync"]["jobs"].append(
                {"name": job.name, "id": job.id, "next_run": str(job.next_run_time)}
            )

        return status
