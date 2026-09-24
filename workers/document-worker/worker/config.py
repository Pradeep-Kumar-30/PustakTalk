from app.core.config import Settings, get_settings


def worker_settings() -> Settings:
    return get_settings()
