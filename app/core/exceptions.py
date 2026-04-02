"""API errors shaped like docs/api-contracts.md (error envelope)."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class APIError(Exception):
    def __init__(
        self,
        status_code: int,
        *,
        code: str,
        message: str,
        details: dict | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


async def api_error_handler(_request: Request, exc: APIError) -> JSONResponse:
    body: dict = {"error": {"code": exc.code, "message": exc.message}}
    if exc.details is not None:
        body["error"]["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content=body)


async def validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    errs = exc.errors()
    first = errs[0] if errs else {}
    loc = first.get("loc", ())
    field = str(loc[-1]) if loc else "body"
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Error en validación de datos",
                "details": {"field": field, "reason": first.get("msg", "Invalid input")},
            }
        },
    )
