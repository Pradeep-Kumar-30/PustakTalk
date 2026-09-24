from fastapi import Depends

from app.infrastructure.database.session import get_db_session

DatabaseSession = Depends(get_db_session)
