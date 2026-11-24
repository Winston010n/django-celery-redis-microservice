import logging
import time

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email_task(user_email):
    """Simulate sending a welcome email."""
    time.sleep(5)
    logger.info("Welcome email sent to %s", user_email)
    return f"Welcome email sent to {user_email}"


@shared_task
def clear_expired_cache_task():
    logger.info("Beat Task: Cleaning expired items...")
