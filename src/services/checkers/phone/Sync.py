"""
Phone Sync Service - Scheduled Tasks Implementation
Handles periodic syncing and setup operations using APScheduler
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import atexit


class ServicePhoneSync:
    def __init__(self, user_id: str = None):
        """Initialize the sync service with a background scheduler"""
        self.scheduler = BackgroundScheduler()
        self.logger = logging.getLogger(__name__)
        self.user_id = user_id

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # Add jobs
        self._setup_jobs()

        # Register cleanup on exit
        atexit.register(lambda: self.scheduler.shutdown())

    def _setup_jobs(self):
        """Setup scheduled jobs"""
        # Job 1: sync_to_server - runs every 10 seconds
        self.scheduler.add_job(
            func=self.sync_to_server,
            trigger=IntervalTrigger(seconds=10),
            id="sync_to_server_job",
            name="Sync to Server",
            replace_existing=True,
        )

        # Job 2: setup - runs every 30 seconds
        self.scheduler.add_job(
            func=self.setup,
            trigger=IntervalTrigger(seconds=30),
            id="setup_job",
            name="Setup Task",
            replace_existing=True,
        )

    def sync_to_server(self, user_id: str = None):
        """
        Sync data to server
        Called every 10 seconds by scheduler
        """
        try:
            # Use instance user_id if no parameter provided
            uid = user_id or self.user_id
            self.logger.info(f"Syncing to server... User ID: {uid}")

            # TODO: Implement actual sync logic here
            # Example:
            # - Collect device data
            # - Send to server via API
            # - Handle response/errors

            self.logger.info("Sync to server completed successfully")

        except Exception as e:
            self.logger.error(f"Error during sync_to_server: {e}")

    def setup(self, user_id: str = None):
        """
        Perform setup tasks
        Called every 30 seconds by scheduler
        """
        try:
            # Use instance user_id if no parameter provided
            uid = user_id or self.user_id
            self.logger.info(f"Running setup... User ID: {uid}")

            # TODO: Implement actual setup logic here
            # Example:
            # - Check device status
            # - Apply configurations
            # - Update settings

            self.logger.info("Setup completed successfully")

        except Exception as e:
            self.logger.error(f"Error during setup: {e}")

    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            self.logger.info("Sync service started")

    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self.logger.info("Sync service stopped")

    def pause_job(self, job_id: str):
        """Pause a specific job"""
        self.scheduler.pause_job(job_id)
        self.logger.info(f"Job {job_id} paused")

    def resume_job(self, job_id: str):
        """Resume a specific job"""
        self.scheduler.resume_job(job_id)
        self.logger.info(f"Job {job_id} resumed")

    def get_jobs(self):
        """Get all scheduled jobs"""
        return self.scheduler.get_jobs()

    def run_sync_now(self, user_id: str = None):
        """Manually trigger sync_to_server"""
        self.sync_to_server(user_id)

    def run_setup_now(self, user_id: str = None):
        """Manually trigger setup"""
        self.setup(user_id)


# Example usage
if __name__ == "__main__":
    # Create sync service instance
    sync_service = ServicePhoneSync()

    # Start the service
    sync_service.start()

    print("Sync service is running...")
    print("Press Ctrl+C to stop")

    try:
        # Keep the main thread alive
        import time

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping sync service...")
        sync_service.stop()
