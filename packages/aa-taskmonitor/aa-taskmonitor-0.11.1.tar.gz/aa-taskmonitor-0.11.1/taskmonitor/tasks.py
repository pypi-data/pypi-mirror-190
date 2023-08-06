import datetime as dt

from celery import shared_task

from django.utils import timezone

from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce
from app_utils.logging import LoggerAddTag

from . import __title__
from .app_settings import TASKMONITOR_DATA_MAX_AGE
from .core import cached_reports
from .models import TaskLog

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

DEFAULT_TASK_PRIORITY = 4


@shared_task(base=QueueOnce)
def run_housekeeping():
    """Run all housekeeping tasks."""
    delete_stale_tasklogs.apply_async(priority=7)
    refresh_reports_cache.apply_async(priority=DEFAULT_TASK_PRIORITY)


@shared_task
def delete_stale_tasklogs():
    """Delete all stale tasklogs from the database."""
    old_entries = TaskLog.objects.filter(
        timestamp__lte=timezone.now() - dt.timedelta(hours=TASKMONITOR_DATA_MAX_AGE)
    )
    old_entries_count = old_entries.count()
    old_entries._raw_delete(old_entries.db)
    logger.info(f"Deleted {old_entries_count:,} stale tasklogs.")


@shared_task
def refresh_reports_cache():
    """Refresh cache for all reports."""
    reports = cached_reports.reports()
    logger.info(f"Refreshing caches for {len(reports)} reports...")
    for report in reports:
        refresh_single_report_cache.apply_async(
            priority=DEFAULT_TASK_PRIORITY, args=[report.name]
        )


@shared_task
def refresh_single_report_cache(report_name: str):
    """Refresh cache for given report."""
    cached_reports.report(report_name).refresh_cache()
    logger.info(f"Refreshed reports cache of {report_name}.")
