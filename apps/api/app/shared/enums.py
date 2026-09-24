from enum import StrEnum


class DocumentStatus(StrEnum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Intent(StrEnum):
    DOCUMENT_QA = "document_qa"
    PAGE_SEARCH = "page_search"
    EXACT_SEARCH = "exact_search"
    PAGE_SUMMARY = "page_summary"
    DOCUMENT_SUMMARY = "document_summary"
    MULTI_DOCUMENT_COMPARE = "multi_document_compare"
    SELECTED_TEXT = "selected_text"
    STUDY_MATERIAL = "study_material"
    GENERAL_CHAT = "general_chat"
