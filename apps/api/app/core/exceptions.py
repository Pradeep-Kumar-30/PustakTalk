from dataclasses import dataclass


@dataclass(slots=True)
class DomainError(Exception):
    detail: str
    status_code: int = 400
    code: str = "domain_error"


class NotFoundError(DomainError):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail, 404, "not_found")


class AuthorizationError(DomainError):
    def __init__(self, detail: str = "You do not have access to this resource") -> None:
        super().__init__(detail, 403, "forbidden")


class ConflictError(DomainError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, 409, "conflict")


class ServiceUnavailableError(DomainError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, 503, "service_unavailable")
