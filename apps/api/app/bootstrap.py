"""Imports all SQLAlchemy models before schema/migration operations."""

from app.modules.auth.models import User
from app.modules.chat.models import Citation, Message
from app.modules.conversations.models import Conversation
from app.modules.documents.models import Document, DocumentChunk, DocumentPage, ProcessingJob
from app.modules.users.models import UserSettings
from app.modules.workspaces.models import Workspace

__all__ = [
    "Citation",
    "Conversation",
    "Document",
    "DocumentChunk",
    "DocumentPage",
    "Message",
    "ProcessingJob",
    "User",
    "UserSettings",
    "Workspace",
]
