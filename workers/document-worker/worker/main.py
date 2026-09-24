from typing import ClassVar

from app.core.config import get_settings
from arq.connections import RedisSettings

from worker.jobs.process_document import process_document


class WorkerSettings:
    functions: ClassVar[list] = [process_document]
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
    max_jobs = 2
    job_timeout = 60 * 30
    keep_result = 0
